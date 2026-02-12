# Log Clearing Setup

## What was configured

### 1. Immediate log clear (completed)
- All bench logs truncated (`/home/ubuntu/frappe-bench/logs/`)
- All site logs truncated (`sites/*/logs/`)
- Nginx logs cleared (`/var/log/nginx/`)

### 2. Manual clear script
Run anytime to clear log files:
```bash
sudo /path/to/frappe-bench/scripts/clear_logs.sh
```

### 3. Logrotate (auto file log rotation)
- **Config:** `/etc/logrotate.d/frappe-bench`
- **Schedule:** Daily (via systemd timer or cron)
- **Retention:** 7 days of rotated logs
- **Behavior:** Rotates and compresses logs; uses `copytruncate` so processes keep writing

### 4. Frappe Log Settings (auto DB log clear)
- **Schedule:** Daily via Frappe scheduler (`run_log_clean_up`)
- **Clears:** Error Log, Activity Log, Email Queue, Scheduled Job Log, Route History
- **Configure:** Setup > Log Settings in the Frappe UI to adjust retention days per log type

## Security note

Change default passwords after setup. Do not share passwords in plain text.
