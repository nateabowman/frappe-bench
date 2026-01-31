# Installation Guide - Modern ERP UI

## Quick Start

### Step 1: Install the App

From your Frappe bench directory, run:

```bash
bench install-app modern_erp_ui
```

If you get an error that the app is not found, you may need to add it to your bench first:

```bash
bench get-app modern_erp_ui --branch develop
```

Or if you've manually copied the app:

```bash
bench --site [your-site-name] install-app modern_erp_ui
```

### Step 2: Build Assets

Build the CSS and JavaScript assets:

```bash
bench build --app modern_erp_ui
```

For production (minified):

```bash
bench build --app modern_erp_ui --production
```

### Step 3: Restart Services

Restart your Frappe server to apply changes:

```bash
bench restart
```

Or if using supervisor/systemd:

```bash
bench restart --web
```

### Step 4: Clear Cache (Optional)

Clear browser cache and Frappe cache:

```bash
bench --site [your-site-name] clear-cache
```

Then clear your browser cache or do a hard refresh (Ctrl+Shift+R or Cmd+Shift+R).

## Verification

1. Log in to your ERPNext/Frappe instance
2. You should see the modern UI applied:
   - Modern gradient login page
   - Updated navigation bar
   - Enhanced buttons with hover effects
   - Modern form inputs
   - Improved table styling

## Troubleshooting

### Theme Not Appearing

1. **Check app installation:**
   ```bash
   bench list-apps
   ```
   You should see `modern_erp_ui` in the list.

2. **Rebuild assets:**
   ```bash
   bench build --app modern_erp_ui --force
   ```

3. **Check hooks.py:**
   Ensure the app's hooks.py is being loaded. Check your site's `apps.txt`:
   ```bash
   cat sites/[your-site-name]/apps.txt
   ```

4. **Clear all caches:**
   ```bash
   bench --site [your-site-name] clear-cache
   bench --site [your-site-name] clear-website-cache
   ```

5. **Check browser console:**
   Open browser DevTools (F12) and check for:
   - CSS file loading errors
   - JavaScript errors
   - Network tab to see if assets are loading

### Conflicts with Other Themes

If you have other theme apps installed (like `frappe_desk_theme`), they might conflict. You can:

1. Disable other theme apps temporarily
2. Adjust the load order in hooks.py
3. Use more specific CSS selectors

### Assets Not Loading

1. **Check file permissions:**
   ```bash
   ls -la apps/modern_erp_ui/modern_erp_ui/public/css/
   ls -la apps/modern_erp_ui/modern_erp_ui/public/js/
   ```

2. **Verify asset paths:**
   The files should be accessible at:
   - `/assets/modern_erp_ui/css/modern_erp_ui.css`
   - `/assets/modern_erp_ui/js/modern_erp_ui.js`

3. **Check nginx/apache configuration** (if using reverse proxy)

## Uninstallation

To remove the Modern ERP UI:

```bash
bench --site [your-site-name] uninstall-app modern_erp_ui
bench build
bench restart
```

## Development Mode

For development with auto-reload:

```bash
bench watch
```

This will automatically rebuild assets when you make changes.

## Next Steps

- Customize colors in `modern_erp_ui/public/css/modern_erp_ui.css`
- Modify JavaScript behavior in `modern_erp_ui/public/js/modern_erp_ui.js`
- Add custom components as needed

Enjoy your modern ERP interface! 🎨

