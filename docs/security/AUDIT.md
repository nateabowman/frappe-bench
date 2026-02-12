# Security Audit Summary

This bench has undergone security review. Key findings and recommendations:

## Recommendations

1. **SQL injection** – Ensure all database queries use parameterized queries, not string interpolation.
2. **ignore_permissions** – Review usage of `ignore_permissions=True`; use only where necessary with explicit validation.
3. **Command execution** – Validate and sanitize any user input passed to shell commands.
4. **Secrets** – Never commit `site_config.json`, `common_site_config.json`, or any file containing passwords or API keys.
5. **Redis** – If exposed beyond localhost, enable Redis authentication.
6. **Drive JWT** – Treat shared links as secrets; rotate JWT key if compromised.

## Applied Fixes

- Site configs excluded from version control (`.gitignore`)
- Archived sites and deployment configs excluded from git
- Redis bound to localhost when auth not used
- Security headers in nginx (HSTS, X-Frame-Options, etc.)

## Reporting Vulnerabilities

See [SECURITY.md](../SECURITY.md) in the repository root for how to report security issues.
