# Security Recommendations

Ongoing recommendations for this bench. Apply where appropriate for your environment.

## Redis authentication

**Current:** `sites/common_site_config.json` has `"use_redis_auth": false`.

**Recommendation:** If Redis is bound to anything other than localhost, or you want defense in depth:

1. Configure a password in your Redis config (`config/redis_cache.conf`, `config/redis_queue.conf`).
2. Set `"use_redis_auth": true` in `sites/common_site_config.json`.
3. Add the Redis password to `sites/common_site_config.json` (e.g. in the redis URL or the key used by Frappe for Redis auth).

Until then, keep Redis bound to `127.0.0.1` only so it is not network-accessible.

## Site config and secrets

- `sites/*/site_config.json` and `sites/common_site_config.json` contain secrets (DB passwords, encryption keys). They are in `.gitignore`; keep them out of version control.
- File permissions have been set to `600` (owner read/write only) on these config files. Preserve these permissions after edits.

## Drive JWT sharing

The Drive app uses JWT tokens for unauthenticated file access (shared links). JWTs are validated (signature and expiry). Treat shared links as secret; rotate the JWT key in Drive Site Settings if a link is compromised.
