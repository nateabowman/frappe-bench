#!/bin/bash
set -euo pipefail
trap 'echo -e "❌ Error on line $LINENO. Check $LOGFILE" | tee -a "$LOGFILE"; exit 1' ERR

# -----------------------------
# SaaS Administration & Maintenance Script
# -----------------------------

BENCH_PATH="/home/ubuntu/frappe-bench"
BENCH_BIN="$BENCH_PATH/env/bin/bench"
SITES_DIR="$BENCH_PATH/sites"
DATE=$(date +"%Y-%m-%d_%H-%M-%S")
LOGFILE="$BENCH_PATH/maintenance_logs/saas_admin_$DATE.log"
ARCHIVE_DIR="$BENCH_PATH/backup_archives"
METRICS_DIR="$BENCH_PATH/saas_metrics"
ALERT_EMAIL="${ALERT_EMAIL:-}"  # Set via environment variable

# Colors
NC='\033[0m'
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'

# Thresholds (configurable via environment)
DISK_WARNING_PERCENT="${DISK_WARNING_PERCENT:-80}"
DISK_CRITICAL_PERCENT="${DISK_CRITICAL_PERCENT:-90}"
MEMORY_WARNING_PERCENT="${MEMORY_WARNING_PERCENT:-80}"
DB_SIZE_WARNING_MB="${DB_SIZE_WARNING_MB:-5000}"
LOG_SIZE_WARNING_MB="${LOG_SIZE_WARNING_MB:-1000}"

mkdir -p "$BENCH_PATH/maintenance_logs" "$ARCHIVE_DIR" "$METRICS_DIR"
cd "$BENCH_PATH"

# Determine mode
MODE="${1:-all}"
SITE="${2:-}"

if [[ "$MODE" == "--help" || "$MODE" == "-h" ]]; then
  cat << EOF
SaaS Administration Script

Usage: $0 [COMMAND] [SITE]

Commands:
  health          - Run health checks on all sites
  health-check    - Same as health
  metrics         - Collect and store system metrics
  cleanup         - Clean up old logs, backups, and cache
  optimize        - Optimize databases and clear old data
  verify-backups  - Verify backup integrity
  ssl-check       - Check SSL certificate expiration
  services        - Check service status (supervisor, redis, mariadb)
  disk-space      - Check disk space usage
  site-info       - Show information about a specific site
  full            - Run all maintenance tasks (default)
  [SITE]          - Run maintenance for specific site only

Examples:
  $0 health                    # Health check all sites
  $0 health prod.nexelya.com   # Health check one site
  $0 metrics                   # Collect metrics
  $0 cleanup                   # Cleanup old files
  $0 optimize                  # Optimize databases
  $0 verify-backups            # Verify backups
  $0 ssl-check                 # Check SSL certificates
  $0 services                  # Check services
  $0 disk-space                # Check disk usage
  $0 site-info prod.nexelya.com # Site information
  $0 full                      # Full maintenance

Environment Variables:
  ALERT_EMAIL              - Email for alerts
  DISK_WARNING_PERCENT    - Disk warning threshold (default: 80)
  DISK_CRITICAL_PERCENT   - Disk critical threshold (default: 90)
  MEMORY_WARNING_PERCENT  - Memory warning threshold (default: 80)
  DB_SIZE_WARNING_MB      - Database size warning in MB (default: 5000)
  LOG_SIZE_WARNING_MB     - Log size warning in MB (default: 1000)
EOF
  exit 0
fi

timestamp_section() {
  echo -e "\n${BLUE}⏱️ [$1] $(date +"%T")${NC}" | tee -a "$LOGFILE"
}

send_alert() {
  local subject="$1"
  local message="$2"
  if [[ -n "$ALERT_EMAIL" ]]; then
    echo "$message" | mail -s "$subject" "$ALERT_EMAIL" 2>/dev/null || true
  fi
  echo -e "${RED}🚨 ALERT: $subject${NC}" | tee -a "$LOGFILE"
  echo "$message" | tee -a "$LOGFILE"
}

# Get all sites
get_sites() {
  local sites=()
  if [[ -n "$SITE" && "$MODE" != "full" ]]; then
    sites=("$SITE")
  else
    for path in "$SITES_DIR"/*; do
      [[ -d "$path" ]] || continue
      name=$(basename "$path")
      [[ "$name" =~ ^(assets|common_site_config\.json|apps\.json|apps\.txt)$ ]] && continue
      sites+=("$name")
    done
  fi
  echo "${sites[@]}"
}

# Health check for a site
health_check_site() {
  local site="$1"
  local issues=0
  
  echo -e "${CYAN}Checking health of ${site}...${NC}" | tee -a "$LOGFILE"
  
  # Check if site is accessible
  if ! "$BENCH_BIN" --site "$site" console --execute "frappe.db.get_value('System Settings', 'System Settings', 'setup_complete')" >>"$LOGFILE" 2>&1; then
    echo -e "${RED}  ✗ Site database connection failed${NC}" | tee -a "$LOGFILE"
    ((issues++))
  else
    echo -e "${GREEN}  ✓ Database connection OK${NC}" | tee -a "$LOGFILE"
  fi
  
  # Check scheduler
  if ! "$BENCH_BIN" --site "$site" console --execute "frappe.utils.scheduler.is_scheduler_inactive()" >>"$LOGFILE" 2>&1; then
    echo -e "${YELLOW}  ⚠ Scheduler may be inactive${NC}" | tee -a "$LOGFILE"
  else
    echo -e "${GREEN}  ✓ Scheduler active${NC}" | tee -a "$LOGFILE"
  fi
  
  # Check for failed jobs
  local failed_jobs=$("$BENCH_BIN" --site "$site" console --execute "frappe.db.count('Scheduled Job Log', {'status': 'Failed', 'creation': ['>', frappe.utils.add_days(frappe.utils.now(), -1)]})" 2>/dev/null | tail -1 || echo "0")
  if [[ "$failed_jobs" -gt 10 ]]; then
    echo -e "${YELLOW}  ⚠ High number of failed jobs: $failed_jobs${NC}" | tee -a "$LOGFILE"
    ((issues++))
  fi
  
  return $issues
}

# Collect system metrics
collect_metrics() {
  timestamp_section "Collecting System Metrics"
  
  local metrics_file="$METRICS_DIR/metrics_$DATE.json"
  local metrics="{"
  
  # Disk usage
  local disk_usage=$(df -h "$BENCH_PATH" | awk 'NR==2 {print $5}' | sed 's/%//')
  metrics+="\"disk_usage_percent\": $disk_usage, "
  
  # Memory usage
  local mem_usage=$(free | awk 'NR==2{printf "%.0f", $3*100/$2}')
  metrics+="\"memory_usage_percent\": $mem_usage, "
  
  # CPU load
  local cpu_load=$(uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | sed 's/,//')
  metrics+="\"cpu_load_1min\": $cpu_load, "
  
  # Database sizes
  local db_sizes="{"
  local sites_array=($(get_sites))
  for site in "${sites_array[@]}"; do
    local db_name=$("$BENCH_BIN" --site "$site" console --execute "frappe.conf.db_name" 2>/dev/null | tail -1 || echo "")
    if [[ -n "$db_name" ]]; then
      local db_size=$(mysql -u root -e "SELECT ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS 'DB Size in MB' FROM information_schema.tables WHERE table_schema='$db_name';" 2>/dev/null | tail -1 || echo "0")
      db_sizes+="\"$site\": $db_size, "
    fi
  done
  db_sizes="${db_sizes%, }"
  metrics+="\"database_sizes\": {$db_sizes}, "
  
  # Site count
  metrics+="\"site_count\": ${#sites_array[@]}, "
  
  # Log sizes
  local log_size_mb=$(du -sm "$BENCH_PATH/logs" 2>/dev/null | awk '{print $1}' || echo "0")
  metrics+="\"log_size_mb\": $log_size_mb"
  
  metrics+="}"
  echo "$metrics" > "$metrics_file"
  echo -e "${GREEN}✓ Metrics saved to $metrics_file${NC}" | tee -a "$LOGFILE"
  
  # Check thresholds
  if [[ $disk_usage -gt $DISK_CRITICAL_PERCENT ]]; then
    send_alert "CRITICAL: Disk Space" "Disk usage is at ${disk_usage}% (critical threshold: ${DISK_CRITICAL_PERCENT}%)"
  elif [[ $disk_usage -gt $DISK_WARNING_PERCENT ]]; then
    send_alert "WARNING: Disk Space" "Disk usage is at ${disk_usage}% (warning threshold: ${DISK_WARNING_PERCENT}%)"
  fi
  
  if [[ $mem_usage -gt $MEMORY_WARNING_PERCENT ]]; then
    send_alert "WARNING: Memory Usage" "Memory usage is at ${mem_usage}%"
  fi
}

# Cleanup old files
cleanup_old_files() {
  timestamp_section "Cleaning Up Old Files"
  
  # Clean old logs (keep last 30 days)
  echo -e "${CYAN}Cleaning old logs...${NC}" | tee -a "$LOGFILE"
  find "$BENCH_PATH/logs" -name "*.log" -type f -mtime +30 -delete 2>/dev/null || true
  find "$BENCH_PATH/maintenance_logs" -name "*.log" -type f -mtime +30 -delete 2>/dev/null || true
  
  # Clean old backups (keep last 90 days)
  echo -e "${CYAN}Cleaning old backups...${NC}" | tee -a "$LOGFILE"
  find "$ARCHIVE_DIR" -name "*.tar.gz" -type f -mtime +90 -delete 2>/dev/null || true
  
  # Clean old site backups (keep last 30 days)
  for site_dir in "$SITES_DIR"/*/private/backups; do
    if [[ -d "$site_dir" ]]; then
      find "$site_dir" -name "*.sql.gz" -type f -mtime +30 -delete 2>/dev/null || true
      find "$site_dir" -name "*.tar" -type f -mtime +30 -delete 2>/dev/null || true
    fi
  done
  
  # Clean Python cache
  find "$BENCH_PATH" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
  find "$BENCH_PATH" -name "*.pyc" -type f -delete 2>/dev/null || true
  
  echo -e "${GREEN}✓ Cleanup completed${NC}" | tee -a "$LOGFILE"
}

# Optimize databases
optimize_databases() {
  timestamp_section "Optimizing Databases"
  
  local sites_array=($(get_sites))
  for site in "${sites_array[@]}"; do
    echo -e "${CYAN}Optimizing database for ${site}...${NC}" | tee -a "$LOGFILE"
    
    local db_name=$("$BENCH_BIN" --site "$site" console --execute "frappe.conf.db_name" 2>/dev/null | tail -1 || echo "")
    if [[ -n "$db_name" ]]; then
      # Optimize tables
      mysql -u root -e "USE \`$db_name\`; OPTIMIZE TABLE \`tabSessions\`;" 2>/dev/null || true
      mysql -u root -e "USE \`$db_name\`; DELETE FROM \`tabSessions\` WHERE \`lastupdate\` < DATE_SUB(NOW(), INTERVAL 1 DAY);" 2>/dev/null || true
      
      # Clear old error logs
      "$BENCH_BIN" --site "$site" console --execute "frappe.db.sql('DELETE FROM \`tabError Log\` WHERE creation < DATE_SUB(NOW(), INTERVAL 30 DAY)')" 2>/dev/null || true
      
      echo -e "${GREEN}  ✓ ${site} optimized${NC}" | tee -a "$LOGFILE"
    fi
  done
}

# Verify backups
verify_backups() {
  timestamp_section "Verifying Backups"
  
  local sites_array=($(get_sites))
  local failed=0
  
  for site in "${sites_array[@]}"; do
    echo -e "${CYAN}Verifying backups for ${site}...${NC}" | tee -a "$LOGFILE"
    
    local backup_dir="$SITES_DIR/$site/private/backups"
    if [[ -d "$backup_dir" ]]; then
      local latest_backup=$(ls -t "$backup_dir"/*.sql.gz 2>/dev/null | head -1)
      if [[ -n "$latest_backup" && -f "$latest_backup" ]]; then
        # Check if backup file is valid (not corrupted)
        if gzip -t "$latest_backup" 2>/dev/null; then
          local backup_size=$(du -h "$latest_backup" | awk '{print $1}')
          echo -e "${GREEN}  ✓ Latest backup valid: $latest_backup (${backup_size})${NC}" | tee -a "$LOGFILE"
        else
          echo -e "${RED}  ✗ Backup file corrupted: $latest_backup${NC}" | tee -a "$LOGFILE"
          ((failed++))
        fi
      else
        echo -e "${YELLOW}  ⚠ No backups found for ${site}${NC}" | tee -a "$LOGFILE"
      fi
    fi
  done
  
  if [[ $failed -gt 0 ]]; then
    send_alert "Backup Verification Failed" "$failed backup(s) failed verification"
  fi
}

# Check SSL certificates
check_ssl_certificates() {
  timestamp_section "Checking SSL Certificates"
  
  local sites_array=($(get_sites))
  local expiring_soon=0
  
  for site in "${sites_array[@]}"; do
    echo -e "${CYAN}Checking SSL for ${site}...${NC}" | tee -a "$LOGFILE"
    
    # Try to get certificate expiration
    local expiry=$(echo | openssl s_client -servername "$site" -connect "$site:443" 2>/dev/null | openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2 || echo "")
    
    if [[ -n "$expiry" ]]; then
      local expiry_epoch=$(date -d "$expiry" +%s 2>/dev/null || echo "0")
      local now_epoch=$(date +%s)
      local days_until_expiry=$(( (expiry_epoch - now_epoch) / 86400 ))
      
      if [[ $days_until_expiry -lt 0 ]]; then
        echo -e "${RED}  ✗ Certificate EXPIRED for ${site}${NC}" | tee -a "$LOGFILE"
        send_alert "SSL Certificate Expired" "Certificate for $site has expired!"
        ((expiring_soon++))
      elif [[ $days_until_expiry -lt 30 ]]; then
        echo -e "${YELLOW}  ⚠ Certificate expires in ${days_until_expiry} days for ${site}${NC}" | tee -a "$LOGFILE"
        send_alert "SSL Certificate Expiring Soon" "Certificate for $site expires in ${days_until_expiry} days"
        ((expiring_soon++))
      else
        echo -e "${GREEN}  ✓ Certificate valid for ${days_until_expiry} more days${NC}" | tee -a "$LOGFILE"
      fi
    else
      echo -e "${YELLOW}  ⚠ Could not check SSL for ${site}${NC}" | tee -a "$LOGFILE"
    fi
  done
}

# Check service status
check_services() {
  timestamp_section "Checking Services"
  
  # Check supervisor
  if command -v supervisorctl &> /dev/null; then
    if supervisorctl status >>"$LOGFILE" 2>&1; then
      echo -e "${GREEN}✓ Supervisor services running${NC}" | tee -a "$LOGFILE"
    else
      echo -e "${RED}✗ Supervisor issues detected${NC}" | tee -a "$LOGFILE"
      send_alert "Supervisor Issues" "Some supervisor services may be down"
    fi
  fi
  
  # Check Redis
  if redis-cli -p 13000 ping >>"$LOGFILE" 2>&1; then
    echo -e "${GREEN}✓ Redis cache running${NC}" | tee -a "$LOGFILE"
  else
    echo -e "${RED}✗ Redis cache not responding${NC}" | tee -a "$LOGFILE"
    send_alert "Redis Cache Down" "Redis cache service is not responding"
  fi
  
  if redis-cli -p 11000 ping >>"$LOGFILE" 2>&1; then
    echo -e "${GREEN}✓ Redis queue running${NC}" | tee -a "$LOGFILE"
  else
    echo -e "${RED}✗ Redis queue not responding${NC}" | tee -a "$LOGFILE"
    send_alert "Redis Queue Down" "Redis queue service is not responding"
  fi
  
  # Check MariaDB
  if mysqladmin ping -u root >>"$LOGFILE" 2>&1; then
    echo -e "${GREEN}✓ MariaDB running${NC}" | tee -a "$LOGFILE"
  else
    echo -e "${RED}✗ MariaDB not responding${NC}" | tee -a "$LOGFILE"
    send_alert "MariaDB Down" "MariaDB service is not responding"
  fi
}

# Check disk space
check_disk_space() {
  timestamp_section "Checking Disk Space"
  
  local disk_usage=$(df -h "$BENCH_PATH" | awk 'NR==2 {print $5}' | sed 's/%//')
  local disk_available=$(df -h "$BENCH_PATH" | awk 'NR==2 {print $4}')
  local disk_total=$(df -h "$BENCH_PATH" | awk 'NR==2 {print $2}')
  
  echo -e "Disk Usage: ${disk_usage}% (${disk_available} available of ${disk_total})" | tee -a "$LOGFILE"
  
  if [[ $disk_usage -gt $DISK_CRITICAL_PERCENT ]]; then
    echo -e "${RED}✗ CRITICAL: Disk usage above ${DISK_CRITICAL_PERCENT}%${NC}" | tee -a "$LOGFILE"
    send_alert "CRITICAL: Disk Space" "Disk usage is at ${disk_usage}% (${disk_available} available)"
  elif [[ $disk_usage -gt $DISK_WARNING_PERCENT ]]; then
    echo -e "${YELLOW}⚠ WARNING: Disk usage above ${DISK_WARNING_PERCENT}%${NC}" | tee -a "$LOGFILE"
    send_alert "WARNING: Disk Space" "Disk usage is at ${disk_usage}% (${disk_available} available)"
  else
    echo -e "${GREEN}✓ Disk space OK${NC}" | tee -a "$LOGFILE"
  fi
  
  # Show largest directories
  echo -e "\n${CYAN}Top 10 largest directories:${NC}" | tee -a "$LOGFILE"
  du -h --max-depth=1 "$BENCH_PATH" 2>/dev/null | sort -rh | head -10 | tee -a "$LOGFILE"
}

# Show site information
show_site_info() {
  local site="$1"
  
  if [[ ! -d "$SITES_DIR/$site" ]]; then
    echo -e "${RED}Site '$site' not found${NC}"
    exit 1
  fi
  
  timestamp_section "Site Information: $site"
  
  # Database info
  local db_name=$("$BENCH_BIN" --site "$site" console --execute "frappe.conf.db_name" 2>/dev/null | tail -1 || echo "N/A")
  echo -e "${CYAN}Database:${NC} $db_name" | tee -a "$LOGFILE"
  
  # Database size
  if [[ "$db_name" != "N/A" ]]; then
    local db_size=$(mysql -u root -e "SELECT ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS 'Size (MB)' FROM information_schema.tables WHERE table_schema='$db_name';" 2>/dev/null | tail -1 || echo "N/A")
    echo -e "${CYAN}Database Size:${NC} ${db_size} MB" | tee -a "$LOGFILE"
  fi
  
  # User count
  local user_count=$("$BENCH_BIN" --site "$site" console --execute "frappe.db.count('User', {'enabled': 1})" 2>/dev/null | tail -1 || echo "N/A")
  echo -e "${CYAN}Active Users:${NC} $user_count" | tee -a "$LOGFILE"
  
  # Last backup
  local backup_dir="$SITES_DIR/$site/private/backups"
  if [[ -d "$backup_dir" ]]; then
    local latest_backup=$(ls -t "$backup_dir"/*.sql.gz 2>/dev/null | head -1)
    if [[ -n "$latest_backup" ]]; then
      local backup_date=$(stat -c %y "$latest_backup" 2>/dev/null | cut -d' ' -f1 || echo "N/A")
      echo -e "${CYAN}Last Backup:${NC} $backup_date" | tee -a "$LOGFILE"
    fi
  fi
  
  # Site config
  if [[ -f "$SITES_DIR/$site/site_config.json" ]]; then
    echo -e "\n${CYAN}Site Configuration:${NC}" | tee -a "$LOGFILE"
    cat "$SITES_DIR/$site/site_config.json" | tee -a "$LOGFILE"
  fi
}

# Main execution
echo -e "${MAGENTA}🔧 SaaS Administration Script - Mode: ${MODE}${NC}" | tee -a "$LOGFILE"
echo -e "Started at: $(date)" | tee -a "$LOGFILE"

case "$MODE" in
  health|health-check)
    timestamp_section "Health Checks"
    local sites_array=($(get_sites))
    local total_issues=0
    for site in "${sites_array[@]}"; do
      health_check_site "$site" || ((total_issues++))
    done
    if [[ $total_issues -eq 0 ]]; then
      echo -e "\n${GREEN}✅ All health checks passed${NC}" | tee -a "$LOGFILE"
    else
      echo -e "\n${YELLOW}⚠️  $total_issues issue(s) found${NC}" | tee -a "$LOGFILE"
    fi
    ;;
  metrics)
    collect_metrics
    ;;
  cleanup)
    cleanup_old_files
    ;;
  optimize)
    optimize_databases
    ;;
  verify-backups)
    verify_backups
    ;;
  ssl-check)
    check_ssl_certificates
    ;;
  services)
    check_services
    ;;
  disk-space)
    check_disk_space
    ;;
  site-info)
    if [[ -z "$SITE" ]]; then
      echo -e "${RED}Error: site-info requires a site name${NC}"
      echo "Usage: $0 site-info SITENAME"
      exit 1
    fi
    show_site_info "$SITE"
    ;;
  full|all|"")
    # Run all maintenance tasks
    collect_metrics
    check_services
    check_disk_space
    cleanup_old_files
    optimize_databases
    verify_backups
    check_ssl_certificates
    
    timestamp_section "Health Checks"
    local sites_array=($(get_sites))
    local total_issues=0
    for site in "${sites_array[@]}"; do
      health_check_site "$site" || ((total_issues++))
    done
    
    echo -e "\n${GREEN}✅ Full maintenance completed${NC}" | tee -a "$LOGFILE"
    ;;
  *)
    # If mode is a site name, run maintenance for that site
    if [[ -d "$SITES_DIR/$MODE" ]]; then
      SITE="$MODE"
      MODE="full"
      # Re-run with full mode
      exec "$0" full "$SITE"
    else
      echo -e "${RED}Unknown command: $MODE${NC}"
      echo "Run '$0 --help' for usage information"
      exit 1
    fi
    ;;
esac

timestamp_section "Done"
echo -e "${GREEN}✅ SaaS administration completed at $(date +"%T")${NC}" | tee -a "$LOGFILE"

