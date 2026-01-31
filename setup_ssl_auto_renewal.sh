#!/bin/bash
#
# Script to set up automatic SSL certificate renewal with nginx reload
# This script should be run with sudo
#
# Usage: sudo ./setup_ssl_auto_renewal.sh

set -e

BENCH_DIR="/home/ubuntu/frappe-bench"

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

echo "=== Setting up automatic SSL certificate renewal ==="
echo ""

# Create renewal hook directories if they don't exist
mkdir -p /etc/letsencrypt/renewal-hooks/deploy
mkdir -p /etc/letsencrypt/renewal-hooks/post

# Create deploy hook to reload nginx after certificate renewal
cat > /etc/letsencrypt/renewal-hooks/deploy/reload-nginx.sh << 'EOF'
#!/bin/bash
# Reload nginx after certificate renewal

# Wait a moment for certificates to be written
sleep 2

# Test nginx configuration
if nginx -t >/dev/null 2>&1; then
    echo "Reloading nginx after certificate renewal..."
    systemctl reload nginx || systemctl restart nginx
    echo "Nginx reloaded successfully"
else
    echo "ERROR: Nginx configuration test failed. Not reloading nginx."
    exit 1
fi
EOF

chmod +x /etc/letsencrypt/renewal-hooks/deploy/reload-nginx.sh

# Create post hook to start nginx (in case it was stopped for standalone mode)
cat > /etc/letsencrypt/renewal-hooks/post/start-nginx.sh << 'EOF'
#!/bin/bash
# Start nginx after certificate renewal (in case it was stopped for standalone mode)

if ! systemctl is-active --quiet nginx; then
    echo "Starting nginx after certificate renewal..."
    systemctl start nginx
fi
EOF

chmod +x /etc/letsencrypt/renewal-hooks/post/start-nginx.sh

# Note: For standalone mode, certbot needs port 80/443, so nginx must be stopped
# The certbot service will handle this, but we need to ensure nginx starts after
# Since certbot runs with standalone mode, it handles stopping/starting nginx itself
# But our deploy hook will reload nginx after renewal completes

echo "Renewal hooks created:"
echo "  - /etc/letsencrypt/renewal-hooks/deploy/reload-nginx.sh (reloads nginx after renewal)"
echo "  - /etc/letsencrypt/renewal-hooks/post/start-nginx.sh (ensures nginx is running)"
echo ""

# Enable and check certbot timer
echo "Checking certbot timer..."
systemctl enable certbot.timer
systemctl start certbot.timer 2>/dev/null || true

# Show timer status
echo ""
echo "Certbot timer status:"
systemctl status certbot.timer --no-pager -l || true

echo ""
echo "=== Automatic renewal setup complete ==="
echo ""
echo "Certbot timer is configured to run twice daily."
echo "When certificates are renewed, nginx will be reloaded automatically."
echo ""
echo "NOTE: Since certificates use standalone mode, certbot will temporarily"
echo "      stop nginx during renewal, then start it again."
echo ""
echo "To test renewal manually (dry run):"
echo "  sudo certbot renew --dry-run"
echo ""
echo "To check next renewal time:"
echo "  sudo systemctl status certbot.timer"
echo ""
echo "To view certbot logs:"
echo "  sudo journalctl -u certbot.service -f"
