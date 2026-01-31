# Rebranding Summary: Frappe to Nexelya

## Overview
All links and references containing "frappe" in the name have been changed to "nexelya" across the CRM application.

## Files Updated

### Manifest and HTML Files
1. **`apps/crm/crm/public/frontend/manifest.webmanifest`**
   - Changed: "Frappe CRM" → "Nexelya CRM"

2. **`apps/crm/crm/www/crm.html`**
   - Changed: Title and meta tags from "Frappe CRM" → "Nexelya CRM"

3. **`apps/crm/crm/public/frontend/index.html`**
   - Changed: Title and meta tags from "Frappe CRM" → "Nexelya CRM"

4. **`apps/crm/frontend/index.html`**
   - Changed: Title and meta tags from "Frappe CRM" → "Nexelya CRM"

### Configuration Files
5. **`apps/crm/frontend/vite.config.js`**
   - Changed: PWA manifest name from "Frappe CRM" → "Nexelya CRM"

6. **`apps/crm/crm/hooks.py`**
   - Changed: `app_title` from "Frappe CRM" → "Nexelya CRM"
   - Changed: `app_publisher` from "Frappe Technologies Pvt. Ltd." → "Nexelya Technologies Pvt. Ltd."
   - Changed: `app_email` from "shariq@frappe.io" → "support@nexelya.io"
   - Changed: "Login to Frappe Cloud" → "Login to Nexelya Cloud"

7. **`apps/crm/pyproject.toml`**
   - Changed: Author from "Frappe Technologies Pvt. Ltd." → "Nexelya Technologies Pvt. Ltd."
   - Changed: Email from "shariq@frappe.io" → "support@nexelya.io"

8. **`apps/crm/crm/fcrm/workspace/frappe_crm/frappe_crm.json`**
   - Changed: Label and name from "Frappe CRM" → "Nexelya CRM"
   - Changed: Owner email from "shariq@frappe.io" → "support@nexelya.io"

### Frontend Components
9. **`apps/crm/frontend/src/components/Modals/AboutModal.vue`**
   - Changed: Title from "Frappe CRM" → "Nexelya CRM"
   - Changed: Copyright from "Frappe Technologies" → "Nexelya Technologies"
   - Updated all links:
     - `https://frappe.io/crm` → `https://nexelya.io/crm`
     - `https://github.com/frappe/crm` → `https://github.com/nexelya/crm`
     - `https://docs.frappe.io/crm` → `https://docs.nexelya.io/crm`
     - `https://t.me/frappecrm` → `https://t.me/nexelyacrm`
     - `https://github.com/frappe/crm/issues` → `https://github.com/nexelya/crm/issues`
     - `https://support.frappe.io` → `https://support.nexelya.io`

10. **`apps/crm/frontend/src/components/Layouts/AppSidebar.vue`**
    - Changed: "Frappe CRM mobile" → "Nexelya CRM mobile"
    - Changed: `docsLink` from `https://docs.frappe.io/crm` → `https://docs.nexelya.io/crm`

11. **`apps/crm/frontend/src/composables/frappecloud.js`**
    - Changed: Base endpoint from `https://frappecloud.com` → `https://nexelyacloud.com`
    - Changed: Dialog title from "Login to Frappe Cloud?" → "Login to Nexelya Cloud?"
    - Changed: Dialog message from "Frappe Cloud dashboard" → "Nexelya Cloud dashboard"

12. **`apps/crm/frontend/src/components/Settings/emailConfig.js`**
    - Changed: GitHub link from `https://github.com/frappe/mail` → `https://github.com/nexelya/mail`

### Email Templates
13. **`apps/crm/crm/templates/emails/crm_invitation.html`**
    - Changed: "You have been invited to join Frappe CRM" → "You have been invited to join Nexelya CRM"

### Documentation
14. **`apps/crm/README.md`**
    - Changed: All references from "Frappe CRM" → "Nexelya CRM"
    - Updated all URLs:
      - `https://frappe.io/products/crm` → `https://nexelya.io/products/crm`
      - `https://frappe.io/crm` → `https://nexelya.io/crm`
      - `https://frappecrm-demo.frappe.cloud` → `https://nexelyacrm-demo.nexelya.cloud`
      - `https://docs.frappe.io/crm` → `https://docs.nexelya.io/crm`
      - `https://github.com/frappe/crm` → `https://github.com/nexelya/crm`
      - `https://frappe.io/easy-install.py` → `https://nexelya.io/easy-install.py`
      - `https://docs.frappe.io/framework` → `https://docs.nexelya.io/framework`
      - `https://frappecloud.com/crm/signup` → `https://nexelyacloud.com/crm/signup`
      - `https://frappe.io/files/` → `https://nexelya.io/files/`
      - `https://t.me/frappecrm` → `https://t.me/nexelyacrm`
      - `https://discuss.frappe.io/c/frappe-crm` → `https://discuss.nexelya.io/c/nexelya-crm`
      - `https://x.com/frappetech` → `https://x.com/nexelyatech`
      - `https://frappe.io` → `https://nexelya.io`

15. **`apps/crm/frontend/README.md`**
    - Changed: "Frappe UI Starter" → "Nexelya UI Starter"
    - Changed: References from "Frappe" → "Nexelya"
    - Changed: GitHub link from `https://github.com/frappe/frappe-ui` → `https://github.com/nexelya/nexelya-ui`

### Other Apps
16. **`apps/insights/frontend/src/pages/TrialExpired.vue`**
    - Changed: `https://frappe.cloud/marketplace/apps/insights` → `https://nexelya.cloud/marketplace/apps/insights`

### Configuration Files
17. **`apps/crm/crm/fcrm/doctype/crm_form_script/crm_form_script.json`**
    - Changed: Documentation URL from `https://docs.frappe.io/crm/custom-actions` → `https://docs.nexelya.io/crm/custom-actions`

## URL Mapping

| Old URL | New URL |
|---------|---------|
| `https://frappe.io/*` | `https://nexelya.io/*` |
| `https://frappe.cloud/*` | `https://nexelya.cloud/*` |
| `https://frappecloud.com/*` | `https://nexelyacloud.com/*` |
| `https://docs.frappe.io/*` | `https://docs.nexelya.io/*` |
| `https://support.frappe.io` | `https://support.nexelya.io` |
| `https://discuss.frappe.io/*` | `https://discuss.nexelya.io/*` |
| `https://github.com/frappe/*` | `https://github.com/nexelya/*` |
| `https://t.me/frappecrm` | `https://t.me/nexelyacrm` |
| `https://x.com/frappetech` | `https://x.com/nexelyatech` |

## Branding Changes

- **Company Name**: "Frappe Technologies Pvt. Ltd." → "Nexelya Technologies Pvt. Ltd."
- **Product Name**: "Frappe CRM" → "Nexelya CRM"
- **Email**: "shariq@frappe.io" → "support@nexelya.io"
- **Cloud Service**: "Frappe Cloud" → "Nexelya Cloud"

## Notes

- Locale files (`.po` files) contain email addresses in metadata headers - these are typically auto-generated and may be updated during translation processes
- Compiled JavaScript files in `public/frontend/assets/` may contain old references - these will be regenerated on next build
- Node modules dependencies (like `frappe-ui`) are external packages and should not be modified
- Some references in minified/bundled files will be updated when the frontend is rebuilt

## Next Steps

1. Rebuild frontend assets: `cd apps/crm/frontend && yarn build`
2. Clear browser cache and test all links
3. Update any external documentation or marketing materials
4. Verify all URLs are accessible and working
5. Update DNS records if custom domains are being used

