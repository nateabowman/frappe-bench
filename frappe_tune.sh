#!/bin/bash

# Auto-tune Frappe Gunicorn and worker settings

# Check we're in a bench dir
if [ ! -d sites ] || [ ! -d apps ]; then
  echo "❌ You must run this from your frappe-bench directory."
  exit 1
fi

SITE="prod.ignitr.cloud"

# Get CPU + RAM info
CORES=$(nproc)
RAM_GB=$(free -g | awk '/^Mem:/{print $2}')
GUNICORN_WORKERS=$(( CORES * 2 + 1 ))
REDIS_WORKERS=$(( CORES / 2 ))

echo "🧠 Detected:"
echo " - Logical Cores : $CORES"
echo " - Total RAM      : ${RAM_GB} GB"
echo " - Gunicorn Workers: $GUNICORN_WORKERS"
echo " - Redis Queue Workers: $REDIS_WORKERS"
echo ""

read -p "➡️ Apply these settings to site $SITE? (y/n): " confirm
if [[ $confirm != "y" ]]; then
  echo "❌ Cancelled."
  exit 0
fi

# Set gunicorn workers
bench --site "$SITE" set-config gunicorn_workers "$GUNICORN_WORKERS"

# Set redis and background workers in common_site_config.json
bench set-config redis_queue_workers "$REDIS_WORKERS"
bench set-config redis_socketio_workers "$REDIS_WORKERS"

# Optional: Set max-requests to recycle Gunicorns for memory leaks
bench --site "$SITE" set-config gunicorn_max_requests 5000
bench --site "$SITE" set-config gunicorn_max_requests_jitter 500

# Restart bench
bench restart

echo ""
echo "✅ All settings applied!"
