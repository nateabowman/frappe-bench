# ignitr_brand/ignitr_brand/overrides.py
import frappe
from frappe.desk.page.desktop import get_context as _get_context
from frappe.www.login import get_context as _get_login_context
from frappe import _

@frappe.whitelist()
def get_desktop_context():
    # Call the core method
    context = _get_context()
    # Filter out any icon whose label is exactly "Ignitr ERP Integrations"
    context["icons"] = [
        icon for icon in context.get("icons", [])
        if icon.get("label") != "Ignitr ERP Integrations"
    ]
    return context

def get_login_context(context=None):
    """Override login context to use branded app name"""
    # Call the original function (it accepts context as parameter)
    if context is None:
        context = {}
    context = _get_login_context(context)
    
    # Override app_name if it's still "Frappe" - use Nexelya
    app_name = context.get("app_name", "")
    if app_name == "Frappe" or app_name == _("Frappe") or not app_name:
        context["app_name"] = (
            frappe.get_website_settings("app_name") 
            or frappe.get_system_settings("app_name") 
            or "Nexelya"
        )
    
    return context
