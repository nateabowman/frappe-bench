#!/bin/bash
# Fix Module Onboarding Documentation URL Error
# This script connects to the server and fixes the error

BENCH_PATH="/home/ubuntu/frappe-bench"
SITE_NAME="${1:-}"  # Get site name from first argument

if [ -z "$SITE_NAME" ]; then
    echo "Usage: $0 <site_name>"
    echo "Example: $0 site1.local"
    exit 1
fi

cd "$BENCH_PATH" || exit 1

echo "🔧 Fixing Module Onboarding Documentation URL error..."
echo "Site: $SITE_NAME"
echo ""

# Option 1: Fix using bench console
echo "Running fix script via bench console..."
bench --site "$SITE_NAME" console << 'PYTHON_SCRIPT'
import frappe

def fix_onboarding_documentation_url():
    """Fix missing Documentation URL in Module Onboarding records"""
    onboarding_records = frappe.get_all(
        "Module Onboarding",
        fields=["name", "documentation_url", "module_name"],
        filters={}
    )
    
    print(f"Found {len(onboarding_records)} Module Onboarding records\n")
    
    fixed_count = 0
    for record in onboarding_records:
        doc = frappe.get_doc("Module Onboarding", record.name)
        
        if not doc.documentation_url or doc.documentation_url.strip() == "":
            # Set a default documentation URL
            default_url = f"https://docs.erpnext.com/docs/user/manual/en/{doc.module_name.lower().replace(' ', '-')}"
            doc.documentation_url = default_url
            doc.save(ignore_permissions=True)
            frappe.db.commit()
            
            print(f"✓ Fixed: {record.name} (Module: {doc.module_name})")
            fixed_count += 1
        else:
            print(f"✓ OK: {record.name} (Module: {doc.module_name})")
    
    print(f"\n✅ Fixed {fixed_count} records")
    return fixed_count

# Execute the fix
fix_onboarding_documentation_url()
PYTHON_SCRIPT

echo ""
echo "✅ Fix completed!"
echo ""
echo "Alternative: If you want to disable onboarding instead, run:"
echo "  bench --site $SITE_NAME console"
echo "  Then execute:"
echo "  frappe.db.set_value('System Settings', 'System Settings', 'enable_onboarding', 0)"
echo "  frappe.db.commit()"

