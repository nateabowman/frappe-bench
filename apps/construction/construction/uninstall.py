import frappe


def before_uninstall():
	"""Run before uninstallation"""
	# Remove workspace
	if frappe.db.exists("Workspace", "Construction"):
		frappe.delete_doc("Workspace", "Construction", force=True)
	
	# Clean up custom fields
	custom_fields = frappe.get_all(
		"Custom Field",
		filters={"module": "Construction"},
		pluck="name"
	)
	for cf in custom_fields:
		frappe.delete_doc("Custom Field", cf, force=True)
	
	frappe.db.commit()
