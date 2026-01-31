#!/bin/bash
#
# Wrapper script for certbot renewal that handles nginx with standalone mode
# This is used by the certbot systemd service
#
# Usage: This is called by systemd, not directly

set -e

# For standalone mode, nginx must be stopped during renewal
# Since certbot's service doesn't handle this automatically, we need to do it here

# Stop nginx before renewal (needed for standalone mode)
echo "Stopping nginx for certificate renewal..."
systemctl stop nginx || true

# Run certbot renewal
/usr/bin/certbot -q renew --no-random-sleep-on-renew

# Start nginx after renewal
echo "Starting nginx after certificate renewal..."
systemctl start nginx
