# BuildPro - US Construction Company Branding

This document describes the construction-industry specific branding and terminology implemented for US-based construction companies.

## Brand Identity

**Brand Name**: BuildPro Construction Management

The system has been rebranded from Frappe/ERPNext to "BuildPro" with construction-industry specific terminology throughout.

## Construction-Specific Terminology

### Module Renaming

| Original Module | Construction Term |
|----------------|------------------|
| Projects | **Job Sites** |
| Buying | **Procurement** |
| Selling | **Estimating & Billing** |
| Stock | **Materials & Inventory** |
| Warehouse | **Yard** |
| Manufacturing | **Prefab & Modular** |
| Assets | **Equipment & Fleet** |
| Maintenance | **Equipment Maintenance** |
| Support | **Client Support** |
| CRM | **Client Relations** |

### Document/Entity Renaming

| Original Term | Construction Term |
|---------------|------------------|
| Customer | **Client** |
| Supplier | **Vendor** |
| Sales Order | **Contract** |
| Quotation | **Estimate** |
| Sales Invoice | **Invoice** |
| Delivery Note | **Delivery Ticket** |
| Item | **Material** |
| Timesheet | **Time Card** |
| Employee | **Crew Member** |

## Color Scheme

The construction theme uses industry-appropriate colors:

- **Primary Color**: Safety Orange (#FF6B35) - Used for primary actions, highlights
- **Secondary Color**: Professional Blue (#004E89) - Used for secondary actions, headers
- **Accent Color**: Construction Yellow (#FFA500) - Used for warnings, highlights
- **Success Color**: Safety Green (#2E7D32) - Used for completed statuses
- **Warning Color**: Caution Orange (#F57C00) - Used for alerts, warnings
- **Dark**: Dark Gray (#1A1A1A) - Used for text, borders

## Visual Styling

### Login Page
- Construction-themed gradient background
- Orange accent border on login card
- Professional, clean design

### Navigation
- Orange accent border on navbar
- Professional logo display
- Construction-themed module cards with colored left borders

### Module Cards
- **Job Sites** (Projects): Green left border
- **Equipment & Fleet** (Assets): Orange left border
- **Other modules**: Orange left border
- Hover effects with elevation

### Tables & Forms
- Blue headers for data tables
- Orange focus states on form controls
- Construction-themed alert styling

## Setup Instructions

### 1. Configure App Name

Go to **System Settings**:
- Set **App Name** to "BuildPro" or your construction company name

Go to **Navbar Settings**:
- Upload your construction company logo
- This will appear in the navbar and login page

### 2. Customize Brand Name (Optional)

If you want to use a different brand name than "BuildPro":

1. Edit `/apps/ignitr_brand/ignitr_brand/public/js/brand.js`
2. Replace all instances of "BuildPro" with your brand name
3. Edit `/apps/ignitr_brand/ignitr_brand/translations/en.csv`
4. Update the translations accordingly

### 3. Customize Colors (Optional)

To change the construction color scheme:

1. Edit `/apps/ignitr_brand/ignitr_brand/public/css/ignitr_brand.css`
2. Update the CSS variables in the `:root` section:
   ```css
   :root {
     --construction-primary: #YOUR_COLOR;
     --construction-secondary: #YOUR_COLOR;
     /* etc. */
   }
   ```

### 4. Clear Cache

After making changes:
```bash
bench --site <your-site> clear-cache
```

## Construction Industry Features

The rebranding maintains all ERPNext functionality while presenting it in construction-industry terms:

- **Job Site Management** (Projects) - Track construction projects
- **Procurement** (Buying) - Manage material and equipment purchases
- **Estimating & Billing** (Selling) - Create estimates and invoices
- **Materials & Inventory** (Stock) - Track construction materials
- **Yard Management** (Warehouse) - Manage storage yards
- **Equipment & Fleet** (Assets) - Track construction equipment
- **Time Cards** (Timesheets) - Track crew hours
- **Crew Management** (HR) - Manage construction workforce
- **Client Relations** (CRM) - Manage client relationships

## Testing Checklist

- [ ] Login page shows "Login to BuildPro"
- [ ] Navbar displays construction company logo
- [ ] Module cards show construction terminology (Job Sites, Equipment & Fleet, etc.)
- [ ] Documents use construction terms (Client, Vendor, Contract, Estimate, etc.)
- [ ] Colors match construction theme (orange, blue accents)
- [ ] Footer does not show "Powered by" text
- [ ] All Frappe/ERPNext references are replaced

## Support

For construction-specific customizations:
1. Check browser console for JavaScript errors
2. Verify all files are in correct locations
3. Clear cache after making changes
4. Check System Settings for app name configuration

## Notes

- The rebranding works on both desk and website views
- JavaScript replacements happen in real-time
- Some hardcoded references in minified JS may not be replaceable
- Module names in the sidebar are controlled by translations
- Document types maintain their internal names but display with construction terminology

