import frappe
from frappe import _
import json


@frappe.whitelist()
def get_reports():
	"""
	Get all saved reports for the current user
	"""
	reports = frappe.get_all(
		"CRM Analytics Report",
		filters={"owner": frappe.session.user},
		fields=["name", "title", "doctype", "config"],
		order_by="modified desc",
	)

	# Parse config for each report
	for report in reports:
		if report.config:
			try:
				report.config = json.loads(report.config) if isinstance(report.config, str) else report.config
			except:
				report.config = {}

	return reports


@frappe.whitelist()
def save_report(report):
	"""
	Save a report configuration
	"""
	if isinstance(report, str):
		report = json.loads(report)

	if not report.get("title"):
		frappe.throw(_("Report title is required"))

	# Create or update report
	if report.get("name") and frappe.db.exists("CRM Analytics Report", report.name):
		doc = frappe.get_doc("CRM Analytics Report", report.name)
		# Check permissions - user must own the report or be admin
		if doc.owner != frappe.session.user and frappe.session.user != "Administrator":
			frappe.throw(_("Not permitted to modify this report"), frappe.PermissionError)
	else:
		doc = frappe.get_doc({"doctype": "CRM Analytics Report"})
		doc.owner = frappe.session.user  # Set owner for new reports

	doc.title = report.get("title")
	doc.doctype = report.get("doctype")
	doc.config = json.dumps(report.get("config", {}))

	doc.save()  # Remove ignore_permissions - permission checked above

	return doc.name


@frappe.whitelist()
def get_fields(doctype):
	"""
	Get all fields for a doctype
	"""
	meta = frappe.get_meta(doctype)
	fields = []
	
	for field in meta.fields:
		if field.fieldtype not in ['Section Break', 'Column Break', 'Tab Break', 'HTML', 'Button']:
			fields.append({
				"label": field.label or field.fieldname,
				"value": field.fieldname,
			})
	
	return fields


@frappe.whitelist()
def get_report_data(report_name):
	"""
	Get data for a saved report
	"""
	report = frappe.get_doc("CRM Analytics Report", report_name)

	if not report:
		frappe.throw(_("Report not found"))

	config = json.loads(report.config) if isinstance(report.config, str) else report.config

	# Build filters
	filters = {}
	for filter_item in config.get("filters", []):
		if filter_item.get("field") and filter_item.get("operator") and filter_item.get("value") is not None:
			filters[filter_item["field"]] = [filter_item["operator"], filter_item["value"]]

	# Get data
	data = frappe.get_all(
		report.doctype,
		filters=filters,
		fields=config.get("columns", []),
		limit=config.get("limit", 1000),
		order_by=config.get("order_by"),
	)

	return {
		"data": data,
		"config": config,
		"title": report.title,
	}

