# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _


def process_chatbot_query(user_query, employee):
	"""Process chatbot queries and return appropriate responses"""
	
	query_lower = user_query.lower()
	
	# Leave balance queries
	if any(keyword in query_lower for keyword in ["leave balance", "leave remaining", "how many leaves"]):
		return get_leave_balance_response(employee)
	
	# Policy queries
	if any(keyword in query_lower for keyword in ["policy", "rules", "guidelines"]):
		return get_policy_response(query_lower)
	
	# Salary queries
	if any(keyword in query_lower for keyword in ["salary", "pay", "compensation"]):
		return get_salary_response(employee)
	
	# Attendance queries
	if any(keyword in query_lower for keyword in ["attendance", "present", "absent"]):
		return get_attendance_response(employee)
	
	# Default response
	return {
		"response": _("I can help you with leave balances, policies, salary information, and attendance. Please ask a specific question."),
		"suggestions": [
			"What is my leave balance?",
			"What are the leave policies?",
			"Show my salary information",
			"What is my attendance status?"
		]
	}


def get_leave_balance_response(employee):
	"""Get leave balance information"""
	from hrms.hr.doctype.leave_application.leave_application import get_leave_details
	from frappe.utils import getdate
	
	leave_details = get_leave_details(employee, getdate())
	leave_allocation = leave_details.get("leave_allocation", {})
	
	if not leave_allocation:
		return {
			"response": _("No leave allocation found for you."),
			"type": "leave_balance"
		}
	
	balance_text = _("Your leave balances:\n")
	for leave_type, details in leave_allocation.items():
		balance_text += f"{leave_type}: {details.get('remaining_leaves', 0)} days\n"
	
	return {
		"response": balance_text,
		"type": "leave_balance",
		"data": leave_allocation
	}


def get_policy_response(query):
	"""Get policy information"""
	# This would integrate with policy documents
	return {
		"response": _("Please refer to the HR Policies section in the app for detailed policy information."),
		"type": "policy",
		"link": "/app/hr-settings"
	}


def get_salary_response(employee):
	"""Get salary information"""
	latest_slip = frappe.db.get_value(
		"Salary Slip",
		{"employee": employee, "docstatus": 1},
		["name", "net_pay", "gross_pay"],
		order_by="start_date desc"
	)
	
	if not latest_slip:
		return {
			"response": _("No salary slip found."),
			"type": "salary"
		}
	
	return {
		"response": _("Your latest salary slip shows:\nGross Pay: {0}\nNet Pay: {1}").format(
			latest_slip.gross_pay or 0,
			latest_slip.net_pay or 0
		),
		"type": "salary",
		"data": {
			"gross_pay": latest_slip.gross_pay,
			"net_pay": latest_slip.net_pay
		}
	}


def get_attendance_response(employee):
	"""Get attendance information"""
	from datetime import datetime, timedelta
	
	today = datetime.now().date()
	month_start = today.replace(day=1)
	
	attendance_count = frappe.db.count(
		"Attendance",
		{
			"employee": employee,
			"attendance_date": [">=", month_start],
			"status": "Present",
			"docstatus": 1
		}
	)
	
	return {
		"response": _("You have been present for {0} days this month.").format(attendance_count),
		"type": "attendance",
		"data": {"present_days": attendance_count}
	}


@frappe.whitelist()
def chat_with_assistant(query, employee):
	"""API endpoint for chatbot"""
	try:
		return process_chatbot_query(query, employee)
	except Exception as e:
		frappe.log_error(f"Error in chat_with_assistant: {str(e)}")
		return {
			"response": _("I'm sorry, I encountered an error. Please try again or contact HR."),
			"type": "error"
		}
