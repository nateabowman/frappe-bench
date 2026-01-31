# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _
from datetime import datetime


def validate_date_range(start_date, end_date):
	"""Validate that date range is valid"""
	
	if not start_date or not end_date:
		frappe.throw(_("Start date and end date are required"))
	
	if start_date > end_date:
		frappe.throw(_("Start date cannot be after end date"))
	
	# Check if range is too large (max 2 years)
	days_diff = (end_date - start_date).days
	if days_diff > 730:
		frappe.throw(_("Date range cannot exceed 2 years"))


def validate_employee_access(employee):
	"""Validate that user has access to employee data"""
	
	user = frappe.session.user
	
	# System managers and HR managers have access
	if "System Manager" in frappe.get_roles(user) or "HR Manager" in frappe.get_roles(user):
		return True
	
	# Employees can only access their own data
	employee_doc = frappe.get_cached_doc("Employee", employee)
	if employee_doc.user_id == user:
		return True
	
	frappe.throw(_("You don't have permission to access this employee's data"), frappe.PermissionError)


def validate_department_access(department):
	"""Validate that user has access to department data"""
	
	user = frappe.session.user
	
	# System managers have full access
	if "System Manager" in frappe.get_roles(user):
		return True
	
	# HR managers have access to all departments
	if "HR Manager" in frappe.get_roles(user):
		return True
	
	# Employees can only access their own department
	employee = frappe.db.get_value("Employee", {"user_id": user, "status": "Active"}, "name")
	if employee:
		emp_doc = frappe.get_cached_doc("Employee", employee)
		if emp_doc.department == department:
			return True
	
	frappe.throw(_("You don't have permission to access this department's data"), frappe.PermissionError)


def validate_period(period):
	"""Validate period parameter"""
	
	valid_periods = ["week", "month", "year", "custom"]
	if period not in valid_periods:
		frappe.throw(_("Invalid period. Must be one of: {0}").format(", ".join(valid_periods)))
