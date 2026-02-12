# Multi-Tenancy Guide for BuildPro SaaS

## Overview

This guide explains how to set up and manage a multi-tenant SaaS deployment using Frappe/ERPNext with BuildPro Construction Management.

## Architecture Decision: Single Bench vs. Multiple Benches

### ✅ Recommended: Single Bench with Multiple Sites

**For most SaaS deployments, use a single bench with multiple sites.**

#### Advantages:
1. **Resource Efficiency**: Shared resources (Python environment, Redis, workers) across all tenants
2. **Easier Management**: Single codebase, single update process, centralized logging
3. **Cost Effective**: Lower infrastructure costs, better resource utilization
4. **Simpler Scaling**: Add more workers/processes as needed without per-tenant overhead
5. **Faster Updates**: Update all tenants simultaneously with one command
6. **Built-in Isolation**: Each site has its own database, ensuring data isolation

#### How It Works:
- Each customer gets their own **site** (e.g., `customer1.nexelya.com`, `customer2.nexelya.com`)
- Each site has its own:
  - Database (complete isolation)
  - File storage directory
  - Configuration
  - Users and permissions
- Shared resources:
  - Application code
  - Python environment
  - Redis (with namespace isolation)
  - Background workers
  - Web server processes

### When to Use Separate Benches

Consider separate benches only for:
1. **Enterprise Customers**: Very large customers requiring dedicated resources
2. **Compliance Requirements**: Customers needing physical/logical separation
3. **Different Versions**: Customers requiring different app versions
4. **Geographic Requirements**: Customers needing data residency in specific regions
5. **High-Value Customers**: Customers willing to pay for dedicated infrastructure

## Current Setup

Your system is already configured for multi-tenancy:

```json
// sites/common_site_config.json
{
  "dns_multitenant": true,  // ✅ Multi-tenancy enabled
  "gunicorn_workers": 41,    // Shared workers
  "background_workers": 1,  // Shared background workers
  "redis_cache": "redis://127.0.0.1:13000",
  "redis_queue": "redis://127.0.0.1:11000"
}
```

## Site Creation Process

### 1. Create a New Site

```bash
# Create site with database
bench new-site customer1.nexelya.com --db-name customer1_db --admin-password 'SecurePassword123!'

# Install apps
bench --site customer1.nexelya.com install-app erpnext
bench --site customer1.nexelya.com install-app crm
bench --site customer1.nexelya.com install-app hrms

# Set up plan/subscription (using your Nexelya Plan Settings)
bench --site customer1.nexelya.com console
# Then in console:
# frappe.set_user("Administrator")
# doc = frappe.get_doc({
#   "doctype": "Nexelya Plan Settings",
#   "plan_type": "Growth",
#   "company": frappe.db.get_single_value("Company", "name")
# })
# doc.insert()
```

### 2. Configure DNS

Add DNS record pointing to your server:
```
customer1.nexelya.com  A  YOUR_SERVER_IP
```

### 3. SSL Certificate

```bash
# Using Let's Encrypt (certbot)
sudo certbot --nginx -d customer1.nexelya.com

# Or use wildcard certificate for *.nexelya.com
sudo certbot certonly --dns-cloudflare -d "*.nexelya.com" -d "nexelya.com"
```

### 4. Update Nginx Configuration

Nginx should automatically handle multiple sites with `dns_multitenant: true`. Verify:

```bash
# Check nginx config
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
```

## Site Management

### List All Sites

```bash
ls -la sites/
# Or use bench command
bench --site all list-apps
```

### Site-Specific Operations

```bash
# Run migration for one site
bench --site customer1.nexelya.com migrate

# Clear cache for one site
bench --site customer1.nexelya.com clear-cache

# Backup one site
bench --site customer1.nexelya.com backup --with-files

# Console access
bench --site customer1.nexelya.com console
```

### Bulk Operations

```bash
# Run for all sites
bench --site all migrate
bench --site all clear-cache
bench --site all backup --with-files

# Or use refresh.sh
./refresh.sh  # All sites
./refresh.sh --site customer1.nexelya.com  # One site
```

## Resource Management

### Database Isolation

Each site has its own database:
- `customer1_db`
- `customer2_db`
- `customer3_db`
- etc.

This ensures:
- Complete data isolation
- Independent backups
- Per-tenant optimization
- Easy migration/export

### Redis Namespacing

Frappe automatically namespaces Redis keys by site:
- Cache keys: `{site}:cache:{key}`
- Queue keys: `{site}:queue:{job_id}`
- Session keys: `{site}:session:{session_id}`

### File Storage

Files are stored per site:
```
sites/
  customer1.nexelya.com/
    private/
      files/
    public/
      files/
  customer2.nexelya.com/
    private/
      files/
    public/
      files/
```

## Scaling Considerations

### Vertical Scaling (Single Server)

1. **Increase Workers**: Adjust `gunicorn_workers` in `common_site_config.json`
2. **Add Background Workers**: Increase `background_workers`
3. **Database Optimization**: Tune MariaDB settings
4. **Redis Memory**: Increase Redis maxmemory

### Horizontal Scaling (Multiple Servers)

For larger deployments:

1. **Load Balancer**: Use nginx/HAProxy to distribute traffic
2. **Database Replication**: Master-slave setup for read scaling
3. **Redis Cluster**: For high availability
4. **Shared File Storage**: NFS or S3 for file storage
5. **Worker Nodes**: Separate servers for background jobs

## Monitoring & Administration

### Use SaaS Admin Script

```bash
# Health checks
./saas_admin.sh health

# Collect metrics
./saas_admin.sh metrics

# Full maintenance
./saas_admin.sh full

# Site-specific info
./saas_admin.sh site-info customer1.nexelya.com
```

### Key Metrics to Monitor

1. **Per-Site Metrics**:
   - Database size
   - User count
   - Active sessions
   - API request rate
   - Storage usage

2. **System-Wide Metrics**:
   - CPU usage
   - Memory usage
   - Disk space
   - Redis memory
   - Database connections

3. **Business Metrics**:
   - Plan type per site
   - Feature usage
   - Billing/subscription status

## Security Best Practices

### 1. Site Isolation

- ✅ Each site has separate database (enforced by Frappe)
- ✅ File storage is per-site
- ✅ Redis keys are namespaced
- ✅ User sessions are isolated

### 2. Access Control

```python
# In your custom code, always check site context
import frappe

def my_function():
    # This automatically ensures site isolation
    site = frappe.local.site
    # Your code here
```

### 3. Network Security

- Use HTTPS for all sites
- Implement rate limiting per site
- Use firewall rules
- Regular security updates

### 4. Backup Strategy

```bash
# Automated backups (add to cron)
0 2 * * * cd /home/ubuntu/frappe-bench && ./refresh.sh --site customer1.nexelya.com

# Or use bench's built-in scheduler
bench --site customer1.nexelya.com set-config backup_frequency "Daily"
```

## Plan/Subscription Management

### Using Nexelya Plan Settings

Each site should have a `Nexelya Plan Settings` record:

```python
# Check plan and features
from erpnext.projects.api.feature_gating import check_feature_access

if check_feature_access("rfi"):
    # Allow RFI feature
    pass
else:
    frappe.throw("RFI feature not available in your plan")
```

### Plan Types

- **Core**: Basic features
- **Growth**: Core + premium features
- **Enterprise**: All features + customizations

## Troubleshooting

### Site Not Accessible

```bash
# Check site exists
ls -la sites/customer1.nexelya.com/

# Check database
bench --site customer1.nexelya.com console
# In console: frappe.db.get_value("System Settings", "System Settings", "setup_complete")

# Check nginx config
sudo nginx -t
sudo systemctl status nginx

# Check DNS
dig customer1.nexelya.com
```

### Performance Issues

```bash
# Check site-specific metrics
./saas_admin.sh site-info customer1.nexelya.com

# Check database size
mysql -u root -e "SELECT table_schema AS 'Database', 
  ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS 'Size (MB)' 
  FROM information_schema.tables 
  WHERE table_schema LIKE 'customer%' 
  GROUP BY table_schema;"

# Check slow queries
mysql -u root -e "SHOW PROCESSLIST;"
```

### Resource Exhaustion

```bash
# Check disk space
./saas_admin.sh disk-space

# Check memory
free -h

# Check Redis memory
redis-cli -p 13000 INFO memory
```

## Migration from Single-Tenant to Multi-Tenant

If you have an existing single-tenant setup:

1. **Backup existing site**
   ```bash
   bench --site existing-site.com backup --with-files
   ```

2. **Create new site structure**
   ```bash
   bench new-site customer1.nexelya.com
   ```

3. **Restore data** (if needed)
   ```bash
   bench --site customer1.nexelya.com restore /path/to/backup
   ```

4. **Update DNS and SSL**

5. **Test thoroughly**

## Best Practices Summary

1. ✅ **Use single bench** for most customers
2. ✅ **One site per customer** (one database per customer)
3. ✅ **Monitor resources** using saas_admin.sh
4. ✅ **Regular backups** for each site
5. ✅ **Plan-based feature gating** using Nexelya Plan Settings
6. ✅ **Automated maintenance** using refresh.sh and saas_admin.sh
7. ✅ **SSL certificates** for all sites
8. ✅ **Regular updates** across all sites
9. ✅ **Monitor disk space** and database sizes
10. ✅ **Document customer-specific customizations**

## Additional Resources

- Frappe Multi-Tenancy Docs: https://frappeframework.com/docs/user/en/basics/sites
- ERPNext Deployment Guide: https://frappeframework.com/docs/user/en/installation
- Your custom scripts:
  - `./refresh.sh` - Maintenance and updates
  - `./saas_admin.sh` - SaaS administration and monitoring

