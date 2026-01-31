app_name = "ignitr_security"
app_title = "Ignitr Security"
app_publisher = "Ignitr"
app_description = "Single-session enforcement and device/IP binding"
app_email = "support@ignitr.cloud"
app_license = "mit"

# Session lifecycle hooks
on_session_creation = "ignitr_security.auth.on_session_creation"
on_logout           = "ignitr_security.auth.on_logout"

# Per-request guard (runs for authenticated routes)
before_request = "ignitr_security.auth.before_request"

# Optional: daily clean-up (stale locks / logs)
scheduler_events = {
    "daily": ["ignitr_security.auth.cleanup"]
}
