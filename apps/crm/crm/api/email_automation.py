import frappe
from frappe import _
from frappe.utils import now, add_days, getdate
import json


@frappe.whitelist()
def create_email_sequence(name, steps):
	"""
	Create an email sequence/drip campaign
	"""
	# Check permissions - only Sales Manager or System Manager can create sequences
	frappe.only_for(["System Manager", "Sales Manager"])
	
	if isinstance(steps, str):
		steps = json.loads(steps)

	sequence = frappe.get_doc({
		"doctype": "CRM Email Sequence",
		"title": name,
		"steps": steps,
		"enabled": True,
	})
	# Permission check done above, safe to use ignore_permissions for system operations
	sequence.insert(ignore_permissions=True)

	return sequence.name


@frappe.whitelist()
def add_recipient_to_sequence(sequence_name, recipient_email, recipient_name=None, reference_doctype=None, reference_docname=None):
	"""
	Add a recipient to an email sequence
	"""
	sequence = frappe.get_doc("CRM Email Sequence", sequence_name)

	# Check permissions - user must have read access to the sequence
	if not frappe.has_permission("CRM Email Sequence", "read", sequence):
		frappe.throw(_("Not permitted to access this email sequence"), frappe.PermissionError)

	if not sequence.enabled:
		frappe.throw(_("Email sequence is not enabled"))

	# Create sequence enrollment
	enrollment = frappe.get_doc({
		"doctype": "CRM Email Sequence Enrollment",
		"email_sequence": sequence_name,
		"recipient_email": recipient_email,
		"recipient_name": recipient_name,
		"reference_doctype": reference_doctype,
		"reference_docname": reference_docname,
		"status": "Active",
		"current_step": 0,
		"next_send_date": now(),
	})
	# Permission checked above, safe for system operation
	enrollment.insert(ignore_permissions=True)

	# Send first email
	send_sequence_email(enrollment.name)

	return enrollment.name


@frappe.whitelist()
def send_sequence_email(enrollment_name):
	"""
	Send the next email in a sequence
	"""
	enrollment = frappe.get_doc("CRM Email Sequence Enrollment", enrollment_name)
	sequence = frappe.get_doc("CRM Email Sequence", enrollment.email_sequence)

	# Check permissions - user must have read access to the sequence
	if not frappe.has_permission("CRM Email Sequence", "read", sequence):
		frappe.throw(_("Not permitted to access this email sequence"), frappe.PermissionError)

	if enrollment.status != "Active":
		return {"status": "skipped", "reason": "Enrollment not active"}

	if enrollment.current_step >= len(sequence.steps):
		enrollment.status = "Completed"
		# Permission checked above, safe for system operation
		enrollment.save(ignore_permissions=True)
		return {"status": "completed"}

	step = sequence.steps[enrollment.current_step]

	# Get email template
	template = frappe.get_doc("Email Template", step.template) if step.template else None

	if template:
		# Send email
		frappe.sendmail(
			recipients=[enrollment.recipient_email],
			subject=step.subject or template.subject,
			message=template.response or step.message,
		)

		# Update enrollment
		enrollment.current_step += 1
		if enrollment.current_step < len(sequence.steps):
			enrollment.next_send_date = add_days(now(), step.delay_days or 1)
		else:
			enrollment.status = "Completed"
		# Permission checked above, safe for system operation
		enrollment.save(ignore_permissions=True)

		return {"status": "sent", "step": enrollment.current_step - 1}

	return {"status": "error", "message": "No template found"}


@frappe.whitelist()
def get_email_analytics(sequence_name=None, from_date=None, to_date=None):
	"""
	Get email sequence analytics
	"""
	filters = {}
	if sequence_name:
		filters["email_sequence"] = sequence_name
	if from_date:
		filters["creation"] = [">=", from_date]
	if to_date:
		filters["creation"] = ["<=", to_date]

	enrollments = frappe.get_all(
		"CRM Email Sequence Enrollment",
		filters=filters,
		fields=["name", "status", "email_sequence"],
	)

	total = len(enrollments)
	active = len([e for e in enrollments if e.status == "Active"])
	completed = len([e for e in enrollments if e.status == "Completed"])
	unsubscribed = len([e for e in enrollments if e.status == "Unsubscribed"])

	return {
		"total": total,
		"active": active,
		"completed": completed,
		"unsubscribed": unsubscribed,
		"completion_rate": (completed / total * 100) if total > 0 else 0,
	}

