# -*- coding: utf-8 -*-
"""
Ignitr Branding Utilities
"""
import frappe

def get_branded_app_name():
    """Get branded app name"""
    return (
        frappe.get_website_settings("app_name") 
        or frappe.get_system_settings("app_name") 
        or "Nexelya"
    )

def override_login_context(context):
    """Override login page context to use branded name"""
    if context.get("app_name") == "Frappe":
        context["app_name"] = get_branded_app_name()
    return context

