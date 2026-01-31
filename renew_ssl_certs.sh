#!/bin/bash
#
# Script to renew/generate SSL certificates for all bench sites
# This script should be run with sudo
#
# Usage: sudo ./renew_ssl_certs.sh

set -e

BENCH_DIR="/home/ubuntu/frappe-bench"
SITES=("apps.heinigesons.com" "apps.nolagg.com" "dev.ignitr.cloud" "prod.nexelya.com")

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

echo "=== Renewing/Generating SSL certificates for bench sites ==="
echo ""

# Function to check if certificate exists and is valid
check_cert_exists() {
    local domain=$1
    if [ -f "/etc/letsencrypt/live/$domain/cert.pem" ]; then
        # Check expiration date
        local expiry=$(openssl x509 -in /etc/letsencrypt/live/$domain/cert.pem -noout -enddate 2>/dev/null | cut -d= -f2)
        local expiry_epoch=$(date -d "$expiry" +%s 2>/dev/null || date -d "$expiry" +%s 2>/dev/null)
        local now_epoch=$(date +%s)
        local days_left=$(( ($expiry_epoch - $now_epoch) / 86400 ))
        
        if [ $days_left -gt 0 ]; then
            echo "Certificate for $domain exists and expires in $days_left days"
            return 0
        else
            echo "Certificate for $domain has expired"
            return 1
        fi
    else
        echo "Certificate for $domain does not exist"
        return 1
    fi
}

# Stop nginx temporarily for standalone mode (certbot needs port 80/443)
echo "Stopping nginx..."
systemctl stop nginx || true

# Process each site
for site in "${SITES[@]}"; do
    echo ""
    echo "=== Processing $site ==="
    
    if check_cert_exists "$site"; then
        # Renew existing certificate
        echo "Renewing certificate for $site..."
        certbot certonly --standalone \
            --non-interactive \
            --agree-tos \
            --email admin@$(echo $site | cut -d. -f2-3) \
            -d "$site" \
            --force-renewal \
            --keep-until-expiring || {
            echo "Warning: Renewal failed for $site, trying to obtain new certificate..."
            certbot certonly --standalone \
                --non-interactive \
                --agree-tos \
                --email admin@$(echo $site | cut -d. -f2-3) \
                -d "$site" || echo "Error: Failed to obtain certificate for $site"
        }
    else
        # Generate new certificate
        echo "Generating new certificate for $site..."
        certbot certonly --standalone \
            --non-interactive \
            --agree-tos \
            --email admin@$(echo $site | cut -d. -f2-3) \
            -d "$site" || echo "Error: Failed to obtain certificate for $site"
    fi
done

# Start nginx
echo ""
echo "Starting nginx..."
systemctl start nginx

echo ""
echo "=== Certificate renewal/generation complete ==="
echo ""
echo "Next steps:"
echo "1. Run: cd $BENCH_DIR && bench setup nginx --yes"
echo "2. Test nginx config: sudo nginx -t"
echo "3. Reload nginx: sudo systemctl reload nginx"
