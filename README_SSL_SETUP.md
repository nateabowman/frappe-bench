# SSL Certificate Setup and Renewal Guide

This guide explains how to renew/generate SSL certificates for your bench sites and set up automatic renewal.

## Sites
- `apps.heinigesons.com` (has SSL, may need renewal)
- `apps.nolagg.com` (needs SSL)
- `dev.ignitr.cloud` (needs SSL)
- `prod.nexelya.com` (has SSL, may need renewal)

## Step 1: Generate/Renew SSL Certificates

Run the renewal script with sudo:

```bash
cd /home/ubuntu/frappe-bench
sudo ./renew_ssl_certs.sh
```

This script will:
- Check existing certificates and their expiration dates
- Renew expired or expiring certificates
- Generate new certificates for sites without SSL
- Use Let's Encrypt with standalone mode (requires nginx to be temporarily stopped)

## Step 2: Update Nginx Configuration

After certificates are generated/renewed, update nginx configuration:

```bash
cd /home/ubuntu/frappe-bench
./update_nginx_ssl.sh
sudo ./update_nginx_ssl_complete.sh
```

Or manually:
```bash
cd /home/ubuntu/frappe-bench
bench setup nginx --yes
sudo cp config/nginx.conf /etc/nginx/sites-available/frappe-bench
sudo ln -sf /etc/nginx/sites-available/frappe-bench /etc/nginx/sites-enabled/frappe-bench
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
```

## Step 3: Set Up Automatic Renewal

Set up automatic certificate renewal with nginx reload:

```bash
cd /home/ubuntu/frappe-bench
sudo ./setup_ssl_auto_renewal.sh
```

This will:
- Create renewal hooks that reload nginx after certificates are renewed
- Enable the certbot timer (runs twice daily)
- Ensure nginx is properly restarted after renewal

## Testing

### Test certificate renewal (dry run):
```bash
sudo certbot renew --dry-run
```

### Check certificate expiration dates:
```bash
sudo certbot certificates
```

### Check certbot timer status:
```bash
sudo systemctl status certbot.timer
```

### View certbot logs:
```bash
sudo journalctl -u certbot.service -f
```

## Important Notes

1. **Standalone Mode**: Certificates use standalone mode, which requires nginx to be temporarily stopped during renewal. This is handled automatically by certbot.

2. **Renewal Timing**: Let's Encrypt certificates expire after 90 days. Certbot will automatically renew certificates when they have 30 days or less remaining.

3. **Nginx Reload**: After renewal, nginx will be automatically reloaded by the renewal hooks.

4. **Manual Renewal**: If you need to manually renew certificates:
   ```bash
   sudo certbot renew --force-renewal
   sudo systemctl reload nginx
   ```

## Troubleshooting

If certificates fail to renew:
1. Check that ports 80 and 443 are accessible
2. Verify DNS records point to this server
3. Check certbot logs: `sudo journalctl -u certbot.service`
4. Test nginx configuration: `sudo nginx -t`

If nginx doesn't reload after renewal:
1. Check the deploy hook: `/etc/letsencrypt/renewal-hooks/deploy/reload-nginx.sh`
2. Test nginx configuration: `sudo nginx -t`
3. Manually reload: `sudo systemctl reload nginx`
