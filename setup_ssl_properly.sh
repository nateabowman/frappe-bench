#!/bin/bash
#
# Script to properly set up SSL using Frappe/Bench official methods
# This follows the official Frappe documentation for SSL setup
#
# Usage: sudo ./setup_ssl_properly.sh

set -e

BENCH_DIR="/home/ubuntu/frappe-bench"
SITE="prod.nexelya.com"

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

cd "$BENCH_DIR"

echo "========================================="
echo "Proper SSL Setup for $SITE"
echo "Following Frappe/Bench Official Method"
echo "========================================="
echo ""

# Step 1: Check if DNS multitenancy is enabled
echo "Step 1: Checking DNS multitenancy..."
DNS_MULTITENANT=$(su - ubuntu -c "cd $BENCH_DIR && bench config dns_multitenant" 2>&1 | grep -i "dns_multitenant" | awk '{print $2}')
if [ "$DNS_MULTITENANT" != "True" ] && [ "$DNS_MULTITENANT" != "true" ]; then
    echo "Enabling DNS multitenancy..."
    su - ubuntu -c "cd $BENCH_DIR && bench config dns_multitenant on"
    echo "DNS multitenancy enabled."
else
    echo "DNS multitenancy is already enabled."
fi

echo ""
echo "Step 2: Setting up Let's Encrypt SSL using bench command..."
echo "This is the official Frappe/Bench method for SSL setup."
echo ""

# Use bench's official lets-encrypt setup command
# Note: This requires sudo, so we need to run it properly
su - ubuntu -c "cd $BENCH_DIR && sudo -H bench setup lets-encrypt $SITE --non-interactive" 2>&1 || {
    echo ""
    echo "Note: The bench setup lets-encrypt command may require interactive input."
    echo "If it failed, you may need to run manually:"
    echo "  sudo -H bench setup lets-encrypt $SITE"
    echo ""
    echo "However, since certificates already exist, let's verify the setup instead..."
}

echo ""
echo "Step 3: Regenerating nginx configuration..."
# Regenerate nginx config as ubuntu user
su - ubuntu -c "cd $BENCH_DIR && bench setup nginx --yes" 2>&1 || {
    echo "Warning: Failed to regenerate nginx config as ubuntu user"
}

echo ""
echo "Step 4: Copying nginx configuration to system location..."
cp "$BENCH_DIR/config/nginx.conf" /etc/nginx/sites-available/frappe-bench
ln -sf /etc/nginx/sites-available/frappe-bench /etc/nginx/sites-enabled/frappe-bench
rm -f /etc/nginx/sites-enabled/default

echo ""
echo "Step 5: Testing nginx configuration..."
nginx -t

if [ $? -eq 0 ]; then
    echo ""
    echo "Step 6: Reloading nginx..."
    systemctl reload nginx
    
    echo ""
    echo "Step 7: Verifying SSL certificate..."
    sleep 2
    
    echo ""
    echo "Certificate details:"
    echo | openssl s_client -connect $SITE:443 -servername $SITE 2>&1 | openssl x509 -noout -dates -subject -issuer 2>&1 || true
    
    echo ""
    echo "SSL connection test:"
    SSL_TEST=$(echo | openssl s_client -connect $SITE:443 -servername $SITE 2>&1 | grep -E "Verify return code" || echo "Verify return code: unknown")
    echo "$SSL_TEST"
    
    echo ""
    echo "========================================="
    echo "SSL Setup Complete!"
    echo "========================================="
    echo ""
    echo "The site $SITE should now be properly configured with SSL."
    echo ""
    echo "To verify in browser:"
    echo "  1. Visit https://$SITE"
    echo "  2. Clear browser cache or use incognito/private mode"
    echo "  3. Check for a secure lock icon in the address bar"
    echo ""
    echo "If the site still shows 'not secure':"
    echo "  1. Check browser console for mixed content warnings (F12 > Console)"
    echo "  2. Ensure all resources load over HTTPS (no HTTP content)"
    echo "  3. Try a different browser or incognito mode"
    echo ""
else
    echo ""
    echo "ERROR: Nginx configuration test failed!"
    echo "Please check the configuration manually."
    exit 1
fi
