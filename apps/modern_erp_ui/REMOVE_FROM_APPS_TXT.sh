#!/bin/bash
# Script to remove modern_erp_ui from all apps.txt files
# Use this if the app isn't installed yet and causing errors

set -e

BENCH_PATH="${1:-$(pwd)}"
cd "$BENCH_PATH" || exit 1

echo "🗑️  Removing modern_erp_ui from all apps.txt files..."

# Remove from global apps.txt
if [ -f "sites/apps.txt" ]; then
    if grep -q "^modern_erp_ui$" "sites/apps.txt"; then
        sed -i '/^modern_erp_ui$/d' "sites/apps.txt"
        echo "✅ Removed from sites/apps.txt"
    else
        echo "ℹ️  Not found in sites/apps.txt"
    fi
fi

# Remove from all site-specific apps.txt files
FOUND=0
for site_file in sites/*/apps.txt; do
    if [ -f "$site_file" ] && grep -q "^modern_erp_ui$" "$site_file"; then
        sed -i '/^modern_erp_ui$/d' "$site_file"
        echo "✅ Removed from $site_file"
        FOUND=1
    fi
done

if [ $FOUND -eq 0 ]; then
    echo "ℹ️  Not found in any site-specific apps.txt files"
fi

echo "✅ Done! The app has been removed from all apps.txt files."
echo "You can re-add it later when the app is properly installed."

