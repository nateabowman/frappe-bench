# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _


@frappe.whitelist()
def get_dashboard_summary(employee=None, department=None):
	"""Get comprehensive dashboard summary"""
	try:
		from hrms.analytics.api.charts import (
			get_attendance_heatmap_data,
			get_payroll_trends,
			get_leave_utilization,
			get_performance_metrics,
		)
		
		summary = {
			"attendance": get_attendance_heatmap_data(employee, department, "month"),
			"payroll": get_payroll_trends(employee, department, "year"),
			"leaves": get_leave_utilization(employee, department, "year"),
			"performance": get_performance_metrics(employee, department),
		}
		
		return summary
	except Exception as e:
		frappe.log_error(f"Error in get_dashboard_summary: {str(e)}")
		frappe.throw(_("Error fetching dashboard summary"))


@frappe.whitelist()
def get_hr_dashboard_summary(department=None):
	"""Get HR manager dashboard summary"""
	try:
		from hrms.analytics.api.charts import (
			get_workforce_demographics,
			get_cost_analysis,
			get_engagement_metrics,
		)
		
		summary = {
			"demographics": get_workforce_demographics(department),
			"cost_analysis": get_cost_analysis(department, "year"),
			"engagement": get_engagement_metrics(department),
		}
		
		return summary
	except Exception as e:
		frappe.log_error(f"Error in get_hr_dashboard_summary: {str(e)}")
		frappe.throw(_("Error fetching HR dashboard summary"))
