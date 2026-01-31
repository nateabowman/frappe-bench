# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _
from datetime import datetime, timedelta
from collections import defaultdict
import json


def get_date_range(period="month"):
	"""Get date range based on period type"""
	today = datetime.now().date()
	
	if period == "week":
		start_date = today - timedelta(days=today.weekday())
		end_date = start_date + timedelta(days=6)
	elif period == "month":
		start_date = today.replace(day=1)
		if today.month == 12:
			end_date = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
		else:
			end_date = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
	elif period == "year":
		start_date = today.replace(month=1, day=1)
		end_date = today.replace(month=12, day=31)
	else:
		start_date = today - timedelta(days=30)
		end_date = today
	
	return start_date, end_date


def aggregate_attendance_data(employee=None, department=None, start_date=None, end_date=None):
	"""Aggregate attendance data for visualization"""
	filters = {}
	
	if employee:
		filters["employee"] = employee
	if department:
		filters["department"] = department
	if start_date:
		filters["attendance_date"] = [">=", start_date]
	if end_date:
		if "attendance_date" in filters:
			filters["attendance_date"] = ["between", [start_date, end_date]]
		else:
			filters["attendance_date"] = ["<=", end_date]
	
	attendance_records = frappe.get_all(
		"Attendance",
		filters=filters,
		fields=["attendance_date", "status", "employee", "department"],
		order_by="attendance_date"
	)
	
	# Group by date
	by_date = defaultdict(lambda: {"present": 0, "absent": 0, "on_leave": 0})
	
	for record in attendance_records:
		date_key = str(record.attendance_date)
		if record.status == "Present":
			by_date[date_key]["present"] += 1
		elif record.status == "Absent":
			by_date[date_key]["absent"] += 1
		elif record.status == "On Leave":
			by_date[date_key]["on_leave"] += 1
	
	return {
		"by_date": dict(by_date),
		"total_records": len(attendance_records),
		"summary": {
			"present": sum(d["present"] for d in by_date.values()),
			"absent": sum(d["absent"] for d in by_date.values()),
			"on_leave": sum(d["on_leave"] for d in by_date.values()),
		}
	}


def aggregate_leave_data(employee=None, department=None, start_date=None, end_date=None):
	"""Aggregate leave utilization data"""
	filters = {"docstatus": 1}
	
	if employee:
		filters["employee"] = employee
	if department:
		filters["department"] = department
	if start_date:
		filters["from_date"] = [">=", start_date]
	if end_date:
		if "from_date" in filters:
			filters["from_date"] = ["between", [start_date, end_date]]
		else:
			filters["to_date"] = ["<=", end_date]
	
	leave_applications = frappe.get_all(
		"Leave Application",
		filters=filters,
		fields=["leave_type", "total_leave_days", "from_date", "to_date", "employee"]
	)
	
	# Group by leave type
	by_type = defaultdict(float)
	
	for app in leave_applications:
		by_type[app.leave_type] += app.total_leave_days or 0
	
	# Get leave type names
	leave_type_names = {}
	for leave_type in by_type.keys():
		leave_type_doc = frappe.get_cached_doc("Leave Type", leave_type)
		leave_type_names[leave_type] = leave_type_doc.leave_type_name
	
	return {
		"by_type": {leave_type_names.get(k, k): v for k, v in by_type.items()},
		"total_days": sum(by_type.values()),
		"applications": len(leave_applications)
	}


def aggregate_payroll_data(employee=None, department=None, start_date=None, end_date=None):
	"""Aggregate payroll trends data"""
	filters = {"docstatus": 1}
	
	if employee:
		filters["employee"] = employee
	if department:
		filters["department"] = department
	if start_date:
		filters["start_date"] = [">=", start_date]
	if end_date:
		if "start_date" in filters:
			filters["start_date"] = ["between", [start_date, end_date]]
		else:
			filters["end_date"] = ["<=", end_date]
	
	salary_slips = frappe.get_all(
		"Salary Slip",
		filters=filters,
		fields=["name", "start_date", "end_date", "gross_pay", "net_pay", "employee", "department"],
		order_by="start_date"
	)
	
	# Group by month
	by_month = defaultdict(lambda: {"gross_pay": 0, "net_pay": 0, "count": 0})
	
	for slip in salary_slips:
		if slip.start_date:
			month_key = str(slip.start_date)[:7]  # YYYY-MM
			by_month[month_key]["gross_pay"] += slip.gross_pay or 0
			by_month[month_key]["net_pay"] += slip.net_pay or 0
			by_month[month_key]["count"] += 1
	
	return {
		"by_month": dict(by_month),
		"total_slips": len(salary_slips),
		"total_gross": sum(s["gross_pay"] for s in by_month.values()),
		"total_net": sum(s["net_pay"] for s in by_month.values())
	}


def aggregate_performance_data(employee=None, department=None):
	"""Aggregate performance metrics"""
	filters = {"docstatus": 1}
	
	if employee:
		filters["employee"] = employee
	if department:
		filters["department"] = department
	
	appraisals = frappe.get_all(
		"Appraisal",
		filters=filters,
		fields=["name", "employee", "appraisal_cycle", "final_score", "department"],
		order_by="creation desc"
	)
	
	if not appraisals:
		return {"average_score": 0, "total_appraisals": 0, "by_employee": {}}
	
	scores = [a.final_score for a in appraisals if a.final_score]
	
	# Group by employee
	by_employee = defaultdict(list)
	for app in appraisals:
		if app.final_score:
			by_employee[app.employee].append(app.final_score)
	
	# Calculate averages
	by_employee_avg = {
		emp: sum(scores) / len(scores) 
		for emp, scores in by_employee.items()
	}
	
	return {
		"average_score": sum(scores) / len(scores) if scores else 0,
		"total_appraisals": len(appraisals),
		"by_employee": by_employee_avg
	}


def aggregate_workforce_demographics(department=None):
	"""Aggregate workforce demographics"""
	filters = {"status": "Active"}
	
	if department:
		filters["department"] = department
	
	employees = frappe.get_all(
		"Employee",
		filters=filters,
		fields=["name", "gender", "date_of_birth", "date_of_joining", "department", "designation"]
	)
	
	# Age distribution
	age_groups = {"18-25": 0, "26-35": 0, "36-45": 0, "46-55": 0, "56+": 0}
	
	# Gender distribution
	gender_dist = defaultdict(int)
	
	# Department distribution
	dept_dist = defaultdict(int)
	
	# Tenure groups
	tenure_groups = {"0-1": 0, "1-3": 0, "3-5": 0, "5-10": 0, "10+": 0}
	
	today = datetime.now().date()
	
	for emp in employees:
		# Gender
		if emp.gender:
			gender_dist[emp.gender] += 1
		
		# Age
		if emp.date_of_birth:
			age = (today - emp.date_of_birth).days // 365
			if age < 26:
				age_groups["18-25"] += 1
			elif age < 36:
				age_groups["26-35"] += 1
			elif age < 46:
				age_groups["36-45"] += 1
			elif age < 56:
				age_groups["46-55"] += 1
			else:
				age_groups["56+"] += 1
		
		# Department
		if emp.department:
			dept_dist[emp.department] += 1
		
		# Tenure
		if emp.date_of_joining:
			tenure_years = (today - emp.date_of_joining).days / 365
			if tenure_years < 1:
				tenure_groups["0-1"] += 1
			elif tenure_years < 3:
				tenure_groups["1-3"] += 1
			elif tenure_years < 5:
				tenure_groups["3-5"] += 1
			elif tenure_years < 10:
				tenure_groups["5-10"] += 1
			else:
				tenure_groups["10+"] += 1
	
	return {
		"total_employees": len(employees),
		"age_distribution": age_groups,
		"gender_distribution": dict(gender_dist),
		"department_distribution": dict(dept_dist),
		"tenure_distribution": tenure_groups
	}


def aggregate_cost_analysis(department=None, start_date=None, end_date=None):
	"""Aggregate cost analysis data"""
	filters = {"docstatus": 1}
	
	if department:
		filters["department"] = department
	if start_date:
		filters["start_date"] = [">=", start_date]
	if end_date:
		if "start_date" in filters:
			filters["start_date"] = ["between", [start_date, end_date]]
		else:
			filters["end_date"] = ["<=", end_date]
	
	salary_slips = frappe.get_all(
		"Salary Slip",
		filters=filters,
		fields=["gross_pay", "total_deduction", "net_pay", "start_date", "department"]
	)
	
	total_gross = sum(slip.gross_pay or 0 for slip in salary_slips)
	total_deductions = sum(slip.total_deduction or 0 for slip in salary_slips)
	total_net = sum(slip.net_pay or 0 for slip in salary_slips)
	
	# Group by department
	dept_costs = defaultdict(lambda: {"gross": 0, "deductions": 0, "net": 0})
	
	for slip in salary_slips:
		if slip.department:
			dept_costs[slip.department]["gross"] += slip.gross_pay or 0
			dept_costs[slip.department]["deductions"] += slip.total_deduction or 0
			dept_costs[slip.department]["net"] += slip.net_pay or 0
	
	return {
		"total_gross": total_gross,
		"total_deductions": total_deductions,
		"total_net": total_net,
		"by_department": dict(dept_costs),
		"total_slips": len(salary_slips)
	}


def aggregate_engagement_metrics(department=None):
	"""Aggregate employee engagement metrics"""
	# This would integrate with employee pulse surveys when implemented
	# For now, return placeholder structure
	return {
		"overall_score": 0,
		"by_department": {},
		"trend": []
	}
