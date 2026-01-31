# Fix: Module Onboarding Documentation URL Error

This error occurs because Frappe's Module Onboarding feature requires a documentation URL for each module. Here are two ways to fix it:

## Solution 1: Disable Onboarding (Quick Fix)

1. Log in to your Frappe/ERPNext instance
2. Go to **Setup** → **System Settings**
3. Find the **Enable Onboarding** option
4. **Uncheck** it
5. Save

This will disable the onboarding feature and prevent the error.

## Solution 2: Add Documentation URL to Module Onboarding (Proper Fix)

1. Log in to your Frappe/ERPNext instance
2. Go to **Module Onboarding** list: `/app/module-onboarding`
3. Find any records that are missing the **Documentation URL** field
4. Add a valid URL (can be your app's GitHub repo, documentation site, or even `https://example.com`)
5. Save each record

## Solution 3: Fix via Console (For System Administrators)

Run this in bench console to fix all Module Onboarding records:

```bash
bench --site prod.nexelya.com console
```

Then in the Python console:

```python
import frappe

# Get all Module Onboarding records missing documentation_url
onboardings = frappe.get_all("Module Onboarding", 
    filters={"documentation_url": ["in", ["", None]]},
    fields=["name"])

# Update them with a default URL
for onboarding in onboardings:
    doc = frappe.get_doc("Module Onboarding", onboarding.name)
    doc.documentation_url = "https://github.com/your-org/modern_erp_ui"  # Update with your URL
    doc.save()

print(f"Updated {len(onboardings)} Module Onboarding records")
```

## Solution 4: Skip Onboarding During Installation

If you want to install the app without dealing with onboarding:

```bash
# Install app with skip_onboarding flag (if available in your Frappe version)
bench --site prod.nexelya.com install-app modern_erp_ui --skip-onboarding
```

Or simply disable onboarding before installation, then re-enable it after if needed.

## Recommended Approach

**For now, use Solution 1** (disable onboarding) to get the app installed, then you can:
- Re-enable onboarding later if needed
- Add proper documentation URLs to Module Onboarding records
- Or leave it disabled if you don't need the onboarding feature

The app will work perfectly fine with onboarding disabled - it's just a feature to help new users get started with modules.

