#!/bin/bash
#
# Script to complete nginx SSL setup (requires sudo)
# This should be run after update_nginx_ssl.sh
#
# Usage: sudo ./update_nginx_ssl_complete.sh

set -e

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

BENCH_DIR="/home/ubuntu/frappe-bench"
NGINX_CONF="$BENCH_DIR/config/nginx.conf"
NGINX_SITES_AVAILABLE="/etc/nginx/sites-available/frappe-bench"
NGINX_SITES_ENABLED="/etc/nginx/sites-enabled/frappe-bench"

echo "=== Completing nginx SSL setup ==="
echo ""

# Copy nginx config to system location
echo "Copying nginx configuration..."
cp "$NGINX_CONF" "$NGINX_SITES_AVAILABLE"

# Create symlink in sites-enabled
echo "Creating symlink in sites-enabled..."
ln -sf "$NGINX_SITES_AVAILABLE" "$NGINX_SITES_ENABLED"

# Remove default nginx site if it exists
if [ -f "/etc/nginx/sites-enabled/default" ]; then
    echo "Removing default nginx site..."
    rm -f /etc/nginx/sites-enabled/default
fi

# Test nginx configuration
echo ""
echo "Testing nginx configuration..."
nginx -t

# Reload nginx
echo ""
echo "Reloading nginx..."
systemctl reload nginx

echo ""
echo "=== Nginx SSL setup complete ==="
