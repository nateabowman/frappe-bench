# Quick Fix for Installation Issues

## The Problem
The app can't be found because it's not registered in the site's `apps.txt` file.

## Solution (Run these commands on your Ubuntu server)

```bash
cd ~/frappe-bench

# 1. Add app to site-specific apps.txt
echo "modern_erp_ui" >> sites/prod.nexelya.com/apps.txt

# 2. Clear Python cache
find apps/modern_erp_ui -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true

# 3. Clear Frappe cache
bench --site prod.nexelya.com clear-cache

# 4. Install the app
bench --site prod.nexelya.com install-app modern_erp_ui

# 5. Build assets
bench build --app modern_erp_ui

# 6. Restart
bench restart
```

## Or use the setup script:

```bash
cd ~/frappe-bench
chmod +x apps/modern_erp_ui/setup.sh
./apps/modern_erp_ui/setup.sh prod.nexelya.com
```

## If it still doesn't work:

1. **Verify the app structure:**
   ```bash
   ls -la apps/modern_erp_ui/modern_erp_ui/
   # Should show: __init__.py, hooks.py, public/
   ```

2. **Check if app is in apps.txt:**
   ```bash
   grep modern_erp_ui sites/prod.nexelya.com/apps.txt
   ```

3. **Verify Python can import it:**
   ```bash
   cd ~/frappe-bench
   source env/bin/activate
   python -c "import modern_erp_ui; print('OK')"
   ```

4. **If Python import fails, check the path:**
   ```bash
   python -c "import sys; print('\n'.join(sys.path))"
   # Should include: /home/ubuntu/frappe-bench/apps
   ```

