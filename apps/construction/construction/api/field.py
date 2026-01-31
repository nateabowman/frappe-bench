import frappe
from frappe.utils import today


@frappe.whitelist()
def get_daily_logs(job_site=None, limit=20):
	"""Get daily logs for field app"""
	filters = {"submitted_by": frappe.session.user}
	if job_site:
		filters["job_site"] = job_site
	
	logs = frappe.get_all(
		"Daily Field Report",
		filters=filters,
		fields=[
			"name", "job_site", "report_date", "status",
			"weather_condition", "temperature", "total_man_hours"
		],
		order_by="report_date desc",
		limit=limit
	)
	
	# Add job site names
	for log in logs:
		log["job_site_name"] = frappe.db.get_value("Job Site", log["job_site"], "job_name")
	
	return logs


@frappe.whitelist()
def get_user_job_sites():
	"""Get job sites accessible by current user"""
	user = frappe.session.user
	
	# Get job sites where user is on the team
	sites = frappe.db.sql("""
		SELECT DISTINCT js.name, js.job_name, js.status
		FROM `tabJob Site` js
		LEFT JOIN `tabJob Site Team Member` tm ON tm.parent = js.name
		WHERE js.status IN ('Active', 'Pre-Construction', 'Punch List')
		AND (
			js.project_manager = %(user)s
			OR js.superintendent = %(user)s
			OR tm.user = %(user)s
		)
		ORDER BY js.job_name
	""", {"user": user}, as_dict=True)
	
	return sites


@frappe.whitelist()
def get_punch_items(job_site=None, status=None):
	"""Get punch list items for field app"""
	filters = {}
	if job_site:
		filters["parent"] = ["in", frappe.get_all(
			"Punch List", 
			filters={"job_site": job_site}, 
			pluck="name"
		)]
	if status:
		filters["status"] = status
	
	items = frappe.get_all(
		"Punch List Item",
		filters=filters,
		fields=[
			"name", "parent", "description", "trade", "status",
			"priority", "location", "due_date"
		],
		order_by="priority desc, due_date asc",
		limit=100
	)
	
	return items


@frappe.whitelist()
def complete_punch_item(item_name):
	"""Mark a punch list item as complete"""
	frappe.db.set_value("Punch List Item", item_name, {
		"status": "Completed",
		"completed_date": today(),
		"completed_by": frappe.session.user,
	})
	
	# Update parent punch list
	parent = frappe.db.get_value("Punch List Item", item_name, "parent")
	if parent:
		doc = frappe.get_doc("Punch List", parent)
		doc.save()
	
	return {"success": True}


@frappe.whitelist()
def create_daily_log(job_site, work_performed, weather_condition=None, temperature=None, **kwargs):
	"""Create a daily log from mobile app"""
	doc = frappe.new_doc("Daily Field Report")
	doc.job_site = job_site
	doc.report_date = today()
	doc.submitted_by = frappe.session.user
	doc.work_performed = work_performed
	doc.weather_condition = weather_condition
	doc.temperature = temperature
	
	# Set optional fields
	for key, value in kwargs.items():
		if hasattr(doc, key):
			setattr(doc, key, value)
	
	doc.insert()
	return doc.as_dict()


@frappe.whitelist()
def upload_photo(doctype, docname, fieldname, file_data):
	"""Upload a photo attachment"""
	from frappe.utils.file_manager import save_file
	
	file_doc = save_file(
		fname=f"{docname}_{fieldname}.jpg",
		content=file_data,
		dt=doctype,
		dn=docname,
		is_private=0
	)
	
	return file_doc.file_url
