# Documentation Index

Technical documentation for this Frappe Bench deployment.

## Architecture

- [Multi-Tenancy Guide](architecture/MULTI_TENANCY_GUIDE.md) – Single bench vs multiple benches, site isolation, scaling
- [Technical Overview](architecture/OVERVIEW.md) – System architecture and components

## Administration

- [SaaS Administration](administration/SAAS_ADMINISTRATION.md) – `saas_admin.sh` usage and features
- [Quick Reference](administration/QUICK_REFERENCE.md) – Common commands and workflows
- [Log Cleanup](administration/LOG_CLEANUP.md) – Log rotation and cleanup

## Deployment

- [SSL Setup](deployment/SSL_SETUP.md) – SSL certificates with Let's Encrypt
- [Configuration](deployment/CONFIGURATION.md) – Nginx, Supervisor, and environment setup

## Security

- [Security Recommendations](security/RECOMMENDATIONS.md) – Redis auth, secrets, best practices
- [Security Audit](security/AUDIT.md) – Audit findings and hardening

## Features & Customizations

- [Agriculture Demo](features/AGRICULTURE_DEMO.md) – Agriculture app setup
- [Business Hours](features/BUSINESS_HOURS.md) – Business hours configuration
- [Phone / Twilio](features/PHONE_ATTENDANT.md) – Twilio integration and phone attendant
- [Premium Addons](features/PREMIUM_ADDONS.md) – Premium feature implementation
- [UI/UX Overhaul](features/UI_UX_OVERHAUL.md) – UI/UX improvements
- [Branding](features/BRANDING.md) – Rebranding and whitelabel

## Implementation Notes

- [Security Fixes Summary](implementation/SECURITY_FIXES_SUMMARY.md)
- [Final Implementation Summary](implementation/FINAL_IMPLEMENTATION_SUMMARY.md)

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `refresh.sh` | Full maintenance: backup, migrate, clear-cache, build, restart |
| `saas_admin.sh` | Health checks, metrics, cleanup, SSL verification |
| `renew_ssl_certs.sh` | Renew Let's Encrypt certificates |
| `scripts/clear_logs.sh` | Clear application and nginx logs |
