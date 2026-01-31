import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import today


class PunchList(Document):
	def validate(self):
		self.calculate_completion()

	def calculate_completion(self):
		"""Calculate completion metrics"""
		self.total_items = len(self.items)
		self.completed_items = len([i for i in self.items if i.status == "Completed"])
		
		if self.total_items:
			self.percent_complete = (self.completed_items / self.total_items) * 100
		else:
			self.percent_complete = 0
		
		# Auto-update status
		if self.percent_complete == 100 and self.total_items > 0:
			self.status = "Completed"
			if not self.completion_date:
				self.completion_date = today()
		elif self.percent_complete > 0:
			self.status = "In Progress"

	def on_update(self):
		"""Notify assignees of changes"""
		self.send_notifications()

	def send_notifications(self):
		"""Send notifications to assigned parties"""
		settings = frappe.get_single("Construction Settings")
		if not settings.auto_notify_punch_list_assignee:
			return
		
		# Get recipient
		recipient = None
		if self.assigned_to_type == "Subcontractor" and self.assigned_subcontractor:
			recipient = frappe.db.get_value("Supplier", self.assigned_subcontractor, "email_id")
		elif self.assigned_to_type == "Employee" and self.assigned_employee:
			recipient = frappe.db.get_value("Employee", self.assigned_employee, "company_email")
		
		if recipient and self.has_value_changed("items"):
			frappe.sendmail(
				recipients=[recipient],
				subject=f"Punch List Updated: {self.punch_list_name}",
				message=f"""
					<p>The punch list <strong>{self.punch_list_name}</strong> has been updated.</p>
					<p>Job Site: {self.job_site}</p>
					<p>Due Date: {self.due_date}</p>
					<p>Total Items: {self.total_items}</p>
					<p>Completed: {self.completed_items}</p>
				""",
			)


@frappe.whitelist()
def batch_complete_items(items):
	"""Batch complete multiple punch items"""
	import json
	if isinstance(items, str):
		items = json.loads(items)
	
	completed = 0
	for item in items:
		frappe.db.set_value("Punch List Item", item, {
			"status": "Completed",
			"completed_date": today(),
			"completed_by": frappe.session.user,
		})
		completed += 1
	
	frappe.db.commit()
	return {"completed": completed}


@frappe.whitelist()
def get_punch_list_summary(job_site):
	"""Get punch list summary for a job site"""
	lists = frappe.get_all(
		"Punch List",
		filters={"job_site": job_site},
		fields=["name", "punch_list_name", "status", "total_items", "completed_items", "percent_complete", "due_date"]
	)
	
	# Get total open items across all lists
	open_items = frappe.db.sql("""
		SELECT COUNT(*) as count
		FROM `tabPunch List Item` pli
		JOIN `tabPunch List` pl ON pl.name = pli.parent
		WHERE pl.job_site = %s AND pli.status != 'Completed'
	""", job_site, as_dict=True)[0].count
	
	return {
		"lists": lists,
		"total_lists": len(lists),
		"open_items": open_items,
	}
