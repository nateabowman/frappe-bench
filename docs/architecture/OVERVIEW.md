# Technical Overview

## What is Frappe Bench?

[Frappe](https://frappeframework.com/) is a full-stack Python/JavaScript web framework. A **bench** is a directory containing:

- **frappe** – Core framework
- **ERPNext** – ERP application (optional)
- Custom apps – Extensions and integrations
- **Sites** – Each site is a tenant with its own database and files

## Architecture

```
frappe-bench/
├── apps/                 # Application code (frappe, erpnext, custom apps)
├── sites/                # Site data (one directory per site/tenant)
│   ├── common_site_config.json   # Shared config (not in git)
│   ├── apps.json         # Installed app versions
│   ├── apps.txt          # App list
│   └── <site-name>/      # Per-site: config, files, backups
├── config/               # Nginx, Supervisor, Redis configs
├── logs/                 # Application logs
├── env/                  # Python virtual environment
├── Procfile              # Process definitions (web, workers, schedule)
├── bench.toml            # Bench configuration
├── refresh.sh            # Maintenance script
└── saas_admin.sh         # SaaS administration script
```

## Key Components

| Component | Purpose |
|-----------|---------|
| **Gunicorn** | WSGI web server (port 8000) |
| **Node SocketIO** | Real-time WebSocket server (port 9000) |
| **Redis** | Cache (13000) and job queue (11000) |
| **MariaDB** | Database (one per site) |
| **Supervisor** | Process manager for all services |
| **Nginx** | Reverse proxy and static file serving |

## Multi-Tenancy Model

- **Single bench, multiple sites** – Each site has its own database; code and workers are shared.
- **Data isolation** – Files and DB are per-site; Redis keys are namespaced.
- See [Multi-Tenancy Guide](MULTI_TENANCY_GUIDE.md) for details.

## Installed Apps (Typical Stack)

- **frappe** – Framework
- **erpnext** – ERP
- **hrms** – HR & Payroll
- **crm** – CRM
- **agriculture** – Agriculture management
- **construction** – Construction management
- **drive** – File management
- **insights** – Analytics
- **gameplan** – Project management
- **twilio_integration** – Voice/SMS
- **whitelabel** / **ignitr_brand** – Branding
- **payments** / **payments_processor** – Payments
- Plus: sheets, toolbox, next_ai, frappe_tinymce, desk_navbar_extended, frappe_desk_theme, ignitr_security

## Processes (Procfile)

- `web` – Bench serve (Gunicorn)
- `socketio` – Node.js SocketIO server
- `watch` – Asset watcher (development)
- `schedule` – Cron/scheduler
- `worker` – Background job worker
- `redis_cache` / `redis_queue` – Redis instances
