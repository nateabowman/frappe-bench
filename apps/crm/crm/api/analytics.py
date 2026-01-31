import frappe
from frappe import _
from frappe.utils import getdate, flt, today, add_days, date_diff
from datetime import datetime, timedelta
import json


@frappe.whitelist()
def get_sales_performance_metrics(from_date=None, to_date=None, user=None):
	"""
	Get comprehensive sales performance metrics
	"""
	if not from_date:
		from_date = getdate(today())
	if not to_date:
		to_date = getdate(today())

	filters = {
		"creation": [">=", from_date],
		"creation": ["<=", to_date],
		"docstatus": ["!=", 2],
	}

	if user:
		filters["deal_owner"] = user

	# Total Revenue
	total_revenue = frappe.db.get_all(
		"CRM Deal",
		filters={**filters, "status": "Won"},
		fields=["SUM(deal_value) as total"],
		as_list=True,
	)[0][0] or 0

	# Total Deals
	total_deals = frappe.db.count("CRM Deal", filters=filters)

	# Won Deals
	won_deals = frappe.db.count("CRM Deal", filters={**filters, "status": "Won"})

	# Lost Deals
	lost_deals = frappe.db.count("CRM Deal", filters={**filters, "status": "Lost"})

	# Conversion Rate
	conversion_rate = (won_deals / total_deals * 100) if total_deals > 0 else 0

	# Average Deal Value
	avg_deal_value = total_revenue / won_deals if won_deals > 0 else 0

	# Average Sales Cycle
	sales_cycle_days = frappe.db.sql(
		"""
		SELECT AVG(DATEDIFF(closed_date, creation))
		FROM `tabCRM Deal`
		WHERE status = 'Won'
		AND closed_date IS NOT NULL
		AND creation >= %(from_date)s
		AND creation <= %(to_date)s
		AND docstatus != 2
		""",
		{"from_date": from_date, "to_date": to_date},
		as_list=True,
	)[0][0] or 0

	return {
		"total_revenue": flt(total_revenue, 2),
		"total_deals": total_deals,
		"won_deals": won_deals,
		"lost_deals": lost_deals,
		"conversion_rate": flt(conversion_rate, 2),
		"avg_deal_value": flt(avg_deal_value, 2),
		"avg_sales_cycle_days": flt(sales_cycle_days, 0),
	}


@frappe.whitelist()
def get_conversion_funnel(from_date=None, to_date=None, user=None):
	"""
	Get conversion funnel data across lead stages
	"""
	if not from_date:
		from_date = getdate(today())
	if not to_date:
		to_date = getdate(today())

	filters = {
		"creation": [">=", from_date],
		"creation": ["<=", to_date],
		"docstatus": ["!=", 2],
	}

	if user:
		filters["lead_owner"] = user

	# Get all lead statuses
	lead_statuses = frappe.get_all("CRM Lead Status", pluck="name", order_by="order_index")

	funnel_data = []
	total_leads = 0

	for status in lead_statuses:
		count = frappe.db.count("CRM Lead", filters={**filters, "status": status})
		total_leads = max(total_leads, count)
		funnel_data.append({
			"label": status,
			"value": count,
			"percentage": 0,  # Will calculate after
		})

	# Calculate percentages
	for item in funnel_data:
		if total_leads > 0:
			item["percentage"] = (item["value"] / total_leads) * 100

	return funnel_data


@frappe.whitelist()
def get_pipeline_health_score(from_date=None, to_date=None, user=None):
	"""
	Calculate pipeline health score based on various factors
	"""
	if not from_date:
		from_date = getdate(today())
	if not to_date:
		to_date = getdate(today())

	filters = {
		"creation": [">=", from_date],
		"creation": ["<=", to_date],
		"docstatus": ["!=", 2],
		"status": ["not in", ["Won", "Lost"]],
	}

	if user:
		filters["deal_owner"] = user

	# Get all active deals
	deals = frappe.get_all(
		"CRM Deal",
		filters=filters,
		fields=["name", "deal_value", "probability", "expected_closure_date", "status"],
	)

	if not deals:
		return {"score": 0, "factors": []}

	total_value = sum(flt(d.deal_value or 0) for d in deals)
	avg_probability = sum(flt(d.probability or 0) for d in deals) / len(deals) if deals else 0

	# Calculate score factors
	factors = []

	# Value factor (0-30 points)
	value_score = min(30, (total_value / 100000) * 30) if total_value > 0 else 0
	factors.append({"name": "Pipeline Value", "score": value_score, "max": 30})

	# Probability factor (0-30 points)
	probability_score = (avg_probability / 100) * 30
	factors.append({"name": "Average Probability", "score": probability_score, "max": 30})

	# Activity factor (0-20 points) - simplified
	activity_score = min(20, len(deals) * 2)
	factors.append({"name": "Deal Count", "score": activity_score, "max": 20})

	# Timeline factor (0-20 points)
	overdue_count = sum(1 for d in deals if d.expected_closure_date and getdate(d.expected_closure_date) < getdate(today()))
	timeline_score = max(0, 20 - (overdue_count / len(deals) * 20)) if deals else 0
	factors.append({"name": "Timeline Health", "score": timeline_score, "max": 20})

	total_score = sum(f["score"] for f in factors)

	return {
		"score": flt(total_score, 2),
		"max_score": 100,
		"factors": factors,
		"total_value": flt(total_value, 2),
		"deal_count": len(deals),
	}


@frappe.whitelist()
def get_activity_analytics(from_date=None, to_date=None, user=None):
	"""
	Get activity analytics (calls, emails, meetings, etc.)
	"""
	if not from_date:
		from_date = getdate(today())
	if not to_date:
		to_date = getdate(today())

	filters = {
		"creation": [">=", from_date],
		"creation": ["<=", to_date],
	}

	if user:
		filters["owner"] = user

	# Call Logs
	call_logs = frappe.db.count("CRM Call Log", filters=filters)

	# Tasks
	tasks = frappe.db.count("CRM Task", filters={**filters, "status": ["!=", "Done"]})

	# Notes
	notes = frappe.db.count("FCRM Note", filters=filters)

	# Communications (simplified)
	communications = frappe.db.count("Communication", filters={**filters, "communication_type": "Communication"})

	return {
		"call_logs": call_logs,
		"tasks": tasks,
		"notes": notes,
		"communications": communications,
		"total": call_logs + tasks + notes + communications,
	}


@frappe.whitelist()
def get_team_performance_comparison(from_date=None, to_date=None, user=None):
	"""
	Compare team member performance
	"""
	if not from_date:
		from_date = getdate(today())
	if not to_date:
		to_date = getdate(today())

	# Get all sales users
	users = frappe.get_all(
		"User",
		filters={"enabled": 1},
		fields=["name", "full_name"],
	)

	# Filter to sales users only
	sales_users = []
	for u in users:
		roles = frappe.get_roles(u.name)
		if "Sales User" in roles or "Sales Manager" in roles:
			sales_users.append(u)

	performance_data = []

	for user_obj in sales_users:
		user_name = user_obj.name

		# Deals created
		deals_created = frappe.db.count(
			"CRM Deal",
			filters={
				"creation": [">=", from_date],
				"creation": ["<=", to_date],
				"deal_owner": user_name,
				"docstatus": ["!=", 2],
			},
		)

		# Deals won
		deals_won = frappe.db.count(
			"CRM Deal",
			filters={
				"creation": [">=", from_date],
				"creation": ["<=", to_date],
				"deal_owner": user_name,
				"status": "Won",
				"docstatus": ["!=", 2],
			},
		)

		# Revenue
		revenue = frappe.db.get_all(
			"CRM Deal",
			filters={
				"creation": [">=", from_date],
				"creation": ["<=", to_date],
				"deal_owner": user_name,
				"status": "Won",
				"docstatus": ["!=", 2],
			},
			fields=["SUM(deal_value) as total"],
			as_list=True,
		)[0][0] or 0

		# Conversion rate
		conversion_rate = (deals_won / deals_created * 100) if deals_created > 0 else 0

		performance_data.append({
			"user": user_name,
			"user_name": user_obj.full_name or user_name,
			"deals_created": deals_created,
			"deals_won": deals_won,
			"revenue": flt(revenue, 2),
			"conversion_rate": flt(conversion_rate, 2),
		})

	# Sort by revenue
	performance_data.sort(key=lambda x: x["revenue"], reverse=True)

	return performance_data


@frappe.whitelist()
def get_revenue_forecast(from_date=None, to_date=None, user=None):
	"""
	Get revenue forecast based on deal probabilities
	"""
	if not from_date:
		from_date = getdate(today())
	if not to_date:
		to_date = getdate(today())

	filters = {
		"status": ["not in", ["Won", "Lost"]],
		"docstatus": ["!=", 2],
	}

	if user:
		filters["deal_owner"] = user

	deals = frappe.get_all(
		"CRM Deal",
		filters=filters,
		fields=["name", "deal_value", "probability", "expected_closure_date"],
	)

	# Calculate weighted revenue
	weighted_revenue = sum(
		flt(d.deal_value or 0) * (flt(d.probability or 0) / 100) for d in deals
	)

	# Group by month
	monthly_forecast = {}
	for deal in deals:
		if deal.expected_closure_date:
			month_key = getdate(deal.expected_closure_date).strftime("%Y-%m")
			if month_key not in monthly_forecast:
				monthly_forecast[month_key] = 0
			monthly_forecast[month_key] += flt(deal.deal_value or 0) * (flt(deal.probability or 0) / 100)

	return {
		"total_weighted_revenue": flt(weighted_revenue, 2),
		"total_deals": len(deals),
		"monthly_breakdown": monthly_forecast,
	}


@frappe.whitelist()
def get_analytics_widgets():
	"""
	Get all analytics widgets
	"""
	widgets = frappe.get_all(
		"CRM Analytics Widget",
		filters={"is_public": 1},
		fields=["*"],
		order_by="modified desc"
	)
	
	# Also get user's private widgets
	user_widgets = frappe.get_all(
		"CRM Analytics Widget",
		filters={"created_by": frappe.session.user, "is_public": 0},
		fields=["*"],
		order_by="modified desc"
	)
	
	return widgets + user_widgets


@frappe.whitelist()
def create_analytics_widget(widget_name, widget_type, widget_title, **kwargs):
	"""
	Create an analytics widget
	"""
	if not widget_name:
		frappe.throw(_("Widget name is required"))
	
	if not widget_type:
		frappe.throw(_("Widget type is required"))
	
	if not widget_title:
		frappe.throw(_("Widget title is required"))
	
	widget = frappe.get_doc({
		"doctype": "CRM Analytics Widget",
		"widget_name": widget_name,
		"widget_type": widget_type,
		"widget_title": widget_title,
		"created_by": frappe.session.user,
		**kwargs
	})
	widget.insert()
	frappe.db.commit()
	
	return widget.as_dict()


@frappe.whitelist()
def get_widget_data(widget_name):
	"""
	Get data for a specific widget
	"""
	widget = frappe.get_doc("CRM Analytics Widget", widget_name)
	
	# Check permissions
	if not widget.is_public and widget.created_by != frappe.session.user:
		frappe.throw(_("You don't have permission to access this widget"), frappe.PermissionError)
	
	# Execute query or get data based on widget configuration
	data = {}
	
	if widget.query:
		# Execute SQL query
		try:
			data = frappe.db.sql(widget.query, as_dict=True)
		except Exception as e:
			frappe.throw(_("Error executing widget query: {0}").format(str(e)))
	elif widget.data_source:
		# Get data from data source
		if widget.data_source == "CRM Deal":
			data = frappe.get_all("CRM Deal", fields=["name", "deal_value", "status", "probability"])
		elif widget.data_source == "CRM Lead":
			data = frappe.get_all("CRM Lead", fields=["name", "status", "source"])
	
	# Update last refreshed time
	widget.last_refreshed = now()
	widget.save()
	frappe.db.commit()
	
	return {
		"widget": widget.as_dict(),
		"data": data
	}


@frappe.whitelist()
def update_analytics_widget(name, **kwargs):
	"""
	Update an analytics widget
	"""
	widget = frappe.get_doc("CRM Analytics Widget", name)
	
	# Check permissions
	if not widget.is_public and widget.created_by != frappe.session.user:
		frappe.throw(_("You don't have permission to update this widget"), frappe.PermissionError)
	
	# Update fields
	for key, value in kwargs.items():
		if hasattr(widget, key):
			setattr(widget, key, value)
	
	widget.save()
	frappe.db.commit()
	
	return widget.as_dict()


@frappe.whitelist()
def update_widget_layout(widget_name, position_x, position_y, width, height):
	"""
	Update widget layout position and size
	"""
	widget = frappe.get_doc("CRM Analytics Widget", widget_name)
	
	# Check permissions
	if not widget.is_public and widget.created_by != frappe.session.user:
		frappe.throw(_("You don't have permission to update this widget"), frappe.PermissionError)
	
	widget.position_x = position_x
	widget.position_y = position_y
	widget.width = width
	widget.height = height
	widget.save()
	frappe.db.commit()
	
	return widget.as_dict()

