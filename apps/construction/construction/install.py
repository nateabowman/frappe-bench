import frappe


def before_install():
	"""Run before installation"""
	pass


def after_install():
	"""Run after installation"""
	create_roles()
	create_default_cost_codes()
	setup_workspace()


def create_roles():
	"""Create construction-specific roles"""
	roles = [
		{
			"role_name": "Construction Manager",
			"desk_access": 1,
			"is_custom": 1,
		},
		{
			"role_name": "Project Superintendent",
			"desk_access": 1,
			"is_custom": 1,
		},
		{
			"role_name": "Field Worker",
			"desk_access": 1,
			"is_custom": 1,
		},
		{
			"role_name": "Subcontractor User",
			"desk_access": 0,
			"is_custom": 1,
		},
		{
			"role_name": "Estimator",
			"desk_access": 1,
			"is_custom": 1,
		},
	]

	for role in roles:
		if not frappe.db.exists("Role", role["role_name"]):
			doc = frappe.new_doc("Role")
			doc.update(role)
			doc.insert(ignore_permissions=True)
	
	frappe.db.commit()


def create_default_cost_codes():
	"""Create default CSI MasterFormat cost codes"""
	# Only create if Cost Code doctype exists and no codes exist
	if not frappe.db.exists("DocType", "Cost Code"):
		return
	
	if frappe.db.count("Cost Code") > 0:
		return

	# CSI MasterFormat Division structure
	divisions = [
		{"code": "01", "name": "General Requirements", "is_group": 1},
		{"code": "02", "name": "Existing Conditions", "is_group": 1},
		{"code": "03", "name": "Concrete", "is_group": 1},
		{"code": "04", "name": "Masonry", "is_group": 1},
		{"code": "05", "name": "Metals", "is_group": 1},
		{"code": "06", "name": "Wood, Plastics, Composites", "is_group": 1},
		{"code": "07", "name": "Thermal and Moisture Protection", "is_group": 1},
		{"code": "08", "name": "Openings", "is_group": 1},
		{"code": "09", "name": "Finishes", "is_group": 1},
		{"code": "10", "name": "Specialties", "is_group": 1},
		{"code": "11", "name": "Equipment", "is_group": 1},
		{"code": "12", "name": "Furnishings", "is_group": 1},
		{"code": "13", "name": "Special Construction", "is_group": 1},
		{"code": "14", "name": "Conveying Equipment", "is_group": 1},
		{"code": "21", "name": "Fire Suppression", "is_group": 1},
		{"code": "22", "name": "Plumbing", "is_group": 1},
		{"code": "23", "name": "HVAC", "is_group": 1},
		{"code": "26", "name": "Electrical", "is_group": 1},
		{"code": "27", "name": "Communications", "is_group": 1},
		{"code": "28", "name": "Electronic Safety and Security", "is_group": 1},
		{"code": "31", "name": "Earthwork", "is_group": 1},
		{"code": "32", "name": "Exterior Improvements", "is_group": 1},
		{"code": "33", "name": "Utilities", "is_group": 1},
	]

	for div in divisions:
		doc = frappe.new_doc("Cost Code")
		doc.cost_code = div["code"]
		doc.cost_code_name = div["name"]
		doc.is_group = div.get("is_group", 0)
		doc.insert(ignore_permissions=True)

	frappe.db.commit()


def setup_workspace():
	"""Setup construction workspace"""
	if frappe.db.exists("Workspace", "Construction"):
		return

	workspace = frappe.new_doc("Workspace")
	workspace.name = "Construction"
	workspace.label = "Construction"
	workspace.module = "Construction"
	workspace.icon = "building"
	workspace.is_standard = 0
	
	# Add shortcuts
	workspace.append("shortcuts", {
		"label": "Job Sites",
		"link_to": "Job Site",
		"type": "DocType",
	})
	workspace.append("shortcuts", {
		"label": "Daily Field Reports",
		"link_to": "Daily Field Report",
		"type": "DocType",
	})
	workspace.append("shortcuts", {
		"label": "Punch Lists",
		"link_to": "Punch List",
		"type": "DocType",
	})
	workspace.append("shortcuts", {
		"label": "RFIs",
		"link_to": "RFI",
		"type": "DocType",
	})

	try:
		workspace.insert(ignore_permissions=True)
	except Exception:
		pass
