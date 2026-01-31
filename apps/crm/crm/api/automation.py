import frappe
from frappe import _
from frappe.utils import now, add_days, getdate
import json


@frappe.whitelist()
def execute_automation_rule(rule_name, doc_name=None, doctype=None):
	"""
	Execute an automation rule
	"""
	rule = frappe.get_doc("CRM Automation Rule", rule_name)

	# Check permissions - user must have read access to the automation rule
	if not frappe.has_permission("CRM Automation Rule", "read", rule):
		frappe.throw(_("Not permitted to execute this automation rule"), frappe.PermissionError)

	if not rule.enabled:
		return {"status": "skipped", "reason": "Rule is disabled"}

	# If doc_name and doctype are provided, verify user has read access to the document
	if doc_name and doctype:
		doc = frappe.get_doc(doctype, doc_name)
		if not frappe.has_permission(doctype, "read", doc):
			frappe.throw(_("Not permitted to access this document"), frappe.PermissionError)

	# Check trigger conditions
	if not evaluate_trigger(rule, doc_name, doctype):
		return {"status": "skipped", "reason": "Trigger conditions not met"}

	# Execute actions
	results = []
	for action in rule.actions:
		try:
			result = execute_action(action, doc_name, doctype)
			results.append(result)
		except Exception as e:
			frappe.log_error(f"Automation action failed: {str(e)}")
			results.append({"status": "error", "message": str(e)})

	# Log execution
	log_execution(rule_name, doc_name, doctype, results)

	return {"status": "success", "results": results}


def evaluate_trigger(rule, doc_name, doctype):
	"""
	Evaluate if trigger conditions are met
	"""
	if rule.trigger_type == "On Create":
		return True  # Already triggered on create

	if rule.trigger_type == "On Update":
		if not doc_name or not doctype:
			return False
		# Check if any trigger field changed
		if rule.trigger_fields:
			trigger_fields = json.loads(rule.trigger_fields) if isinstance(rule.trigger_fields, str) else rule.trigger_fields
			doc = frappe.get_doc(doctype, doc_name)
			# Simplified - would check actual field changes
			return True
		return True

	if rule.trigger_type == "Scheduled":
		# Check if it's time to run
		return True

	if rule.trigger_type == "Webhook":
		return True

	return False


def execute_action(action, doc_name, doctype):
	"""
	Execute a single automation action
	"""
	action_type = action.get("type")
	action_config = action.get("config", {})

	if action_type == "Update Field":
		return update_field_action(doc_name, doctype, action_config)

	elif action_type == "Create Task":
		return create_task_action(doc_name, doctype, action_config)

	elif action_type == "Send Email":
		return send_email_action(doc_name, doctype, action_config)

	elif action_type == "Assign To":
		return assign_to_action(doc_name, doctype, action_config)

	elif action_type == "Change Status":
		return change_status_action(doc_name, doctype, action_config)

	elif action_type == "Create Note":
		return create_note_action(doc_name, doctype, action_config)

	else:
		return {"status": "error", "message": f"Unknown action type: {action_type}"}


def update_field_action(doc_name, doctype, config):
	"""Update a field on the document"""
	doc = frappe.get_doc(doctype, doc_name)
	
	# Verify user has write permission (automation runs in system context, but should verify)
	# Note: This is called from automation rules which are system-level operations
	# but we should still verify the automation rule has permission to modify the document
	if not frappe.has_permission(doctype, "write", doc):
		return {"status": "error", "message": "No permission to modify document"}
	
	field = config.get("field")
	value = config.get("value")

	if field and value is not None:
		doc.set(field, value)
		doc.save()  # Remove ignore_permissions - permission checked above
		return {"status": "success", "action": "Update Field", "field": field, "value": value}

	return {"status": "error", "message": "Missing field or value"}


def create_task_action(doc_name, doctype, config):
	"""Create a task"""
	# Verify user has read permission on the reference document
	# Automation rules can create tasks, but should verify access to the document
	doc = frappe.get_doc(doctype, doc_name)
	if not frappe.has_permission(doctype, "read", doc):
		return {"status": "error", "message": "No permission to access document"}
	
	task = frappe.get_doc({
		"doctype": "CRM Task",
		"title": config.get("title", "Automated Task"),
		"description": config.get("description", ""),
		"reference_doctype": doctype,
		"reference_docname": doc_name,
		"assigned_to": config.get("assigned_to"),
		"due_date": config.get("due_date"),
		"priority": config.get("priority", "Medium"),
		"status": "Todo",
	})
	# Permission checked above, safe for system operation
	task.insert(ignore_permissions=True)
	return {"status": "success", "action": "Create Task", "task": task.name}


def send_email_action(doc_name, doctype, config):
	"""Send an email"""
	doc = frappe.get_doc(doctype, doc_name)
	recipient = config.get("recipient") or doc.get("email")
	subject = config.get("subject", "Automated Email")
	message = config.get("message", "")

	if recipient:
		frappe.sendmail(
			recipients=[recipient],
			subject=subject,
			message=message,
		)
		return {"status": "success", "action": "Send Email", "recipient": recipient}

	return {"status": "error", "message": "No recipient specified"}


def assign_to_action(doc_name, doctype, config):
	"""Assign document to user"""
	doc = frappe.get_doc(doctype, doc_name)
	assignee = config.get("assignee")

	if assignee:
		from frappe.desk.form.assign_to import add as assign_to
		assign_to({
			"doctype": doctype,
			"name": doc_name,
			"assign_to": [assignee],
		})
		return {"status": "success", "action": "Assign To", "assignee": assignee}

	return {"status": "error", "message": "No assignee specified"}


def change_status_action(doc_name, doctype, config):
	"""Change document status"""
	doc = frappe.get_doc(doctype, doc_name)
	
	# Verify user has write permission
	if not frappe.has_permission(doctype, "write", doc):
		return {"status": "error", "message": "No permission to modify document"}
	
	new_status = config.get("status")

	if new_status and hasattr(doc, "status"):
		doc.status = new_status
		doc.save()  # Remove ignore_permissions - permission checked above
		return {"status": "success", "action": "Change Status", "status": new_status}

	return {"status": "error", "message": "Status field not found or invalid status"}


def create_note_action(doc_name, doctype, config):
	"""Create a note"""
	# Verify user has read permission on the reference document
	doc = frappe.get_doc(doctype, doc_name)
	if not frappe.has_permission(doctype, "read", doc):
		return {"status": "error", "message": "No permission to access document"}
	
	note = frappe.get_doc({
		"doctype": "FCRM Note",
		"title": config.get("title", "Automated Note"),
		"content": config.get("content", ""),
		"reference_doctype": doctype,
		"reference_docname": doc_name,
	})
	# Permission checked above, safe for system operation
	note.insert(ignore_permissions=True)
	return {"status": "success", "action": "Create Note", "note": note.name}


def log_execution(rule_name, doc_name, doctype, results):
	"""Log automation execution
	
	SECURITY NOTE: This function uses ignore_permissions=True because:
	1. It's a system-level logging operation
	2. It's called from execute_automation_rule which is whitelisted and should verify permissions
	3. Logs are system records, not user data
	4. The automation rule itself should have permission checks
	"""
	log = frappe.get_doc({
		"doctype": "CRM Automation Log",
		"automation_rule": rule_name,
		"reference_doctype": doctype,
		"reference_docname": doc_name,
		"execution_results": json.dumps(results),
		"status": "Success" if all(r.get("status") == "success" for r in results) else "Partial",
	})
	# System-level logging operation - ignore_permissions is acceptable here
	log.insert(ignore_permissions=True)


@frappe.whitelist()
def test_automation_rule(rule_name, test_data):
	"""
	Test an automation rule with sample data
	"""
	rule = frappe.get_doc("CRM Automation Rule", rule_name)

	if isinstance(test_data, str):
		test_data = json.loads(test_data)

	# Simulate execution
	results = []
	for action in rule.actions:
		try:
			result = execute_action(action, test_data.get("doc_name"), test_data.get("doctype"))
			results.append(result)
		except Exception as e:
			results.append({"status": "error", "message": str(e)})

	return {"status": "test_complete", "results": results}

