"""Subcontractor Portal API"""
import frappe
from frappe import _


def get_linked_supplier():
	"""Get the supplier linked to the current user"""
	supplier = frappe.db.get_value(
		"Supplier",
		{"email_id": frappe.session.user},
		"name"
	)
	return supplier


@frappe.whitelist()
def get_subcontractor_stats():
	"""Get statistics for subcontractor dashboard"""
	supplier = get_linked_supplier()
	if not supplier:
		return {}
	
	# Open punch items assigned to this subcontractor
	open_punch = frappe.db.sql("""
		SELECT COUNT(*) as count
		FROM `tabPunch List Item` pli
		JOIN `tabPunch List` pl ON pl.name = pli.parent
		WHERE pl.assigned_subcontractor = %s
		AND pli.status != 'Completed'
	""", supplier, as_dict=True)[0].count
	
	# Pending submittals
	pending_submittals = frappe.db.count("Submittal", {
		"submitted_by": supplier,
		"status": ["in", ["Open", "Pending Review"]]
	})
	
	# Open RFIs
	open_rfis = frappe.db.count("RFI", {
		"ball_in_court": "Subcontractor",
		"status": "Open"
	})
	
	return {
		"open_punch_items": open_punch,
		"pending_submittals": pending_submittals,
		"open_rfis": open_rfis,
	}


@frappe.whitelist()
def get_my_assignments():
	"""Get punch lists assigned to this subcontractor"""
	supplier = get_linked_supplier()
	if not supplier:
		return []
	
	punch_lists = frappe.get_all(
		"Punch List",
		filters={"assigned_subcontractor": supplier},
		fields=["name", "punch_list_name", "job_site", "status", "due_date", "percent_complete"]
	)
	
	for pl in punch_lists:
		pl["job_site_name"] = frappe.db.get_value("Job Site", pl["job_site"], "job_name")
		pl["items"] = frappe.get_all(
			"Punch List Item",
			filters={"parent": pl["name"], "status": ["!=", "Completed"]},
			fields=["description", "priority", "status"]
		)
	
	return punch_lists


@frappe.whitelist()
def get_my_documents(job_site=None):
	"""Get documents accessible to this subcontractor"""
	supplier = get_linked_supplier()
	if not supplier:
		return []
	
	# Get job sites this subcontractor is working on
	if not job_site:
		job_sites = frappe.db.sql("""
			SELECT DISTINCT pl.job_site
			FROM `tabPunch List` pl
			WHERE pl.assigned_subcontractor = %s
		""", supplier, as_list=True)
		job_sites = [js[0] for js in job_sites]
	else:
		job_sites = [job_site]
	
	# Get drawing sets for these job sites
	drawings = frappe.get_all(
		"Drawing Set",
		filters={"job_site": ["in", job_sites], "status": "Current"},
		fields=["name", "set_name", "job_site", "discipline", "revision", "issue_date"]
	)
	
	return drawings


@frappe.whitelist()
def get_my_submittals():
	"""Get submittals submitted by this subcontractor"""
	supplier = get_linked_supplier()
	if not supplier:
		return []
	
	return frappe.get_all(
		"Submittal",
		filters={"submitted_by": supplier},
		fields=[
			"name", "subject", "project", "status", "review_status",
			"submission_date", "due_date"
		],
		order_by="submission_date desc"
	)


@frappe.whitelist()
def submit_submittal(project, subject, spec_section, file_url, description=None):
	"""Submit a new submittal"""
	supplier = get_linked_supplier()
	if not supplier:
		frappe.throw(_("Subcontractor account not found"))
	
	doc = frappe.new_doc("Submittal")
	doc.project = project
	doc.subject = subject
	doc.spec_section = spec_section
	doc.description = description
	doc.submitted_by = supplier
	doc.submission_date = frappe.utils.today()
	doc.status = "Open"
	
	# Attach file
	if file_url:
		doc.append("attachments", {"file": file_url})
	
	doc.insert(ignore_permissions=True)
	
	return doc.name


@frappe.whitelist()
def get_my_rfis():
	"""Get RFIs assigned to subcontractor for response"""
	return frappe.get_all(
		"RFI",
		filters={"ball_in_court": "Subcontractor", "status": "Open"},
		fields=[
			"name", "subject", "project", "requested_date", "due_date",
			"description", "days_open", "is_overdue"
		],
		order_by="due_date"
	)


@frappe.whitelist()
def respond_to_rfi(rfi_name, response):
	"""Submit a response to an RFI"""
	supplier = get_linked_supplier()
	if not supplier:
		frappe.throw(_("Subcontractor account not found"))
	
	doc = frappe.get_doc("RFI", rfi_name)
	doc.response = response
	doc.responded_by = frappe.session.user
	doc.responded_date = frappe.utils.today()
	doc.ball_in_court = "Contractor"
	doc.save(ignore_permissions=True)
	
	return {"success": True}


@frappe.whitelist()
def submit_daily_report(job_site, work_performed, man_hours, notes=None):
	"""Submit a daily report from subcontractor"""
	supplier = get_linked_supplier()
	if not supplier:
		frappe.throw(_("Subcontractor account not found"))
	
	doc = frappe.new_doc("Daily Field Report")
	doc.job_site = job_site
	doc.report_date = frappe.utils.today()
	doc.submitted_by = frappe.session.user
	doc.work_performed = work_performed
	doc.total_man_hours = man_hours
	doc.subcontractors_on_site = supplier
	doc.notes = notes
	doc.insert(ignore_permissions=True)
	
	return doc.name


@frappe.whitelist()
def complete_punch_item(item_name):
	"""Mark a punch item as complete"""
	supplier = get_linked_supplier()
	if not supplier:
		frappe.throw(_("Subcontractor account not found"))
	
	# Verify this item is assigned to this subcontractor
	item = frappe.get_doc("Punch List Item", item_name)
	punch_list = frappe.get_doc("Punch List", item.parent)
	
	if punch_list.assigned_subcontractor != supplier:
		frappe.throw(_("This item is not assigned to you"))
	
	item.status = "Completed"
	item.completed_date = frappe.utils.today()
	item.completed_by = frappe.session.user
	item.save(ignore_permissions=True)
	
	# Update parent
	punch_list.save(ignore_permissions=True)
	
	return {"success": True}
