# Frappe Bench – Multi-Tenant SaaS Stack

A [Frappe](https://frappeframework.com/) bench for multi-tenant ERP deployments with ERPNext, HRMS, CRM, Agriculture, Construction, and integrations.

## Overview

This repository contains:

- **Frappe** – Core framework
- **ERPNext** – ERP application
- **HRMS** – HR and payroll
- **CRM** – Customer relationship management
- **Agriculture** – Agriculture management
- **Construction** – Construction project management
- **Integrations** – Twilio (voice/SMS), Drive, Insights, Gameplan, Payments, and more

## Architecture

- **Multi-tenant** – Single bench, multiple sites (one database per site)
- **Isolation** – Per-site databases, files, and Redis namespacing
- **Deployment** – Nginx, Supervisor, Redis, MariaDB

See [docs/architecture/OVERVIEW.md](docs/architecture/OVERVIEW.md) for technical details.

## Quick Start

### Prerequisites

- Ubuntu/Debian (or compatible)
- Python 3.10+
- Node.js 18+
- MariaDB 10.6+
- Redis

### Installation

```bash
# Clone and setup (customize as needed)
bench init frappe-bench --frappe-branch version-15
cd frappe-bench
bench get-app erpnext
bench new-site your-site.com
bench --site your-site.com install-app erpnext
```

### Development

```bash
bench start
```

### Production

- Use Supervisor or systemd for process management
- See `config/supervisor.example.conf` and `config/nginx.example.conf`
- Copy to `supervisor.conf` / `nginx.conf` and customize paths and domains

## Documentation

| Topic | Location |
|-------|----------|
| **Full docs index** | [docs/INDEX.md](docs/INDEX.md) |
| Architecture | [docs/architecture/](docs/architecture/) |
| Administration | [docs/administration/](docs/administration/) |
| Deployment | [docs/deployment/](docs/deployment/) |
| Security | [docs/security/](docs/security/) |
| Features | [docs/features/](docs/features/) |

### Main Scripts

| Script | Purpose |
|--------|---------|
| `refresh.sh` | Maintenance: backup, migrate, clear-cache, build, restart |
| `saas_admin.sh` | Health checks, metrics, cleanup, SSL verification |

## Security

- **Secrets** – `sites/*/site_config.json` and `sites/common_site_config.json` are not in git
- **Deployment configs** – `config/nginx.conf` and `config/supervisor.conf` are gitignored; use the `.example` files as templates
- **Reporting issues** – See [SECURITY.md](SECURITY.md)

## License

Components have their own licenses (Frappe, ERPNext, etc.). Check each app’s license file.

## Links

- [Frappe Framework](https://frappeframework.com/)
- [ERPNext](https://erpnext.com/)
- [Frappe Bench Docs](https://frappeframework.com/docs/user/en/installation)
