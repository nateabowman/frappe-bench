# Agriculture Demo Site Setup - agri-demo.nexelya.com

## ✅ Completed Steps

1. **Agriculture App Installed**: Successfully cloned and installed from https://github.com/nateabowman/agriculture.git
2. **Site Created**: agri-demo.nexelya.com
3. **Apps Installed**:
   - frappe (15.72.4)
   - erpnext (15.71.1)
   - agriculture (0.0.1 develop)
4. **Configuration**: Site configured for agriculture (no construction apps)
5. **Nginx**: Site added to nginx configuration
6. **Database**: Site database created and migrations completed

## 🔒 SSL Certificate Setup (Requires sudo)

To complete the SSL setup, run the following commands:

```bash
cd /home/ubuntu/frappe-bench

# Option 1: Use the automated script
sudo ./setup_agri_ssl.sh

# Option 2: Manual setup
# 1. Generate SSL certificate
sudo certbot certonly --standalone \
    --non-interactive \
    --agree-tos \
    --email admin@nexelya.com \
    -d agri-demo.nexelya.com

# 2. Configure SSL in site config
bench set-ssl-certificate agri-demo.nexelya.com /etc/letsencrypt/live/agri-demo.nexelya.com/fullchain.pem
bench set-ssl-key agri-demo.nexelya.com /etc/letsencrypt/live/agri-demo.nexelya.com/privkey.pem

# 3. Regenerate nginx config
bench setup nginx --yes

# 4. Copy nginx config and reload
sudo cp config/nginx.conf /etc/nginx/sites-available/frappe-bench
sudo nginx -t
sudo systemctl reload nginx
```

## 🌐 DNS Configuration

Ensure DNS is configured to point agri-demo.nexelya.com to this server's IP address.

## ✅ Verification

After SSL setup, verify the site:

```bash
# Check site status
bench --site agri-demo.nexelya.com list-apps

# Test HTTPS
curl -I https://agri-demo.nexelya.com

# Check SSL certificate
sudo certbot certificates | grep agri-demo
```

## 📝 Site Details

- **Site Name**: agri-demo.nexelya.com
- **Admin Password**: admin
- **Database**: _369e59c8692b41d5
- **Apps**: frappe, erpnext, agriculture
- **Status**: Ready for production (pending SSL setup)

## 🚀 Next Steps

1. Run SSL setup commands above
2. Configure DNS if not already done
3. Test the site at https://agri-demo.nexelya.com
4. Verify agriculture app functionality
