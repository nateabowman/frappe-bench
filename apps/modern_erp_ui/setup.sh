#!/bin/bash
# Setup script for Modern ERP UI app
# Run this from your frappe-bench directory

set -e

BENCH_PATH=$(pwd)
SITE_NAME="${1:-prod.nexelya.com}"

echo "🔧 Setting up Modern ERP UI..."

# Step 0: Verify app exists
if [ ! -d "apps/modern_erp_ui" ]; then
    echo "❌ Error: apps/modern_erp_ui directory not found!"
    echo "Please ensure the app is copied to ~/frappe-bench/apps/modern_erp_ui/"
    exit 1
fi

# Step 1: Add to site-specific apps.txt
SITE_APPS_FILE="sites/${SITE_NAME}/apps.txt"
if [ -f "$SITE_APPS_FILE" ]; then
    if ! grep -q "^modern_erp_ui$" "$SITE_APPS_FILE"; then
        echo "Adding modern_erp_ui to $SITE_APPS_FILE"
        echo "modern_erp_ui" >> "$SITE_APPS_FILE"
    else
        echo "modern_erp_ui already in $SITE_APPS_FILE"
    fi
else
    echo "⚠️  Site apps.txt not found at $SITE_APPS_FILE"
    echo "Creating it..."
    mkdir -p "sites/${SITE_NAME}"
    echo "modern_erp_ui" > "$SITE_APPS_FILE"
fi

# Step 2: Clear Python cache
echo "Clearing Python cache..."
find apps/modern_erp_ui -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
find apps/modern_erp_ui -name "*.pyc" -delete 2>/dev/null || true

# Step 3: Clear Frappe cache
echo "Clearing Frappe cache..."
bench --site "$SITE_NAME" clear-cache 2>/dev/null || true

# Step 4: Install the app
echo "Installing modern_erp_ui..."
bench --site "$SITE_NAME" install-app modern_erp_ui

# Step 5: Build assets
echo "Building assets..."
bench build --app modern_erp_ui

echo "✅ Setup complete! Restart your bench with: bench restart"

