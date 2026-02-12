# Agriculture Demo Site Setup

Guide for setting up a site with the Agriculture app.

## Prerequisites

- Frappe Bench with ERPNext
- Agriculture app: https://github.com/nateabowman/agriculture

## Setup Steps

### 1. Install Agriculture App

```bash
cd /path/to/frappe-bench
bench get-app agriculture
bench install-app agriculture
```

Or for a new site:

```bash
bench new-site agri-demo.yourdomain.com --admin-password 'YourSecurePassword'
bench --site agri-demo.yourdomain.com install-app erpnext
bench --site agri-demo.yourdomain.com install-app agriculture
```

### 2. SSL Certificate

```bash
sudo certbot certonly --standalone -d agri-demo.yourdomain.com
bench set-ssl-certificate agri-demo.yourdomain.com /etc/letsencrypt/live/agri-demo.yourdomain.com/fullchain.pem
bench set-ssl-key agri-demo.yourdomain.com /etc/letsencrypt/live/agri-demo.yourdomain.com/privkey.pem
bench setup nginx --yes
```

### 3. Nginx and DNS

- Copy nginx config and reload
- Point DNS A record to your server IP

## Agriculture Features

- Crop Management
- Farm & Plot Management
- Soil & Water Analysis
- Plant Analysis
- Weather Tracking
- Equipment Management
- Livestock Management
- Irrigation Scheduling
- Harvest Management
- Disease Detection
- Fertilizer Management

## Verification

```bash
bench --site agri-demo.yourdomain.com list-apps
```
