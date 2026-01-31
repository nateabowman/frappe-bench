import frappe


def check_app_permission():
	"""Check if user has permission to access Construction app"""
	if frappe.session.user == "Administrator":
		return True
	
	# Check for construction-specific roles
	construction_roles = [
		"Construction Manager",
		"Project Superintendent",
		"Field Worker",
		"Estimator",
		"Projects Manager",
		"Projects User",
	]
	
	user_roles = frappe.get_roles(frappe.session.user)
	return any(role in user_roles for role in construction_roles)


@frappe.whitelist()
def get_user_permissions():
	"""Get construction permissions for current user"""
	return {
		"can_create_job_site": frappe.has_permission("Job Site", "create"),
		"can_create_daily_report": frappe.has_permission("Daily Field Report", "create"),
		"can_create_punch_list": frappe.has_permission("Punch List", "create"),
		"can_approve_change_orders": "Construction Manager" in frappe.get_roles(),
		"is_field_worker": "Field Worker" in frappe.get_roles(),
		"is_superintendent": "Project Superintendent" in frappe.get_roles(),
	}
