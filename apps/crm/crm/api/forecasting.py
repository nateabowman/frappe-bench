import frappe
from frappe import _
from frappe.utils import getdate, flt, today, add_months
from datetime import datetime


@frappe.whitelist()
def create_forecast(period, user=None):
	"""
	Create a revenue forecast for a period
	"""
	# Validate inputs
	if not period:
		frappe.throw(_("Period is required"))
	
	if not user:
		user = frappe.session.user
	
	# Validate user exists
	if not frappe.db.exists("User", user):
		frappe.throw(_("Invalid user"))
	
	# Check if user can create forecasts (must be forecast owner or admin)
	if user != frappe.session.user and frappe.session.user != "Administrator":
		frappe.throw(_("Not permitted to create forecasts for other users"), frappe.PermissionError)

	# Get all active deals
	filters = {
		"status": ["not in", ["Won", "Lost"]],
		"docstatus": ["!=", 2],
	}

	if user != "Administrator":
		filters["deal_owner"] = user

	deals = frappe.get_all(
		"CRM Deal",
		filters=filters,
		fields=["name", "deal_value", "probability", "expected_closure_date", "deal_owner"],
	)

	# Create forecast
	forecast = frappe.get_doc({
		"doctype": "CRM Forecast",
		"period": period,
		"forecast_owner": user,
		"status": "Draft",
	})
	forecast.insert()

	# Create forecast lines
	for deal in deals:
		weighted_value = flt(deal.deal_value or 0) * (flt(deal.probability or 0) / 100)
		
		forecast_line = frappe.get_doc({
			"doctype": "CRM Forecast Line",
			"forecast": forecast.name,
			"deal": deal.name,
			"deal_value": deal.deal_value,
			"probability": deal.probability,
			"weighted_value": weighted_value,
			"expected_closure_date": deal.expected_closure_date,
		})
		forecast_line.insert()

	# Calculate totals
	forecast.reload()
	forecast.total_deals = len(deals)
	forecast.total_weighted_revenue = sum(flt(d.deal_value or 0) * (flt(d.probability or 0) / 100) for d in deals)
	forecast.save()

	return forecast.name


@frappe.whitelist()
def get_forecast_data(forecast_name):
	"""
	Get forecast data with breakdown
	"""
	# Validate input
	if not forecast_name:
		frappe.throw(_("Forecast name is required"))
	
	# Check if forecast exists
	if not frappe.db.exists("CRM Forecast", forecast_name):
		frappe.throw(_("Forecast not found"))
	
	forecast = frappe.get_doc("CRM Forecast", forecast_name)
	
	# Check permissions
	if not frappe.has_permission("CRM Forecast", "read", forecast):
		frappe.throw(_("Not permitted to access this forecast"), frappe.PermissionError)
	
	# Verify user owns the forecast or has appropriate role
	roles = frappe.get_roles()
	if forecast.forecast_owner != frappe.session.user and "Sales Manager" not in roles and frappe.session.user != "Administrator":
		frappe.throw(_("Not permitted to access this forecast"), frappe.PermissionError)
	
	lines = frappe.get_all(
		"CRM Forecast Line",
		filters={"forecast": forecast_name},
		fields=["deal", "deal_value", "probability", "weighted_value", "expected_closure_date"],
	)

	# Group by month
	monthly_breakdown = {}
	for line in lines:
		if line.expected_closure_date:
			month_key = getdate(line.expected_closure_date).strftime("%Y-%m")
			if month_key not in monthly_breakdown:
				monthly_breakdown[month_key] = {"count": 0, "value": 0, "weighted": 0}
			monthly_breakdown[month_key]["count"] += 1
			monthly_breakdown[month_key]["value"] += flt(line.deal_value or 0)
			monthly_breakdown[month_key]["weighted"] += flt(line.weighted_value or 0)

	return {
		"forecast": forecast.as_dict(),
		"lines": lines,
		"monthly_breakdown": monthly_breakdown,
	}


@frappe.whitelist()
def submit_forecast(forecast_name):
	"""
	Submit forecast for approval
	"""
	# Validate input
	if not forecast_name:
		frappe.throw(_("Forecast name is required"))
	
	# Check if forecast exists
	if not frappe.db.exists("CRM Forecast", forecast_name):
		frappe.throw(_("Forecast not found"))
	
	forecast = frappe.get_doc("CRM Forecast", forecast_name)
	
	# Check permissions
	if not frappe.has_permission("CRM Forecast", "write", forecast):
		frappe.throw(_("Not permitted to modify this forecast"), frappe.PermissionError)
	
	# Verify user owns the forecast
	if forecast.forecast_owner != frappe.session.user and frappe.session.user != "Administrator":
		frappe.throw(_("Not permitted to submit this forecast"), frappe.PermissionError)
	
	forecast.status = "Submitted"
	forecast.submitted_by = frappe.session.user
	forecast.submitted_on = today()
	forecast.save()

	return {"status": "submitted"}


@frappe.whitelist()
def approve_forecast(forecast_name):
	"""
	Approve a forecast
	"""
	# Validate input
	if not forecast_name:
		frappe.throw(_("Forecast name is required"))
	
	# Check if forecast exists
	if not frappe.db.exists("CRM Forecast", forecast_name):
		frappe.throw(_("Forecast not found"))
	
	forecast = frappe.get_doc("CRM Forecast", forecast_name)
	
	# Check permissions
	if not frappe.has_permission("CRM Forecast", "write", forecast):
		frappe.throw(_("Not permitted to modify this forecast"), frappe.PermissionError)
	
	# Only managers and administrators can approve forecasts
	roles = frappe.get_roles()
	if "Sales Manager" not in roles and frappe.session.user != "Administrator":
		frappe.throw(_("Only managers can approve forecasts"), frappe.PermissionError)
	
	forecast.status = "Approved"
	forecast.approved_by = frappe.session.user
	forecast.approved_on = today()
	forecast.save()

	return {"status": "approved"}


@frappe.whitelist()
def get_forecast_accuracy(forecast_name):
	"""
	Calculate forecast accuracy by comparing with actual results
	"""
	# Validate input
	if not forecast_name:
		frappe.throw(_("Forecast name is required"))
	
	# Check if forecast exists
	if not frappe.db.exists("CRM Forecast", forecast_name):
		frappe.throw(_("Forecast not found"))
	
	forecast = frappe.get_doc("CRM Forecast", forecast_name)
	
	# Check permissions
	if not frappe.has_permission("CRM Forecast", "read", forecast):
		frappe.throw(_("Not permitted to access this forecast"), frappe.PermissionError)
	
	# Verify user owns the forecast or has appropriate role
	roles = frappe.get_roles()
	if forecast.forecast_owner != frappe.session.user and "Sales Manager" not in roles and frappe.session.user != "Administrator":
		frappe.throw(_("Not permitted to access this forecast"), frappe.PermissionError)
	
	# Get actual results for the period
	lines = frappe.get_all(
		"CRM Forecast Line",
		filters={"forecast": forecast_name},
		fields=["deal", "weighted_value", "expected_closure_date"],
	)

	actual_revenue = 0
	forecasted_revenue = 0

	for line in lines:
		# Check permissions on deal before accessing
		if not frappe.has_permission("CRM Deal", "read", line.deal):
			continue
		
		deal = frappe.get_doc("CRM Deal", line.deal)
		forecasted_revenue += flt(line.weighted_value or 0)
		
		if deal.status == "Won":
			actual_revenue += flt(deal.deal_value or 0)

	accuracy = (actual_revenue / forecasted_revenue * 100) if forecasted_revenue > 0 else 0

	return {
		"forecasted_revenue": flt(forecasted_revenue, 2),
		"actual_revenue": flt(actual_revenue, 2),
		"accuracy": flt(accuracy, 2),
	}

