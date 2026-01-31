# Quick Reference Card - SaaS Administration

## Multi-Tenancy: Single Bench vs. Multiple Benches

**✅ Use Single Bench with Multiple Sites** (Recommended)
- One bench, multiple sites (one per customer)
- Each site = one database (isolated)
- Shared resources (code, workers, Redis)
- Easier management, lower cost

**Use Separate Benches Only For:**
- Enterprise customers needing dedicated resources
- Compliance requiring separation
- Different app versions

## Quick Commands

### Site Management
```bash
# Create new site
bench new-site customer1.nexelya.com --admin-password 'Password123!'

# Install apps
bench --site customer1.nexelya.com install-app erpnext crm

# Migrate one site
bench --site customer1.nexelya.com migrate

# Migrate all sites
bench --site all migrate

# Clear cache
bench --site customer1.nexelya.com clear-cache
bench --site all clear-cache
```

### Maintenance Scripts
```bash
# Full maintenance (all sites)
./refresh.sh

# Maintenance for one site
./refresh.sh --site customer1.nexelya.com

# Health check
./saas_admin.sh health

# Collect metrics
./saas_admin.sh metrics

# Full SaaS admin tasks
./saas_admin.sh full
```

### SaaS Admin Commands
```bash
./saas_admin.sh health              # Health checks
./saas_admin.sh metrics             # Collect metrics
./saas_admin.sh cleanup             # Clean old files
./saas_admin.sh optimize            # Optimize databases
./saas_admin.sh verify-backups      # Verify backups
./saas_admin.sh ssl-check           # Check SSL certs
./saas_admin.sh services            # Check services
./saas_admin.sh disk-space          # Check disk usage
./saas_admin.sh site-info SITE     # Site information
./saas_admin.sh full                # All tasks
```

### Backup & Restore
```bash
# Backup one site
bench --site customer1.nexelya.com backup --with-files

# Backup all sites
bench --site all backup --with-files

# Restore
bench --site customer1.nexelya.com restore /path/to/backup
```

### Monitoring
```bash
# Check disk space
df -h

# Check memory
free -h

# Check Redis
redis-cli -p 13000 ping
redis-cli -p 11000 ping

# Check MariaDB
mysqladmin ping -u root

# Check supervisor
supervisorctl status
```

### Logs
```bash
# Application logs
tail -f logs/web.log
tail -f logs/worker.log

# Maintenance logs
tail -f maintenance_logs/maintain_*.log
tail -f maintenance_logs/saas_admin_*.log

# Site-specific logs
tail -f sites/customer1.nexelya.com/logs/*.log
```

## Common Tasks

### Add New Customer
1. Create site: `bench new-site customer1.nexelya.com`
2. Install apps: `bench --site customer1.nexelya.com install-app erpnext crm`
3. Set up plan: Use Nexelya Plan Settings doctype
4. Configure DNS: Point to server IP
5. Set up SSL: `sudo certbot --nginx -d customer1.nexelya.com`

### Update All Sites
```bash
./refresh.sh  # Runs: backup, migrate, clear-cache, build, restart
```

### Check Site Health
```bash
./saas_admin.sh health customer1.nexelya.com
```

### Find Large Databases
```bash
mysql -u root -e "SELECT table_schema AS 'Database', 
  ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS 'Size (MB)' 
  FROM information_schema.tables 
  WHERE table_schema LIKE '%' 
  GROUP BY table_schema 
  ORDER BY SUM(data_length + index_length) DESC;"
```

### Emergency: Site Down
```bash
# Check site status
bench --site customer1.nexelya.com console
# In console: frappe.db.get_value("System Settings", "System Settings", "setup_complete")

# Restart services
sudo supervisorctl restart all

# Clear cache
bench --site customer1.nexelya.com clear-cache

# Check logs
tail -f sites/customer1.nexelya.com/logs/*.log
```

## Environment Variables

```bash
# Set alert email
export ALERT_EMAIL="admin@nexelya.com"

# Set thresholds
export DISK_WARNING_PERCENT=80
export DISK_CRITICAL_PERCENT=90
export MEMORY_WARNING_PERCENT=80
```

## File Locations

```
/home/ubuntu/frappe-bench/
├── sites/                    # All site directories
│   ├── customer1.nexelya.com/
│   │   ├── site_config.json
│   │   ├── private/
│   │   │   ├── files/
│   │   │   └── backups/
│   │   └── public/
│   └── common_site_config.json
├── apps/                     # Application code
├── logs/                     # Application logs
├── maintenance_logs/         # Maintenance script logs
├── backup_archives/          # Compressed backups
├── saas_metrics/             # Collected metrics
├── refresh.sh                # Maintenance script
└── saas_admin.sh             # SaaS admin script
```

## Important Notes

- ✅ Each site has its own database (isolated)
- ✅ Redis keys are automatically namespaced by site
- ✅ Files are stored per-site in `sites/SITE/private/files/`
- ✅ Use `bench --site all` for bulk operations
- ✅ Always backup before major operations
- ✅ Monitor disk space regularly
- ✅ Check SSL certificates monthly

## Getting Help

```bash
# Script help
./refresh.sh --help
./saas_admin.sh --help

# Documentation
cat MULTI_TENANCY_GUIDE.md
cat SAAS_ADMINISTRATION_SUMMARY.md
```

