# Fix: ModuleNotFoundError during maintenance

## The Problem

The error occurs because `modern_erp_ui` is listed in `apps.txt` files, but the app doesn't exist on your Ubuntu server yet (or the app structure is incomplete).

## Solution 1: Remove from apps.txt (Temporary Fix)

If the app isn't installed yet, remove it from all `apps.txt` files:

```bash
cd ~/frappe-bench

# Remove from global apps.txt
sed -i '/^modern_erp_ui$/d' sites/apps.txt

# Remove from all site-specific apps.txt files
find sites -name "apps.txt" -type f -exec sed -i '/^modern_erp_ui$/d' {} \;
```

## Solution 2: Ensure App Exists on Server (Proper Fix)

Make sure the app directory exists on your Ubuntu server:

```bash
cd ~/frappe-bench

# Check if app exists
ls -la apps/modern_erp_ui/

# Should show:
# - modern_erp_ui/
#   - __init__.py
#   - hooks.py
#   - commands.py  ← This file prevents the error
#   - public/
```

If the app doesn't exist, you need to:
1. Copy/sync the app from your Windows machine to the Ubuntu server
2. Or clone it from a repository
3. Or create it manually

## Solution 3: Create Minimal App Structure (Quick Fix)

If you just need to stop the errors temporarily, create a minimal app structure:

```bash
cd ~/frappe-bench/apps

# Create minimal structure
mkdir -p modern_erp_ui/modern_erp_ui/public/{css,js}

# Create required files
cat > modern_erp_ui/modern_erp_ui/__init__.py << 'EOF'
__version__ = "1.0.0"
EOF

cat > modern_erp_ui/modern_erp_ui/hooks.py << 'EOF'
app_name = "modern_erp_ui"
app_title = "Modern ERP UI"
app_publisher = "Modern ERP UI Team"
app_description = "Modern, contemporary UI theme for ERPNext and Frappe"
app_email = ""
app_license = "mit"
EOF

cat > modern_erp_ui/modern_erp_ui/commands.py << 'EOF'
# Commands module - prevents import errors
EOF

# Create empty CSS/JS files
touch modern_erp_ui/modern_erp_ui/public/css/modern_erp_ui.css
touch modern_erp_ui/modern_erp_ui/public/js/modern_erp_ui.js
```

## Recommended Approach

**If the app isn't ready yet:**
- Use Solution 1 to remove it from apps.txt
- Install it properly later when ready

**If you want to keep it listed:**
- Use Solution 3 to create minimal structure
- Then properly install it later

The `commands.py` file I've added will prevent the import error, but you still need the app directory to exist on the server.

