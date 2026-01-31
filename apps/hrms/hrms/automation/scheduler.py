# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _


def auto_escalate_pending_approvals():
	"""Scheduled job to auto-escalate pending approvals"""
	
	from hrms.automation.approval_engine import auto_escalate_approvals
	
	doctypes = ["Leave Application", "Expense Claim", "Shift Request", "Attendance Request"]
	
	total_escalated = 0
	for doctype in doctypes:
		result = auto_escalate_approvals(doctype, days_threshold=3)
		total_escalated += result.get("count", 0)
	
	if total_escalated > 0:
		frappe.logger().info(f"Auto-escalated {total_escalated} pending approvals")
	
	return total_escalated


def send_engagement_reminders():
	"""Scheduled job to send engagement survey reminders"""
	
	# Get employees who haven't submitted pulse survey this month
	from datetime import datetime
	from frappe.utils import get_first_day, get_last_day
	
	first_day = get_first_day(datetime.now())
	last_day = get_last_day(datetime.now())
	
	employees_with_survey = frappe.get_all(
		"Employee Pulse",
		filters={
			"survey_date": ["between", [first_day, last_day]],
			"docstatus": 1
		},
		pluck="employee"
	)
	
	all_employees = frappe.get_all(
		"Employee",
		filters={"status": "Active"},
		pluck="name"
	)
	
	employees_without_survey = [e for e in all_employees if e not in employees_with_survey]
	
	# Send reminders (placeholder - would integrate with notification system)
	if employees_without_survey:
		frappe.logger().info(f"Sending engagement reminders to {len(employees_without_survey)} employees")
	
	return len(employees_without_survey)
