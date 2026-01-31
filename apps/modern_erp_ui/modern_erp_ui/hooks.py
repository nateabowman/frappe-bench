app_name = "modern_erp_ui"
app_title = "Modern ERP UI"
app_publisher = "Modern ERP UI Team"
app_description = "Modern, contemporary UI theme for ERPNext and Frappe"
app_email = ""
app_license = "mit"
app_version = "1.0.0"
app_url = "https://github.com/your-org/modern_erp_ui"  # Update with your actual URL

# Includes in <head>
# ------------------
import time

# Include CSS and JS in desk.html header
app_include_css = "/assets/modern_erp_ui/css/modern_erp_ui.css?v={}".format(time.time())
app_include_js = "/assets/modern_erp_ui/js/modern_erp_ui.js?v={}".format(time.time())

# Include CSS and JS in web template header
web_include_css = "/assets/modern_erp_ui/css/modern_erp_ui.css?v={}".format(time.time())
web_include_js = "/assets/modern_erp_ui/js/modern_erp_ui.js?v={}".format(time.time())

