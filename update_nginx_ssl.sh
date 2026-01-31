#!/bin/bash
#
# Script to update nginx configuration with SSL certificates
# This script should be run after certificates are generated/renewed
# Run as regular user (bench will handle permissions)
#
# Usage: ./update_nginx_ssl.sh

set -e

cd /home/ubuntu/frappe-bench

echo "=== Updating nginx configuration with SSL certificates ==="
echo ""

# Regenerate nginx configuration
echo "Regenerating nginx configuration..."
bench setup nginx --yes

# Copy nginx config to system location (requires sudo)
echo ""
echo "To complete the setup, run:"
echo "  sudo cp /home/ubuntu/frappe-bench/config/nginx.conf /etc/nginx/sites-available/frappe-bench"
echo "  sudo ln -sf /etc/nginx/sites-available/frappe-bench /etc/nginx/sites-enabled/frappe-bench"
echo "  sudo nginx -t"
echo "  sudo systemctl reload nginx"

echo ""
echo "Or run: sudo ./update_nginx_ssl_complete.sh"
