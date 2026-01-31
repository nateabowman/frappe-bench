#!/usr/bin/env python3
"""
Quick fix for Module Onboarding Documentation URL error.
This script fixes all existing records and reloads the doctype.
Run: bench --site <site_name> console
Then: exec(open('fix_onboarding_quick.py').read())
"""

import frappe

def fix_all_onboarding_records():
    """Fix all Module Onboarding records missing documentation_url"""
    
    # Get all records
    records = frappe.get_all("Module Onboarding", fields=["name", "documentation_url", "module"])
    
    print(f"Found {len(records)} Module Onboarding records")
    
    fixed = 0
    for record in records:
        doc = frappe.get_doc("Module Onboarding", record.name)
        
        if not doc.documentation_url or (doc.documentation_url and doc.documentation_url.strip() == ""):
            # Set a default URL based on module
            module = doc.module or "general"
            default_url = f"https://docs.erpnext.com/docs/user/manual/en/{module.lower().replace(' ', '-')}"
            
            doc.db_set("documentation_url", default_url, update_modified=False)
            print(f"✓ Fixed: {doc.name} (Module: {module})")
            fixed += 1
    
    frappe.db.commit()
    print(f"\n✅ Fixed {fixed} records")
    
    # Reload doctype to pick up the JSON change
    frappe.reload_doc("desk", "doctype", "module_onboarding")
    print("✅ Reloaded Module Onboarding doctype")
    
    return fixed

# Run the fix
if __name__ == "__main__" or True:
    print("=" * 60)
    print("Fixing Module Onboarding Documentation URL Error")
    print("=" * 60)
    fix_all_onboarding_records()
    print("\n✅ Done! The error should be resolved now.")

