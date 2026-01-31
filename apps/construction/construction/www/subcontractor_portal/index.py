import frappe

def get_context(context):
	context.no_cache = 1
	
	if frappe.session.user == "Guest":
		frappe.local.flags.redirect_location = "/login"
		raise frappe.Redirect
	
	# Check if user has subcontractor role
	if "Subcontractor User" not in frappe.get_roles():
		frappe.throw("Access Denied", frappe.PermissionError)
	
	return context
