# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _
from datetime import datetime, timedelta
from collections import defaultdict


def predict_leave_patterns(employee, period_months=12):
	"""Analyze historical leave patterns to predict future leave requests"""
	
	# Get historical leave data
	leave_applications = frappe.get_all(
		"Leave Application",
		filters={
			"employee": employee,
			"docstatus": 1,
			"from_date": [">=", datetime.now() - timedelta(days=period_months * 30)],
		},
		fields=["leave_type", "from_date", "to_date", "total_leave_days"],
		order_by="from_date"
	)
	
	if not leave_applications:
		return {
			"predicted_leave_days": 0,
			"recommended_leave_types": [],
			"pattern_analysis": {}
		}
	
	# Analyze patterns by month
	monthly_pattern = defaultdict(float)
	leave_type_pattern = defaultdict(float)
	
	for app in leave_applications:
		month_key = str(app.from_date)[:7]  # YYYY-MM
		monthly_pattern[month_key] += app.total_leave_days or 0
		leave_type_pattern[app.leave_type] += app.total_leave_days or 0
	
	# Calculate average monthly leave
	avg_monthly_leave = sum(monthly_pattern.values()) / len(monthly_pattern) if monthly_pattern else 0
	
	# Predict next month
	next_month = (datetime.now() + timedelta(days=30)).strftime("%Y-%m")
	predicted_days = avg_monthly_leave
	
	# Get most common leave types
	recommended_leave_types = sorted(
		leave_type_pattern.items(),
		key=lambda x: x[1],
		reverse=True
	)[:3]
	
	return {
		"predicted_leave_days": round(predicted_days, 1),
		"recommended_leave_types": [lt[0] for lt in recommended_leave_types],
		"pattern_analysis": {
			"average_monthly": round(avg_monthly_leave, 1),
			"total_historical_days": sum(leave_type_pattern.values()),
			"most_used_leave_type": recommended_leave_types[0][0] if recommended_leave_types else None
		}
	}


def suggest_workload_balancing(employee, date_range_start, date_range_end):
	"""Suggest workload balancing based on team leave patterns"""
	
	# Get employee's department
	employee_doc = frappe.get_cached_doc("Employee", employee)
	department = employee_doc.department
	
	if not department:
		return {"suggestions": []}
	
	# Get all employees in department
	team_members = frappe.get_all(
		"Employee",
		filters={"department": department, "status": "Active"},
		fields=["name", "employee_name"]
	)
	
	# Get leave applications for team in date range
	team_leaves = frappe.get_all(
		"Leave Application",
		filters={
			"employee": ["in", [m.name for m in team_members]],
			"docstatus": 1,
			"from_date": [">=", date_range_start],
			"to_date": ["<=", date_range_end],
		},
		fields=["employee", "from_date", "to_date", "total_leave_days"]
	)
	
	# Calculate workload per employee
	workload = defaultdict(int)
	for leave in team_leaves:
		workload[leave.employee] += leave.total_leave_days or 0
	
	# Find employees with high workload
	suggestions = []
	for emp_name, emp_data in [(m.name, m) for m in team_members]:
		current_workload = workload.get(emp_name, 0)
		if current_workload > 10:  # Threshold
			suggestions.append({
				"employee": emp_name,
				"employee_name": emp_data.employee_name,
				"current_workload": current_workload,
				"suggestion": _("Consider redistributing some tasks")
			})
	
	return {"suggestions": suggestions}


@frappe.whitelist()
def get_leave_predictions(employee):
	"""API endpoint for leave predictions"""
	try:
		return predict_leave_patterns(employee)
	except Exception as e:
		frappe.log_error(f"Error in get_leave_predictions: {str(e)}")
		frappe.throw(_("Error generating leave predictions"))


@frappe.whitelist()
def get_workload_suggestions(employee, start_date, end_date):
	"""API endpoint for workload balancing suggestions"""
	try:
		return suggest_workload_balancing(employee, start_date, end_date)
	except Exception as e:
		frappe.log_error(f"Error in get_workload_suggestions: {str(e)}")
		frappe.throw(_("Error generating workload suggestions"))
