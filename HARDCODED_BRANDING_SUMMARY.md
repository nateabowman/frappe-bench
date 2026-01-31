# Hardcoded Branding Changes Summary

## Overview
All branding has been hardcoded directly into the core Frappe and ERPNext applications, replacing the JavaScript-based branding system. This ensures permanent branding changes that don't rely on runtime JavaScript replacement.

## Core Application Changes

### 1. Frappe Framework (`apps/frappe/frappe/hooks.py`)
- **app_title**: "Frappe Framework" → "Nexelya Platform"
- **app_publisher**: "Frappe Technologies" → "Nexelya Technologies"
- **app_email**: "developers@frappe.io" → "support@nexelya.io"

### 2. ERPNext (`apps/erpnext/erpnext/hooks.py`)
- **app_title**: "ERPNext" → "Nexelya ERP"
- **app_publisher**: "Frappe Technologies Pvt. Ltd." → "Nexelya Technologies Pvt. Ltd."
- **app_email**: "hello@frappe.io" → "support@nexelya.io"
- **source_link**: "https://github.com/frappe/erpnext" → "https://github.com/nexelya/erpnext"
- **add_to_apps_screen title**: "ERPNext" → "Nexelya ERP"

### 3. Template Files

#### Base Template (`apps/frappe/frappe/templates/base.html`)
- HTML comment: "Built on Frappe" → "Built on Nexelya Platform"
- URL: "https://frappeframework.com/" → "https://nexelya.io/"
- Meta generator: "frappe" → "nexelya"
- Crowdin project: "frappe" → "nexelya"

#### Footer Template (`apps/frappe/frappe/templates/includes/footer/footer_powered.html`)
- "Built on Frappe" → "Built on Nexelya"
- URL: "https://frappeframework.com" → "https://nexelya.io"

#### ERPNext Footer (`apps/erpnext/erpnext/templates/includes/footer/footer_powered.html`)
- "Powered by ERPNext" → "Powered by Nexelya ERP"
- URL: "https://frappe.io/erpnext" → "https://nexelya.io/erpnext"

#### Email Template (`apps/frappe/frappe/templates/emails/standard.html`)
- Default site URL: "https://frappeframework.com" → "https://nexelya.io"

#### App Template (`apps/frappe/frappe/www/app.html`)
- Crowdin project: "frappe" → "nexelya"

### 4. Application Context (`apps/frappe/frappe/www/app.py`)
- Default app_name fallback: "Frappe" → "Nexelya"

### 5. Copyright Notices
- Updated all Python files in `apps/frappe` and `apps/erpnext`
- "Frappe Technologies" → "Nexelya Technologies" (951 files in Frappe, all ERPNext files)

## Benefits of Hardcoded Approach

1. **Permanent**: Changes are in source code, not runtime JavaScript
2. **Performance**: No JavaScript overhead for text replacement
3. **Reliability**: Works even if JavaScript is disabled
4. **SEO**: Search engines see the correct branding
5. **Maintainability**: Easier to track and maintain changes

## Next Steps

1. **Rebuild Assets**: After these changes, rebuild the frontend assets:
   ```bash
   bench build --app frappe
   bench build --app erpnext
   bench --site <your-site> clear-cache
   ```

2. **Test**: Verify branding appears correctly in:
   - Login page
   - Desktop/app interface
   - Website footer
   - Email templates
   - Error pages

3. **Optional**: You can now disable or remove the `ignitr_brand` app's JavaScript branding system since all changes are hardcoded.

## Files Modified

### Core Hooks
- `apps/frappe/frappe/hooks.py`
- `apps/erpnext/erpnext/hooks.py`

### Templates
- `apps/frappe/frappe/templates/base.html`
- `apps/frappe/frappe/templates/includes/footer/footer_powered.html`
- `apps/frappe/frappe/templates/emails/standard.html`
- `apps/frappe/frappe/www/app.html`
- `apps/erpnext/erpnext/templates/includes/footer/footer_powered.html`

### Application Code
- `apps/frappe/frappe/www/app.py`

### Copyright Notices
- All `.py` files in `apps/frappe/frappe/` (951 files)
- All `.py` files in `apps/erpnext/erpnext/` (all files)

## Notes

- Compiled JavaScript bundles (`.bundle.js` files) will be updated when you rebuild assets
- Some references in minified files will persist until rebuild
- The `ignitr_brand` app can still be used for CSS styling and other enhancements, but the JavaScript text replacement is no longer necessary

