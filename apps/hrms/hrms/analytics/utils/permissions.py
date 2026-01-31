# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _


def check_analytics_permission(employee=None, department=None):
	"""Check if user has permission to view analytics data"""
	
	user = frappe.session.user
	
	# System administrators can view all
	if "System Manager" in frappe.get_roles(user):
		return True
	
	# HR Managers can view department and company-wide data
	if "HR Manager" in frappe.get_roles(user):
		return True
	
	# Employees can only view their own data
	if employee:
		employee_doc = frappe.get_cached_doc("Employee", employee)
		if employee_doc.user_id == user:
			return True
	
	return False


def filter_data_by_permissions(data, employee=None, department=None):
	"""Filter analytics data based on user permissions"""
	
	if not check_analytics_permission(employee, department):
		frappe.throw(_("You don't have permission to view this analytics data"), frappe.PermissionError)
	
	user = frappe.session.user
	
	# If user is not HR Manager, restrict to their own data
	if "HR Manager" not in frappe.get_roles(user) and "System Manager" not in frappe.get_roles(user):
		if employee:
			employee_doc = frappe.get_cached_doc("Employee", employee)
			if employee_doc.user_id != user:
				frappe.throw(_("You can only view your own analytics data"), frappe.PermissionError)
	
	return data
