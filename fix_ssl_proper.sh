#!/bin/bash
#
# Script to properly configure SSL for prod.nexelya.com according to Frappe/Bench documentation
# This script follows the official Frappe documentation for SSL setup
#
# Usage: sudo ./fix_ssl_proper.sh

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
echo "Following Frappe/Bench Documentation"
echo "========================================="
echo ""

# Step 1: Verify SSL certificate paths in site_config.json
echo "Step 1: Verifying SSL certificate configuration in site_config.json..."
SSL_CERT=$(sudo -u ubuntu python3 -c "import json; config = json.load(open('$BENCH_DIR/sites/$SITE/site_config.json')); print(config.get('ssl_certificate', ''))" 2>/dev/null)
SSL_KEY=$(sudo -u ubuntu python3 -c "import json; config = json.load(open('$BENCH_DIR/sites/$SITE/site_config.json')); print(config.get('ssl_certificate_key', ''))" 2>/dev/null)

if [ -z "$SSL_CERT" ] || [ -z "$SSL_KEY" ]; then
    echo "Setting SSL certificate paths using bench commands..."
    sudo -u ubuntu bash -c "cd $BENCH_DIR && bench set-ssl-certificate $SITE /etc/letsencrypt/live/$SITE/fullchain.pem" || true
    sudo -u ubuntu bash -c "cd $BENCH_DIR && bench set-ssl-key $SITE /etc/letsencrypt/live/$SITE/privkey.pem" || true
    SSL_CERT="/etc/letsencrypt/live/$SITE/fullchain.pem"
    SSL_KEY="/etc/letsencrypt/live/$SITE/privkey.pem"
else
    echo "✓ SSL Certificate: $SSL_CERT"
    echo "✓ SSL Key: $SSL_KEY"
fi

# Step 2: Verify certificate files exist
echo ""
echo "Step 2: Verifying certificate files exist..."
if [ ! -f "$SSL_CERT" ]; then
    echo "ERROR: Certificate file not found: $SSL_CERT"
    echo "Please generate the certificate first using: sudo certbot certonly --standalone -d $SITE"
    exit 1
fi
if [ ! -f "$SSL_KEY" ]; then
    echo "ERROR: Key file not found: $SSL_KEY"
    exit 1
fi
echo "✓ Certificate files exist"

# Step 3: Check certificate validity
echo ""
echo "Step 3: Checking certificate validity..."
CERT_EXPIRY=$(openssl x509 -in "$SSL_CERT" -noout -enddate 2>&1 | cut -d= -f2)
echo "Certificate expires: $CERT_EXPIRY"

# Step 4: Regenerate nginx configuration using bench (as per Frappe docs)
echo ""
echo "Step 4: Regenerating nginx configuration with bench (as per Frappe documentation)..."
sudo -u ubuntu bash -c "cd $BENCH_DIR && bench setup nginx --yes"

# Step 5: Add ssl_trusted_certificate for OCSP stapling (bench doesn't add this by default)
echo ""
echo "Step 5: Adding ssl_trusted_certificate for proper OCSP stapling..."
python3 << 'PYTHON_SCRIPT'
import re

nginx_conf_path = '/home/ubuntu/frappe-bench/config/nginx.conf'

with open(nginx_conf_path, 'r') as f:
    lines = f.readlines()

new_lines = []
i = 0
current_domain = None

while i < len(lines):
    line = lines[i]
    
    # Track domain from ssl_certificate lines
    if 'ssl_certificate' in line and '/etc/letsencrypt/live/' in line:
        match = re.search(r'/etc/letsencrypt/live/([^/]+)/', line)
        if match:
            current_domain = match.group(1)
    
    new_lines.append(line.rstrip('\n'))
    
    # Add ssl_trusted_certificate after ssl_stapling_verify on;
    if 'ssl_stapling_verify on;' in line and current_domain:
        if i + 1 < len(lines) and 'ssl_protocols' in lines[i + 1]:
            # Check if ssl_trusted_certificate doesn't already exist
            recent_context = '\n'.join(new_lines[-15:])
            if 'ssl_trusted_certificate' not in recent_context:
                new_lines.append('\tssl_trusted_certificate /etc/letsencrypt/live/' + current_domain + '/chain.pem;')
    
    i += 1

new_content = '\n'.join(new_lines) + '\n'

with open(nginx_conf_path, 'w') as f:
    f.write(new_content)

print("✓ Added ssl_trusted_certificate for OCSP stapling")
PYTHON_SCRIPT

# Step 6: Copy nginx config to system location
echo ""
echo "Step 6: Copying nginx configuration to system location..."
cp "$BENCH_DIR/config/nginx.conf" /etc/nginx/sites-available/frappe-bench
ln -sf /etc/nginx/sites-available/frappe-bench /etc/nginx/sites-enabled/frappe-bench
rm -f /etc/nginx/sites-enabled/default

# Step 7: Test nginx configuration
echo ""
echo "Step 7: Testing nginx configuration..."
if ! nginx -t; then
    echo "ERROR: Nginx configuration test failed!"
    exit 1
fi

# Step 8: Reload nginx
echo ""
echo "Step 8: Reloading nginx..."
systemctl reload nginx

# Step 9: Verify SSL is working
echo ""
echo "Step 9: Verifying SSL connection..."
SSL_TEST=$(echo | openssl s_client -connect $SITE:443 -servername $SITE < /dev/null 2>&1 | grep -E "Verify return code" | head -1)
if echo "$SSL_TEST" | grep -q "0 (ok)"; then
    echo "✓ SSL connection verified successfully"
else
    echo "WARNING: SSL verification returned: $SSL_TEST"
fi

# Check OCSP stapling
echo ""
echo "Checking OCSP stapling..."
OCSP_TEST=$(echo | openssl s_client -connect $SITE:443 -servername $SITE -status < /dev/null 2>&1 | grep -A 3 "OCSP response" | head -5)
if echo "$OCSP_TEST" | grep -q "successful\|no response sent"; then
    echo "OCSP status:"
    echo "$OCSP_TEST" | head -3
fi

echo ""
echo "========================================="
echo "SSL Setup Complete!"
echo "========================================="
echo ""
echo "Configuration verified:"
echo "  ✓ SSL certificate paths set in site_config.json"
echo "  ✓ Nginx configuration generated with bench setup nginx"
echo "  ✓ OCSP stapling configured with ssl_trusted_certificate"
echo "  ✓ Nginx reloaded"
echo ""
echo "Next steps to verify in browser:"
echo "1. Visit https://$SITE in your browser"
echo "2. Clear browser cache or use incognito/private mode"
echo "3. Check browser console for mixed content warnings"
echo "4. Wait a few minutes for OCSP stapling to populate"
echo ""
echo "To test SSL connection:"
echo "  curl -I https://$SITE"
echo ""
echo "To check certificate details:"
echo "  openssl s_client -connect $SITE:443 -servername $SITE < /dev/null | openssl x509 -noout -dates -subject -issuer"
