#!/bin/bash
#
# Script to fix OCSP stapling configuration in nginx.conf
# This adds ssl_trusted_certificate for proper OCSP stapling verification
#
# Usage: sudo ./fix_nginx_ocsp.sh

set -e

BENCH_DIR="/home/ubuntu/frappe-bench"
NGINX_CONF="$BENCH_DIR/config/nginx.conf"

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

cd "$BENCH_DIR"

echo "=== Fixing OCSP stapling configuration ==="
echo ""

# Create backup
BACKUP_FILE="$NGINX_CONF.backup.$(date +%Y%m%d_%H%M%S)"
cp "$NGINX_CONF" "$BACKUP_FILE"
echo "Backup created: $BACKUP_FILE"

# Use Python to add ssl_trusted_certificate
python3 << 'PYTHON_SCRIPT'
import re
import sys

nginx_conf_path = '/home/ubuntu/frappe-bench/config/nginx.conf'

with open(nginx_conf_path, 'r') as f:
    lines = f.readlines()

# Process line by line
new_lines = []
i = 0
current_domain = None

while i < len(lines):
    line = lines[i]
    original_line = line
    
    # Track domain from ssl_certificate lines
    if 'ssl_certificate' in line and '/etc/letsencrypt/live/' in line:
        match = re.search(r'/etc/letsencrypt/live/([^/]+)/', line)
        if match:
            current_domain = match.group(1)
    
    new_lines.append(line.rstrip('\n'))
    
    # If we find ssl_stapling_verify on; followed by ssl_protocols
    if 'ssl_stapling_verify on;' in line and current_domain:
        # Check next line
        if i + 1 < len(lines) and 'ssl_protocols' in lines[i + 1]:
            # Check if ssl_trusted_certificate doesn't already exist (check last 15 lines)
            recent_context = '\n'.join(new_lines[-15:])
            if 'ssl_trusted_certificate' not in recent_context:
                # Add the line
                new_lines.append('\tssl_trusted_certificate /etc/letsencrypt/live/' + current_domain + '/chain.pem;')
    
    i += 1

new_content = '\n'.join(new_lines) + '\n'

# Check if content changed
with open(nginx_conf_path, 'r') as f:
    original_content = f.read()

if new_content != original_content:
    with open(nginx_conf_path, 'w') as f:
        f.write(new_content)
    print("OCSP stapling configuration updated successfully")
    sys.exit(0)
else:
    print("No changes needed (ssl_trusted_certificate may already be configured)")
    sys.exit(0)
PYTHON_SCRIPT

if [ $? -eq 0 ]; then
    echo ""
    echo "Testing nginx configuration..."
    nginx -t
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "Reloading nginx..."
        systemctl reload nginx
        echo ""
        echo "=== OCSP stapling fix complete ==="
        echo ""
        echo "The ssl_trusted_certificate directive has been added to SSL server blocks."
        echo ""
        echo "Note: If the browser still shows 'not secure', try:"
        echo "  1. Clear browser cache or use incognito/private mode"
        echo "  2. Check browser console for mixed content warnings (HTTP resources on HTTPS pages)"
        echo "  3. Wait a few minutes for OCSP stapling to populate"
    else
        echo ""
        echo "ERROR: Nginx configuration test failed!"
        echo "Restoring backup..."
        mv "$BACKUP_FILE" "$NGINX_CONF"
        echo "Backup restored. Please check the configuration manually."
        exit 1
    fi
else
    echo "ERROR: Failed to update configuration"
    exit 1
fi
