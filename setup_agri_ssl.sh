#!/bin/bash
# Script to set up SSL for agri-demo.nexelya.com
# This script should be run with sudo

set -e

SITE="agri-demo.nexelya.com"
BENCH_DIR="/home/ubuntu/frappe-bench"

cd "$BENCH_DIR"

echo "Setting up SSL for $SITE..."

# Generate SSL certificate
echo "Generating SSL certificate..."
certbot certonly --standalone \
    --non-interactive \
    --agree-tos \
    --email admin@nexelya.com \
    -d "$SITE" || {
    echo "Warning: Certificate generation may have failed or certificate already exists"
}

# Update site config with SSL paths
echo "Updating site configuration..."
bench set-ssl-certificate "$SITE" /etc/letsencrypt/live/"$SITE"/fullchain.pem || true
bench set-ssl-key "$SITE" /etc/letsencrypt/live/"$SITE"/privkey.pem || true

# Regenerate nginx config
echo "Regenerating nginx configuration..."
bench setup nginx --yes

echo "SSL setup complete for $SITE"
echo "Next: sudo cp $BENCH_DIR/config/nginx.conf /etc/nginx/sites-available/frappe-bench"
echo "      sudo nginx -t"
echo "      sudo systemctl reload nginx"
