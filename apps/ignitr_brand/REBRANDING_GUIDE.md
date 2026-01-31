# Complete UI Rebranding Guide

This guide explains how the `ignitr_brand` app completely rebrands your Frappe/ERPNext installation to look like your own product (Nexelya).

## What Has Been Customized

### 1. **Text Replacement**
- All instances of "Frappe" are replaced with "Nexelya"
- All instances of "ERPNext" are replaced with "Nexelya ERP"
- Login page titles and messages are rebranded
- Footer "Powered by" text is hidden

### 2. **JavaScript Branding** (`brand.js`)
- Real-time text replacement on page load and route changes
- Hides "Browse Apps" module card
- Hides footer branding elements
- Watches for dynamically loaded content
- Replaces text in titles, placeholders, and attributes

### 3. **CSS Styling** (`ignitr_brand.css`)
- Hides Frappe/ERPNext footer links
- Customizes logo display
- Removes branding from various UI elements

### 4. **Template Overrides**
- Footer templates are overridden to remove "Powered by" text
- Login page context is customized

### 5. **Translation Files**
- Comprehensive translation mappings for all Frappe/ERPNext references

## Setup Instructions

### 1. Configure App Name and Logo

Go to **System Settings** and set:
- **App Name**: "Nexelya" (or your preferred name)
- **App Logo**: Upload your custom logo

Or use **Navbar Settings**:
- **App Logo**: Upload your logo
- This will appear in the navbar and login page

### 2. Configure Website Settings

Go to **Website Settings**:
- **App Name**: Set to "Nexelya"
- **App Logo**: Upload your logo
- **Splash Image**: Upload your splash/loading image

### 3. Clear Cache

After making changes, clear the cache:

```bash
bench --site <your-site> clear-cache
```

### 4. Build Assets (if needed)

If you modify CSS/JS files:

```bash
bench build --app ignitr_brand
bench --site <your-site> clear-cache
```

## Customization Options

### Change Brand Name

Edit `/apps/ignitr_brand/ignitr_brand/public/js/brand.js` and update the `replacements` array:

```javascript
ignitr_brand.brandConfig = {
  replacements: [
    { from: /ERPNext/gi, to: "Your Brand ERP" },
    { from: /Frappe/gi, to: "Your Brand" },
    // ... more replacements
  ]
};
```

### Change Colors/Theme

Edit `/apps/ignitr_brand/ignitr_brand/public/css/ignitr_brand.css` to add your brand colors:

```css
:root {
  --primary-color: #your-color;
  --navbar-bg: #your-color;
}
```

Or use the `frappe_desk_theme` app for more comprehensive theming.

### Add Custom Logo

1. Place your logo in `/apps/ignitr_brand/ignitr_brand/public/images/logo.png`
2. Update System Settings or Navbar Settings to use this logo
3. Or reference it directly in CSS:

```css
.navbar-brand .app-logo {
  content: url('/assets/ignitr_brand/images/logo.png');
}
```

## What Gets Rebranded

✅ Login page title and logo
✅ Navbar logo and branding
✅ Footer "Powered by" text (hidden)
✅ All text references to Frappe/ERPNext
✅ Module names and labels
✅ Help text and tooltips
✅ Page titles
✅ Email templates (via translations)

## Testing

1. **Login Page**: Visit `/login` - should show "Login to Nexelya" (or your app name)
2. **Navbar**: Check that your logo appears in the navbar
3. **Footer**: Footer should not show "Powered by Frappe" or "Powered by ERPNext"
4. **Desktop**: All module cards should show rebranded names
5. **Search**: Search for "Frappe" - should be replaced with "Nexelya"

## Troubleshooting

### Branding not appearing?
1. Clear cache: `bench --site <site> clear-cache`
2. Check that `ignitr_brand` is in `apps.txt`
3. Verify hooks are loaded: Check browser console for JS errors

### Logo not showing?
1. Check System Settings > App Logo is set
2. Check Navbar Settings > App Logo is set
3. Verify logo file path is correct
4. Clear browser cache

### Footer still showing branding?
1. Clear cache
2. Check template overrides are in place
3. Verify CSS is loading (check browser DevTools)

## Advanced Customization

### Override More Templates

Create template overrides in:
`/apps/ignitr_brand/ignitr_brand/templates/`

For example, to override the login template:
1. Copy from Frappe: `apps/frappe/frappe/www/login.html`
2. Place in: `apps/ignitr_brand/ignitr_brand/templates/www/login.html`
3. Customize as needed

### Add More Translations

Edit `/apps/ignitr_brand/ignitr_brand/translations/en.csv` and add more mappings.

### Custom Python Overrides

Add more overrides in `/apps/ignitr_brand/ignitr_brand/overrides.py`

## Notes

- The rebranding works on both desk and website views
- JavaScript replacements happen in real-time as pages load
- Template overrides take precedence over JS replacements
- Some hardcoded references in minified JS may not be replaceable

## Support

For issues or questions, check:
- Browser console for JavaScript errors
- Frappe logs for Python errors
- Verify all files are in the correct locations

