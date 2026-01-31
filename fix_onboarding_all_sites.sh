#!/bin/bash
# Fix Module Onboarding Documentation URL error for all sites

echo "🔧 Fixing Module Onboarding Documentation URL error for all sites..."
echo ""

# Get all sites
SITES=$(ls -d sites/*/site_config.json 2>/dev/null | sed 's|sites/||; s|/site_config.json||' | grep -v "^$")

if [ -z "$SITES" ]; then
    echo "No sites found!"
    exit 1
fi

for SITE in $SITES; do
    echo "Processing site: $SITE"
    echo "----------------------------------------"
    
    # Clear cache and reload doctype
    bench --site "$SITE" clear-cache
    bench --site "$SITE" migrate
    
    # Run the fix script
    bench --site "$SITE" console <<EOF
exec(open('fix_onboarding_quick.py').read())
EOF
    
    echo "✅ Fixed site: $SITE"
    echo ""
done

echo "🎉 All sites have been fixed!"

