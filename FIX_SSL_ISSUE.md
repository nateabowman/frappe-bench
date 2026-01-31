# Fixing "Not Secure" Issue for prod.nexelya.com

The certificate for prod.nexelya.com is valid (expires Apr 11, 2026), but the browser may show "not secure" due to:

1. **OCSP Stapling Configuration Issue** - The nginx config has `ssl_stapling_verify on;` but is missing `ssl_trusted_certificate`, which can cause OCSP stapling verification to fail.

2. **Browser Cache** - The browser may be caching an old certificate.

## Quick Fix

Run this script to fix the OCSP stapling configuration:

```bash
cd /home/ubuntu/frappe-bench
sudo ./fix_nginx_ocsp.sh
```

This will:
- Add `ssl_trusted_certificate` to all SSL server blocks
- Test nginx configuration
- Reload nginx

## After Running the Fix

1. **Clear browser cache** or use incognito/private mode
2. **Check browser console** for any mixed content warnings (HTTP resources loading on HTTPS pages)
3. **Wait a few minutes** for OCSP stapling to populate

## Verify the Fix

Check if OCSP stapling is working:

```bash
echo | openssl s_client -connect prod.nexelya.com:443 -servername prod.nexelya.com -status 2>&1 | grep -A 5 "OCSP response"
```

You should see "OCSP response: OCSP Response Status: successful" instead of "OCSP response: no response sent".

## Alternative: Disable OCSP Stapling Verification

If the issue persists and you don't need OCSP stapling verification, you can disable it:

1. Edit `/home/ubuntu/frappe-bench/config/nginx.conf`
2. Change `ssl_stapling_verify on;` to `ssl_stapling_verify off;`
3. Run `bench setup nginx --yes` (as ubuntu user)
4. Copy config and reload nginx (as root)

However, it's recommended to keep OCSP stapling enabled with proper configuration.
