#!/bin/bash
# Script to replace self-signed certificate with Let's Encrypt certificate
# Run this once DNS is configured for agri-demo.nexelya.com
# Usage: sudo ./upgrade_agri_ssl_to_letsencrypt.sh

set -e

SITE="agri-demo.nexelya.com"
BENCH_DIR="/home/ubuntu/frappe-bench"

cd "$BENCH_DIR"

echo "Upgrading SSL certificate for $SITE to Let's Encrypt..."
echo "This requires DNS to be configured for $SITE"
echo ""

# Stop nginx temporarily
echo "Stopping nginx..."
systemctl stop nginx

# Generate Let's Encrypt certificate
echo "Generating Let's Encrypt certificate..."
certbot certonly --standalone \
    --non-interactive \
    --agree-tos \
    --email admin@nexelya.com \
    -d "$SITE" || {
    echo "Error: Failed to generate certificate. Check DNS configuration."
    systemctl start nginx
    exit 1
}

# Start nginx
echo "Starting nginx..."
systemctl start nginx

# Verify certificate
echo ""
echo "Certificate generated successfully!"
echo "Certificate location: /etc/letsencrypt/live/$SITE/"
echo ""
echo "The site_config.json and nginx.conf are already configured to use these paths."
echo "No further configuration needed - SSL is ready!"
