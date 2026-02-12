# Deployment Configuration

## Config Files

| File | Purpose | In Git |
|------|---------|--------|
| `config/nginx.example.conf` | Nginx template | Yes |
| `config/supervisor.example.conf` | Supervisor template | Yes |
| `config/nginx.conf` | Actual nginx config | No (deployment-specific) |
| `config/supervisor.conf` | Actual supervisor config | No (deployment-specific) |
| `sites/common_site_config.json` | Shared site config | No (secrets) |
| `sites/*/site_config.json` | Per-site config | No (secrets) |

## Setup

1. Copy example configs and customize:
   ```bash
   cp config/nginx.example.conf config/nginx.conf
   cp config/supervisor.example.conf config/supervisor.conf
   # Edit and replace placeholders (paths, domains, user)
   ```

2. Install and symlink nginx config:
   ```bash
   sudo cp config/nginx.conf /etc/nginx/sites-available/frappe-bench
   sudo ln -sf /etc/nginx/sites-available/frappe-bench /etc/nginx/sites-enabled/
   sudo nginx -t && sudo systemctl reload nginx
   ```

3. Supervisor (if not using `bench start`):
   ```bash
   sudo cp config/supervisor.conf /etc/supervisor/conf.d/frappe-bench.conf
   sudo supervisorctl reread && sudo supervisorctl update
   ```

## Environment Variables

Scripts respect these environment variables:

| Variable | Purpose | Default |
|----------|---------|---------|
| `ALERT_EMAIL` | Email for disk/health alerts | (none) |
| `DISK_WARNING_PERCENT` | Disk usage warning threshold | 80 |
| `DISK_CRITICAL_PERCENT` | Disk usage critical threshold | 90 |
| `MEMORY_WARNING_PERCENT` | Memory warning threshold | 80 |
