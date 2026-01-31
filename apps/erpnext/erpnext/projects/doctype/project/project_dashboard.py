import frappe
from frappe import _


def get_data():
	return {
		"heatmap": True,
		"heatmap_message": _("This is based on the Time Sheets created against this project"),
		"fieldname": "project",
		"transactions": [
			{
				"label": _("Project"),
				"items": ["Task", "Timesheet", "Issue", "Project Update"],
			},
			{
				"label": _("Construction Management"),
				"items": ["RFI", "Submittal", "Daily Log"],
			},
			{"label": _("Material"), "items": ["Material Request", "BOM", "Stock Entry"]},
			{"label": _("Sales"), "items": ["Sales Order", "Delivery Note", "Sales Invoice"]},
			{"label": _("Purchase"), "items": ["Purchase Order", "Purchase Receipt", "Purchase Invoice"]},
		],
	}


@frappe.whitelist()
def get_job_costing_dashboard(project):
	"""Get real-time job costing data for dashboard"""
	from erpnext.projects.doctype.project.project import Project
	
	project_doc = frappe.get_doc("Project", project)
	project_doc.update_costing()
	
	return {
		"estimated_cost": project_doc.estimated_costing or 0,
		"total_actual_cost": project_doc.total_actual_cost or 0,
		"total_committed_cost": project_doc.total_committed_cost or 0,
		"committed_purchase_cost": project_doc.committed_purchase_cost or 0,
		"total_costing_amount": project_doc.total_costing_amount or 0,
		"total_purchase_cost": project_doc.total_purchase_cost or 0,
		"total_consumed_material_cost": project_doc.total_consumed_material_cost or 0,
		"total_sales_amount": project_doc.total_sales_amount or 0,
		"total_billed_amount": project_doc.total_billed_amount or 0,
		"gross_margin": project_doc.gross_margin or 0,
		"per_gross_margin": project_doc.per_gross_margin or 0,
		"cost_variance": (project_doc.total_committed_cost or 0) - (project_doc.estimated_costing or 0),
		"cost_variance_percent": (
			((project_doc.total_committed_cost or 0) - (project_doc.estimated_costing or 0)) / (project_doc.estimated_costing or 1) * 100
			if project_doc.estimated_costing else 0
		),
	}
