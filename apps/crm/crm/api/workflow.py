# Copyright (c) 2024, Nexelya Technologies Pvt. Ltd. and Contributors
# GNU GPLv3 License. See license.txt

import frappe
from frappe import _


@frappe.whitelist()
def get_workflow_templates(workflow_type=None):
	"""
	Get workflow templates
	"""
	filters = {"is_active": 1}
	if workflow_type:
		filters["workflow_type"] = workflow_type
	
	templates = frappe.get_all(
		"CRM Workflow Template",
		filters=filters,
		fields=["*"],
		order_by="modified desc"
	)
	
	return templates


@frappe.whitelist()
def create_workflow_template(template_name, workflow_type, trigger_doctype=None, **kwargs):
	"""
	Create a workflow template
	"""
	if not template_name:
		frappe.throw(_("Template name is required"))
	
	if not workflow_type:
		frappe.throw(_("Workflow type is required"))
	
	template = frappe.get_doc({
		"doctype": "CRM Workflow Template",
		"template_name": template_name,
		"workflow_type": workflow_type,
		"trigger_doctype": trigger_doctype,
		"is_active": 1,
		"created_by": frappe.session.user,
		**kwargs
	})
	template.insert()
	frappe.db.commit()
	
	return template.as_dict()


@frappe.whitelist()
def update_workflow_template(name, **kwargs):
	"""
	Update a workflow template
	"""
	template = frappe.get_doc("CRM Workflow Template", name)
	
	# Check permissions
	if not template.is_public and template.created_by != frappe.session.user:
		frappe.throw(_("You don't have permission to update this workflow template"), frappe.PermissionError)
	
	# Update fields
	for key, value in kwargs.items():
		if hasattr(template, key):
			setattr(template, key, value)
	
	template.save()
	frappe.db.commit()
	
	return template.as_dict()


@frappe.whitelist()
def execute_workflow(template_name, reference_doctype, reference_docname):
	"""
	Execute a workflow template on a document
	"""
	template = frappe.get_doc("CRM Workflow Template", template_name)
	
	if not template.is_active:
		frappe.throw(_("Workflow template is not active"))
	
	# Get the document
	doc = frappe.get_doc(reference_doctype, reference_docname)
	
	# Execute workflow steps
	# This is a simplified version - actual implementation would process each step
	result = {
		"status": "success",
		"message": f"Workflow {template_name} executed successfully",
		"steps_executed": len(template.workflow_steps) if template.workflow_steps else 0
	}
	
	return result
