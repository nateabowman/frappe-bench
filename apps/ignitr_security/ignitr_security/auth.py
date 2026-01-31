import hashlib
from datetime import datetime, timedelta

import frappe
from frappe.utils import now_datetime

# ---- Settings ----
DEFAULT_ENFORCE = True                 # master on/off
BIND_TO_IP_MODE = "24"                 # "off", "32" (exact), "24" (subnet /24)
BIND_TO_UA      = "family"             # "off", "exact", "family"
KICK_OLD_SESSIONS = True               # kill all other sessions for the user
EXEMPT_ROLES = {"Integration User"}    # roles skipped (e.g., API only)
CACHE_TTL_SECONDS = 60 * 60 * 24 * 7   # 7 days cache TTL

# Optional: write an audit log row to DB? (uses User Log doctype)
WRITE_AUDIT_LOG = True


def _request_meta():
    req = frappe.local.request
    ip  = getattr(frappe.local, "request_ip", None) or req.headers.get("X-Forwarded-For", req.remote_addr)
    ua  = req.headers.get("User-Agent", "") or ""
    return (ip or "").strip(), (ua or "").strip()


def _ua_family(ua: str) -> str:
    """Very light UA normalization: browser family + major version bucket."""
    ua_l = ua.lower()
    buckets = ["chrome", "chromium", "edge", "safari", "firefox", "opera"]
    for b in buckets:
        if b in ua_l:
            return b
    # fallback: first token
    return ua_l.split("/", 1)[0][:32]


def _ip_bucket(ip: str) -> str:
    if not ip or BIND_TO_IP_MODE == "off":
        return ""
    try:
        if ":" in ip:
            # IPv6: use /64 bucket (first 4 hextets) as an approximation
            parts = ip.split(":")
            if len(parts) >= 4:
                return ":".join(parts[:4]) + "::/64"
            return ip
        # IPv4
        octets = ip.split(".")
        if len(octets) != 4:
            return ip
        if BIND_TO_IP_MODE == "32":
            return ip
        # default /24
        return ".".join(octets[:3]) + ".0/24"
    except Exception:
        return ip


def _fingerprint(ip: str, ua: str) -> str:
    ua_key = ""
    if BIND_TO_UA == "exact":
        ua_key = ua
    elif BIND_TO_UA == "family":
        ua_key = _ua_family(ua)
    # ip bucket
    ip_key = _ip_bucket(ip)
    raw = f"{ip_key}|{ua_key}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _cache_key(user: str) -> str:
    return f"session_lock:{frappe.local.site}:{user}"


def _set_lock(user: str, sid: str, fp: str, ip: str, ua: str):
    cache = frappe.cache()
    key = _cache_key(user)
    cache.hmset(key, {"sid": sid, "fp": fp, "ip": ip, "ua": ua, "ts": now_datetime().isoformat()})
    cache.expire(key, CACHE_TTL_SECONDS)


def _get_lock(user: str) -> dict:
    key = _cache_key(user)
    h = frappe.cache().hgetall(key) or {}
    # Ensure values are strings
    return {k.decode() if isinstance(k, bytes) else k:
            v.decode() if isinstance(v, bytes) else v
            for k, v in h.items()}


def _clear_other_sessions(user: str, keep_sid: str):
    # Drop all sessions for user except keep_sid
    frappe.db.sql("delete from `tabSessions` where user=%s and sid!=%s", (user, keep_sid))
    frappe.db.commit()


def _audit(user: str, action: str, detail: str):
    if not WRITE_AUDIT_LOG:
        return
    try:
        log = frappe.new_doc("User Log")
        log.user = user
        log.method = action
        log.device = detail[:140]
        log.ip_address = (_request_meta()[0] or "")[:140]
        log.save(ignore_permissions=True)
        frappe.db.commit()
    except Exception:
        frappe.log_error("Failed writing audit log", "ignitr_security")


def _should_enforce(user: str) -> bool:
    if not DEFAULT_ENFORCE:
        return False
    try:
        roles = set(frappe.get_roles(user))
        if roles & EXEMPT_ROLES:
            return False
    except Exception:
        pass
    return True


# ----------------- Hooks -----------------

def on_session_creation(login_manager):
    """
    Called at successful login. Bind this user to current fingerprint,
    and kill older sessions (if enabled).
    """
    user = frappe.session.user
    if user == "Guest" or not _should_enforce(user):
        return

    ip, ua = _request_meta()
    fp = _fingerprint(ip, ua)
    sid = frappe.session.sid

    if KICK_OLD_SESSIONS:
        _clear_other_sessions(user, sid)
        _audit(user, "ignitr_kick_old", f"Kept {sid}")

    _set_lock(user, sid, fp, ip, ua)
    _audit(user, "ignitr_bind", f"fp={fp[:8]} ip={ip} ua={_ua_family(ua)}")


def on_logout():
    """Clear lock if this session is the one recorded, so next login isn’t blocked."""
    user = frappe.session.user
    if user == "Guest":
        return
    try:
        key = _cache_key(user)
        rec = _get_lock(user)
        if rec and rec.get("sid") == frappe.session.sid:
            frappe.cache().delete(key)
            _audit(user, "ignitr_unbind", "logout")
    except Exception:
        pass


def before_request():
    """
    Guard that runs on every authenticated request.
    - If user's current SID isn’t the bound one → log out + 401.
    - If fingerprint changed beyond policy → log out + 401.
    """
    # Skip static, login route, and Guest
    if not getattr(frappe.local, "request", None):
        return
    if frappe.request.path.endswith((".js", ".css", ".png", ".jpg", ".svg", ".ico")):
        return
    if frappe.request.path.startswith("/api/method/login"):
        return

    user = getattr(frappe.session, "user", "Guest")
    if user == "Guest" or not _should_enforce(user):
        return

    sid = getattr(frappe.session, "sid", None)
    if not sid:
        return

    rec = _get_lock(user)
    if not rec:
        # No lock yet: create one on-the-fly (handles restored Redis)
        ip, ua = _request_meta()
        _set_lock(user, sid, _fingerprint(ip, ua), ip, ua)
        return

    # 1) Single active SID for this user
    if rec.get("sid") != sid:
        # This session has been superseded by a newer login.
        try:
            # Drop just this SID row, then raise 401
            frappe.db.sql("delete from `tabSessions` where sid=%s", sid)
            frappe.db.commit()
        except Exception:
            pass
        _audit(user, "ignitr_block", "superseded_by_new_login")
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = "/?session_expired=1"
        frappe.local.response["status_code"] = 401
        frappe.throw("You were logged out because your account signed in elsewhere.", frappe.PermissionError)

    # 2) Fingerprint continuity (same IP bucket + UA mode)
    ip, ua = _request_meta()
    current_fp = _fingerprint(ip, ua)
    if current_fp != rec.get("fp"):
        # Invalidate & force re-login. New login will take over and kick this one anyway.
        try:
            frappe.db.sql("delete from `tabSessions` where sid=%s", sid)
            frappe.db.commit()
        except Exception:
            pass
        _audit(user, "ignitr_block", f"fp_changed to {current_fp[:8]}")
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = "/?session_expired=1"
        frappe.local.response["status_code"] = 401
        frappe.throw("Your network or device changed. Please sign in again.", frappe.PermissionError)

def _should_enforce(user: str) -> bool:
    if frappe.conf.get("ignitr_single_session") is False:
        return False

def cleanup():
    """Optional daily tidy-up. Harmless if you skip scheduling."""
    # prune cache keys naturally via TTL; nothing required
    pass
