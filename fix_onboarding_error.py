#!/usr/bin/env python3
"""
Fix Module Onboarding Documentation URL Error

This script fixes the "Value missing for Module Onboarding: Documentation URL" error
by either:
1. Setting a default Documentation URL for all Module Onboarding records missing it
2. Or disabling onboarding for modules without Documentation URL

Run this script using: bench --site <site_name> console
Then execute: exec(open('fix_onboarding_error.py').read())
"""

import frappe

def fix_onboarding_documentation_url():
    """Fix missing Documentation URL in Module Onboarding records"""
    
    # Get all Module Onboarding records
    onboarding_records = frappe.get_all(
        "Module Onboarding",
        fields=["name", "documentation_url", "module"],
        filters={}
    )
    
    print(f"Found {len(onboarding_records)} Module Onboarding records")
    
    fixed_count = 0
    for record in onboarding_records:
        doc = frappe.get_doc("Module Onboarding", record.name)
        
        # Check if Documentation URL is missing or empty
        if not doc.documentation_url or doc.documentation_url.strip() == "":
            # Option 1: Set a default documentation URL
            # You can customize this URL pattern
            module_name = doc.module or "general"
            default_url = f"https://docs.erpnext.com/docs/user/manual/en/{module_name.lower().replace(' ', '-')}"
            
            doc.documentation_url = default_url
            doc.save(ignore_permissions=True)
            frappe.db.commit()
            
            print(f"✓ Fixed: {record.name} (Module: {doc.module}) - Set URL to: {default_url}")
            fixed_count += 1
        else:
            print(f"✓ OK: {record.name} (Module: {doc.module}) - URL already set")
    
    print(f"\n✅ Fixed {fixed_count} records")
    return fixed_count

def disable_onboarding_for_missing_urls():
    """Disable onboarding for modules without Documentation URL"""
    
    onboarding_records = frappe.get_all(
        "Module Onboarding",
        fields=["name", "documentation_url", "module"],
        filters={}
    )
    
    disabled_count = 0
    for record in onboarding_records:
        doc = frappe.get_doc("Module Onboarding", record.name)
        
        if not doc.documentation_url or doc.documentation_url.strip() == "":
            # Disable the onboarding record
            doc.disabled = 1
            doc.save(ignore_permissions=True)
            frappe.db.commit()
            
            print(f"✓ Disabled: {record.name} (Module: {doc.module}) - Missing Documentation URL")
            disabled_count += 1
    
    print(f"\n✅ Disabled {disabled_count} records")
    return disabled_count

def check_onboarding_settings():
    """Check if onboarding is enabled globally"""
    try:
        settings = frappe.get_single("System Settings")
        if hasattr(settings, 'enable_onboarding'):
            print(f"Global onboarding setting: {settings.enable_onboarding}")
            return settings.enable_onboarding
    except:
        pass
    return None

if __name__ == "__main__":
    print("=" * 60)
    print("Module Onboarding Documentation URL Fix")
    print("=" * 60)
    
    # Check global settings
    check_onboarding_settings()
    
    print("\nChoose an option:")
    print("1. Fix missing URLs (set default URLs)")
    print("2. Disable onboarding for modules without URLs")
    print("3. Just check current status")
    
    # For automated execution, we'll fix missing URLs
    # Uncomment the line below to disable instead:
    # disable_onboarding_for_missing_urls()
    
    fix_onboarding_documentation_url()

