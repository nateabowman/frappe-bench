#!/bin/bash
# Clear all Frappe bench and site log files by truncating (keeps files for running processes)
set -e
shopt -s nullglob

BENCH_ROOT="/home/ubuntu/frappe-bench"
echo "Clearing bench logs..."

# Bench-level logs
for f in "$BENCH_ROOT"/logs/*.log "$BENCH_ROOT"/logs/*.error.log; do
    [ -f "$f" ] && : > "$f" && echo "  Cleared: $f"
done

# Site-level logs
for site_dir in "$BENCH_ROOT"/sites/*/; do
    if [ -d "${site_dir}logs" ]; then
        for f in "${site_dir}"logs/*.log; do
            [ -f "$f" ] && : > "$f" && echo "  Cleared: $f"
        done
    fi
done

# Remove old rotated log files (free disk space)
find "$BENCH_ROOT"/logs -name "*.log.*" -type f -delete 2>/dev/null || true

echo "Bench log clearing done."
