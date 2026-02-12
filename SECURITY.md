# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly.

**Do not** open a public GitHub issue for security vulnerabilities.

Instead:

1. Email the maintainers with details of the vulnerability
2. Include steps to reproduce, if possible
3. Allow reasonable time for a fix before public disclosure

## What We Consider Sensitive

- Database passwords and connection strings
- API keys and tokens
- Encryption keys
- Session secrets
- Any credentials stored in `sites/*/site_config.json` or `sites/common_site_config.json`

## Safe Practices

- Never commit `site_config.json` or `common_site_config.json`
- Never commit `config/nginx.conf` or `config/supervisor.conf` with real domains/paths
- Use environment variables or secrets managers for production credentials
- Keep Redis bound to localhost unless properly secured
- Rotate credentials if they may have been exposed
