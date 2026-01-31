import frappe


def get_notification_config():
	"""Return notification configuration for Construction app"""
	return {
		"for_doctype": {
			"Job Site": {"status": ["!=", "Completed"]},
			"RFI": {"status": "Open"},
			"Submittal": {"status": ["in", ["Open", "Pending Review"]]},
			"Punch List": {"status": ["!=", "Completed"]},
			"Change Order Request": {"status": "Pending"},
			"Daily Field Report": {"docstatus": 0},
			"Site Inspection": {"status": "Failed"},
		},
		"for_module_doctypes": {
			"Construction": [
				"Job Site",
				"Cost Code",
				"Budget Line",
				"Job Cost Entry",
				"Construction Phase",
			],
			"Field": [
				"Daily Field Report",
				"Punch List",
				"Site Inspection",
			],
			"Scheduling": [
				"Gantt Schedule",
				"Schedule Activity",
			],
			"Documents": [
				"Drawing Set",
				"Drawing Sheet",
			],
		},
	}


@frappe.whitelist()
def get_construction_notifications():
	"""Get notification counts for construction dashboard"""
	return {
		"open_rfis": frappe.db.count("RFI", {"status": "Open"}),
		"pending_submittals": frappe.db.count("Submittal", {"status": ["in", ["Open", "Pending Review"]]}),
		"open_punch_items": frappe.db.count("Punch List Item", {"status": ["!=", "Completed"]}),
		"pending_change_orders": frappe.db.count("Change Order Request", {"status": "Pending"}),
		"overdue_tasks": frappe.db.count("Task", {
			"status": ["not in", ["Completed", "Cancelled"]],
			"exp_end_date": ["<", frappe.utils.today()],
		}),
	}
