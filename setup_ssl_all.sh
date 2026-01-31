#!/bin/bash
#
# Master script to set up SSL certificates for all bench sites
# This script orchestrates the entire SSL setup process
#
# Usage: sudo ./setup_ssl_all.sh
#
# This script will:
# 1. Generate/renew SSL certificates for all sites
# 2. Update nginx configuration
# 3. Set up automatic renewal

set -e

BENCH_DIR="/home/ubuntu/frappe-bench"

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

cd "$BENCH_DIR"

echo "========================================="
echo "SSL Certificate Setup for Bench Sites"
echo "========================================="
echo ""

# Step 1: Generate/Renew certificates
echo "Step 1: Generating/Renewing SSL certificates..."
./renew_ssl_certs.sh

echo ""
echo "Step 2: Updating nginx configuration..."

# Run bench setup nginx as ubuntu user (bench commands should run as the bench owner)
cd "$BENCH_DIR"
sudo -u ubuntu bash -c "cd $BENCH_DIR && bench setup nginx --yes" || {
    echo "Warning: Failed to run bench setup nginx as ubuntu user"
    echo "You may need to run manually: cd $BENCH_DIR && bench setup nginx --yes"
}

# Copy nginx config to system location
echo "Copying nginx configuration..."
cp "$BENCH_DIR/config/nginx.conf" /etc/nginx/sites-available/frappe-bench
ln -sf /etc/nginx/sites-available/frappe-bench /etc/nginx/sites-enabled/frappe-bench
rm -f /etc/nginx/sites-enabled/default

# Test nginx configuration
echo "Testing nginx configuration..."
nginx -t

# Reload nginx
echo "Reloading nginx..."
systemctl reload nginx

echo ""
echo "Step 3: Setting up automatic renewal..."
./setup_ssl_auto_renewal.sh

echo ""
echo "========================================="
echo "SSL Setup Complete!"
echo "========================================="
echo ""
echo "Certificates have been generated/renewed for:"
echo "  - apps.heinigesons.com"
echo "  - apps.nolagg.com"
echo "  - dev.ignitr.cloud"
echo "  - prod.nexelya.com"
echo ""
echo "Automatic renewal is configured and will run twice daily."
echo "Certificates will be renewed automatically when they have 30 days or less remaining."
echo ""
echo "To check certificate status:"
echo "  sudo certbot certificates"
echo ""
echo "To test renewal (dry run):"
echo "  sudo certbot renew --dry-run"
