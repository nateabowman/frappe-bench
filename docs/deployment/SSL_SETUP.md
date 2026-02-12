# SSL Certificate Setup and Renewal

Setup and renew SSL certificates for bench sites using Let's Encrypt.

## Prerequisites

- Domain pointing to your server
- Certbot installed
- Nginx (or another web server) for HTTP-01 challenge, or use standalone mode

## Step 1: Generate SSL Certificates

### Option A: Using Certbot with Nginx

```bash
sudo certbot --nginx -d your-site.example.com
```

### Option B: Standalone (stops web server temporarily)

```bash
# Nginx must be stopped for standalone
sudo systemctl stop nginx
sudo certbot certonly --standalone \
  --non-interactive \
  --agree-tos \
  -d your-site.example.com
sudo systemctl start nginx
```

### Option C: Wildcard (DNS challenge)

```bash
sudo certbot certonly --dns-cloudflare \
  -d "*.example.com" -d "example.com"
```

## Step 2: Update Nginx Configuration

After certificates are generated:

```bash
cd /path/to/frappe-bench
bench setup nginx --yes
sudo cp config/nginx.conf /etc/nginx/sites-available/frappe-bench
sudo nginx -t
sudo systemctl reload nginx
```

## Step 3: Automatic Renewal

Certbot installs a systemd timer or cron job. For nginx reload after renewal:

```bash
# Create renewal hook
sudo mkdir -p /etc/letsencrypt/renewal-hooks/deploy
echo '#!/bin/bash\nsystemctl reload nginx' | sudo tee /etc/letsencrypt/renewal-hooks/deploy/reload-nginx.sh
sudo chmod +x /etc/letsencrypt/renewal-hooks/deploy/reload-nginx.sh
```

## Verify

```bash
sudo certbot certificates
curl -I https://your-site.example.com
```

## Reference Scripts

- `renew_ssl_certs.sh` – Renew certificates
- `setup_ssl_auto_renewal.sh` – Configure auto-renewal with nginx reload
