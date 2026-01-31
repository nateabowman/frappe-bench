import frappe
from frappe import _
from frappe.utils import now, getdate, flt
import json


@frappe.whitelist()
def create_campaign(name, campaign_type, start_date, end_date=None):
	"""
	Create a marketing campaign
	"""
	# Validate inputs
	if not name:
		frappe.throw(_("Campaign name is required"))
	
	if not campaign_type:
		frappe.throw(_("Campaign type is required"))
	
	if not start_date:
		frappe.throw(_("Start date is required"))
	
	# Validate campaign type
	allowed_types = ["Email", "Social Media", "Website", "Event", "Other"]
	if campaign_type not in allowed_types:
		frappe.throw(_("Invalid campaign type"))
	
	# Validate dates
	try:
		start_date_obj = getdate(start_date)
		if end_date:
			end_date_obj = getdate(end_date)
			if end_date_obj < start_date_obj:
				frappe.throw(_("End date must be after start date"))
	except Exception:
		frappe.throw(_("Invalid date format"))
	
	campaign = frappe.get_doc({
		"doctype": "CRM Campaign",
		"title": name,
		"campaign_type": campaign_type,
		"start_date": start_date,
		"end_date": end_date,
		"status": "Planning",
		"owner": frappe.session.user,
	})
	campaign.insert()

	return campaign.name


@frappe.whitelist()
def get_campaign_performance(campaign_name):
	"""
	Get campaign performance metrics
	"""
	# Validate input
	if not campaign_name:
		frappe.throw(_("Campaign name is required"))
	
	# Check if campaign exists
	if not frappe.db.exists("CRM Campaign", campaign_name):
		frappe.throw(_("Campaign not found"))
	
	campaign = frappe.get_doc("CRM Campaign", campaign_name)
	
	# Check permissions
	if not frappe.has_permission("CRM Campaign", "read", campaign):
		frappe.throw(_("Not permitted to access this campaign"), frappe.PermissionError)

	# Get leads generated from campaign
	leads = frappe.get_all(
		"CRM Lead",
		filters={"source": campaign_name},
		fields=["name", "status"],
	)

	total_leads = len(leads)
	converted_leads = len([l for l in leads if l.status == "Converted"])
	conversion_rate = (converted_leads / total_leads * 100) if total_leads > 0 else 0

	# Get deals from campaign
	deals = frappe.get_all(
		"CRM Deal",
		filters={"source": campaign_name},
		fields=["name", "deal_value", "status"],
	)

	total_deals = len(deals)
	won_deals = len([d for d in deals if d.status == "Won"])
	total_revenue = sum(flt(d.deal_value or 0) for d in deals if d.status == "Won")

	return {
		"total_leads": total_leads,
		"converted_leads": converted_leads,
		"conversion_rate": flt(conversion_rate, 2),
		"total_deals": total_deals,
		"won_deals": won_deals,
		"total_revenue": flt(total_revenue, 2),
	}


@frappe.whitelist()
def create_lead_form(name, fields, redirect_url=None):
	"""
	Create a lead generation form
	"""
	# Validate inputs
	if not name:
		frappe.throw(_("Form name is required"))
	
	if not fields:
		frappe.throw(_("Form fields are required"))
	
	# Validate fields is a valid JSON structure
	if isinstance(fields, str):
		try:
			import json
			fields = json.loads(fields)
		except json.JSONDecodeError:
			frappe.throw(_("Invalid fields format"))
	
	# Validate redirect_url if provided
	if redirect_url and not (redirect_url.startswith("http://") or redirect_url.startswith("https://")):
		frappe.throw(_("Invalid redirect URL"))
	
	form = frappe.get_doc({
		"doctype": "CRM Lead Form",
		"title": name,
		"fields": fields if isinstance(fields, str) else json.dumps(fields),
		"redirect_url": redirect_url,
		"enabled": True,
		"owner": frappe.session.user,
	})
	form.insert()

	return form.name


@frappe.whitelist()
def submit_lead_form(form_name, form_data):
	"""
	Submit data from a lead form
	"""
	# Validate inputs
	if not form_name:
		frappe.throw(_("Form name is required"))
	
	if not form_data:
		frappe.throw(_("Form data is required"))
	
	# Parse form_data if it's a string
	if isinstance(form_data, str):
		try:
			import json
			form_data = json.loads(form_data)
		except json.JSONDecodeError:
			frappe.throw(_("Invalid form data format"))
	
	# Check if form exists
	if not frappe.db.exists("CRM Lead Form", form_name):
		frappe.throw(_("Form not found"))
	
	form = frappe.get_doc("CRM Lead Form", form_name)

	if not form.enabled:
		frappe.throw(_("Form is not enabled"))

	# Validate and sanitize form data
	email = form_data.get("email") or ""
	if email and "@" not in email:
		frappe.throw(_("Invalid email address"))
	
	# Sanitize inputs to prevent XSS
	import html
	lead_name = html.escape(str(form_data.get("name") or form_data.get("email") or ""))
	email = html.escape(email)
	mobile_no = html.escape(str(form_data.get("phone") or form_data.get("mobile") or ""))

	# Create lead from form data
	lead = frappe.get_doc({
		"doctype": "CRM Lead",
		"lead_name": lead_name,
		"email": email,
		"mobile_no": mobile_no,
		"source": form_name,
	})
	lead.insert()

	return lead.name

