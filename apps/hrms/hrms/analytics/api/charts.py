# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _
from hrms.analytics.utils.data_aggregator import (
	aggregate_attendance_data,
	aggregate_leave_data,
	aggregate_payroll_data,
	aggregate_performance_data,
	aggregate_workforce_demographics,
	aggregate_cost_analysis,
	aggregate_engagement_metrics,
	get_date_range
)
from hrms.analytics.utils.permissions import check_analytics_permission, filter_data_by_permissions
from hrms.analytics.utils.validators import validate_date_range, validate_employee_access, validate_department_access, validate_period


@frappe.whitelist()
def get_attendance_heatmap_data(employee=None, department=None, period="month"):
	"""Get attendance heatmap data for calendar visualization"""
	try:
		# Validate inputs
		validate_period(period)
		if employee:
			validate_employee_access(employee)
		if department:
			validate_department_access(department)
		
		# Check permissions
		if not check_analytics_permission(employee, department):
			frappe.throw(_("You don't have permission to view this data"), frappe.PermissionError)
		
		start_date, end_date = get_date_range(period)
		validate_date_range(start_date, end_date)
		
		data = aggregate_attendance_data(
			employee=employee,
			department=department,
			start_date=start_date,
			end_date=end_date
		)
		
		# Filter by permissions
		data = filter_data_by_permissions(data, employee, department)
		
		# Format for heatmap (array of {date, value, status})
		heatmap_data = []
		for date_str, values in data["by_date"].items():
			heatmap_data.append({
				"date": date_str,
				"present": values["present"],
				"absent": values["absent"],
				"on_leave": values["on_leave"],
				"total": sum(values.values())
			})
		
		return {
			"heatmap_data": sorted(heatmap_data, key=lambda x: x["date"]),
			"summary": data["summary"]
		}
	except Exception as e:
		frappe.log_error(f"Error in get_attendance_heatmap_data: {str(e)}")
		frappe.throw(_("Error fetching attendance heatmap data"))


@frappe.whitelist()
def get_payroll_trends(employee=None, department=None, period="year"):
	"""Get payroll trends data"""
	try:
		start_date, end_date = get_date_range(period)
		
		data = aggregate_payroll_data(
			employee=employee,
			department=department,
			start_date=start_date,
			end_date=end_date
		)
		
		# Format for line/area chart
		trend_data = []
		for month, values in sorted(data["by_month"].items()):
			trend_data.append({
				"month": month,
				"gross_pay": values["gross_pay"],
				"net_pay": values["net_pay"],
				"count": values["count"]
			})
		
		return {
			"trend_data": trend_data,
			"total_gross": data["total_gross"],
			"total_net": data["total_net"],
			"total_slips": data["total_slips"]
		}
	except Exception as e:
		frappe.log_error(f"Error in get_payroll_trends: {str(e)}")
		frappe.throw(_("Error fetching payroll trends"))


@frappe.whitelist()
def get_leave_utilization(employee=None, department=None, period="year"):
	"""Get leave utilization data"""
	try:
		start_date, end_date = get_date_range(period)
		
		data = aggregate_leave_data(
			employee=employee,
			department=department,
			start_date=start_date,
			end_date=end_date
		)
		
		# Format for donut/pie chart
		chart_data = []
		for leave_type, days in data["by_type"].items():
			chart_data.append({
				"label": leave_type,
				"value": days,
				"percentage": (days / data["total_days"] * 100) if data["total_days"] > 0 else 0
			})
		
		return {
			"chart_data": chart_data,
			"total_days": data["total_days"],
			"applications": data["applications"]
		}
	except Exception as e:
		frappe.log_error(f"Error in get_leave_utilization: {str(e)}")
		frappe.throw(_("Error fetching leave utilization data"))


@frappe.whitelist()
def get_performance_metrics(employee=None, department=None):
	"""Get performance metrics data"""
	try:
		data = aggregate_performance_data(
			employee=employee,
			department=department
		)
		
		# Format for radar chart or bar chart
		employee_scores = []
		for emp, score in list(data["by_employee"].items())[:10]:  # Top 10
			emp_doc = frappe.get_cached_doc("Employee", emp)
			employee_scores.append({
				"employee": emp,
				"employee_name": emp_doc.employee_name,
				"score": round(score, 2)
			})
		
		return {
			"average_score": round(data["average_score"], 2),
			"total_appraisals": data["total_appraisals"],
			"employee_scores": sorted(employee_scores, key=lambda x: x["score"], reverse=True)
		}
	except Exception as e:
		frappe.log_error(f"Error in get_performance_metrics: {str(e)}")
		frappe.throw(_("Error fetching performance metrics"))


@frappe.whitelist()
def get_workforce_demographics(department=None):
	"""Get workforce demographics data"""
	try:
		data = aggregate_workforce_demographics(department=department)
		
		# Format for various chart types
		age_data = [{"label": k, "value": v} for k, v in data["age_distribution"].items()]
		gender_data = [{"label": k, "value": v} for k, v in data["gender_distribution"].items()]
		dept_data = [{"label": k, "value": v} for k, v in data["department_distribution"].items()]
		tenure_data = [{"label": k, "value": v} for k, v in data["tenure_distribution"].items()]
		
		return {
			"total_employees": data["total_employees"],
			"age_distribution": age_data,
			"gender_distribution": gender_data,
			"department_distribution": dept_data,
			"tenure_distribution": tenure_data
		}
	except Exception as e:
		frappe.log_error(f"Error in get_workforce_demographics: {str(e)}")
		frappe.throw(_("Error fetching workforce demographics"))


@frappe.whitelist()
def get_cost_analysis(department=None, period="year"):
	"""Get cost analysis data"""
	try:
		start_date, end_date = get_date_range(period)
		
		data = aggregate_cost_analysis(
			department=department,
			start_date=start_date,
			end_date=end_date
		)
		
		# Format for bar/stacked chart
		dept_data = []
		for dept, costs in data["by_department"].items():
			dept_data.append({
				"department": dept,
				"gross_pay": costs["gross"],
				"deductions": costs["deductions"],
				"net_pay": costs["net"]
			})
		
		return {
			"total_gross": data["total_gross"],
			"total_deductions": data["total_deductions"],
			"total_net": data["total_net"],
			"by_department": sorted(dept_data, key=lambda x: x["gross_pay"], reverse=True),
			"total_slips": data["total_slips"]
		}
	except Exception as e:
		frappe.log_error(f"Error in get_cost_analysis: {str(e)}")
		frappe.throw(_("Error fetching cost analysis data"))


@frappe.whitelist()
def get_engagement_metrics(department=None):
	"""Get employee engagement metrics"""
	try:
		data = aggregate_engagement_metrics(department=department)
		return data
	except Exception as e:
		frappe.log_error(f"Error in get_engagement_metrics: {str(e)}")
		frappe.throw(_("Error fetching engagement metrics"))


@frappe.whitelist()
def get_attendance_trends(employee=None, department=None, period="month"):
	"""Get attendance trends for time series chart"""
	try:
		start_date, end_date = get_date_range(period)
		
		data = aggregate_attendance_data(
			employee=employee,
			department=department,
			start_date=start_date,
			end_date=end_date
		)
		
		# Format for time series line chart
		trend_data = []
		for date_str, values in sorted(data["by_date"].items()):
			total = sum(values.values())
			attendance_rate = (values["present"] / total * 100) if total > 0 else 0
			
			trend_data.append({
				"date": date_str,
				"present": values["present"],
				"absent": values["absent"],
				"on_leave": values["on_leave"],
				"attendance_rate": round(attendance_rate, 2)
			})
		
		return {
			"trend_data": trend_data,
			"summary": data["summary"]
		}
	except Exception as e:
		frappe.log_error(f"Error in get_attendance_trends: {str(e)}")
		frappe.throw(_("Error fetching attendance trends"))
