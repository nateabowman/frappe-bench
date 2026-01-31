# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _
from datetime import datetime


def get_approval_workload(approver):
	"""Calculate current approval workload for an approver"""
	
	pending_approvals = {
		"Leave Application": frappe.db.count("Leave Application", {
			"leave_approver": approver,
			"docstatus": 0,
			"status": "Open"
		}),
		"Expense Claim": frappe.db.count("Expense Claim", {
			"expense_approver": approver,
			"docstatus": 0,
			"approval_status": "Draft"
		}),
		"Shift Request": frappe.db.count("Shift Request", {
			"approver": approver,
			"docstatus": 0,
			"status": "Draft"
		}),
		"Attendance Request": frappe.db.count("Attendance Request", {
			"docstatus": 0
		}),
	}
	
	total_pending = sum(pending_approvals.values())
	
	return {
		"by_doctype": pending_approvals,
		"total": total_pending,
		"workload_level": "high" if total_pending > 20 else "medium" if total_pending > 10 else "low"
	}


def suggest_delegation(approver, doctype):
	"""Suggest delegation based on workload and hierarchy"""
	
	# Get approver's employee record
	employee = frappe.db.get_value("Employee", {"user_id": approver}, "name")
	if not employee:
		return None
	
	emp_doc = frappe.get_cached_doc("Employee", employee)
	
	# Get direct reports
	direct_reports = frappe.get_all(
		"Employee",
		filters={"reports_to": employee, "status": "Active"},
		fields=["name", "user_id", "employee_name"]
	)
	
	if not direct_reports:
		return None
	
	# Find report with lowest workload
	best_delegate = None
	lowest_workload = float("inf")
	
	for report in direct_reports:
		if report.user_id:
			workload = get_approval_workload(report.user_id)
			if workload["total"] < lowest_workload:
				lowest_workload = workload["total"]
				best_delegate = report
	
	return {
		"suggested_delegate": best_delegate.employee_name if best_delegate else None,
		"delegate_user_id": best_delegate.user_id if best_delegate else None,
		"reason": _("Lowest current workload among direct reports")
	}


def auto_escalate_approvals(doctype, days_threshold=3):
	"""Auto-escalate approvals that have been pending for too long"""
	
	from datetime import timedelta
	threshold_date = datetime.now() - timedelta(days=days_threshold)
	
	# Get pending approvals older than threshold
	pending_docs = frappe.get_all(
		doctype,
		filters={
			"docstatus": 0,
			"creation": ["<", threshold_date]
		},
		fields=["name", "employee", "leave_approver" if doctype == "Leave Application" else "approver"]
	)
	
	escalated = []
	for doc in pending_docs:
		approver_field = "leave_approver" if doctype == "Leave Application" else "approver"
		current_approver = doc.get(approver_field)
		
		if current_approver:
			# Get employee's manager
			employee_doc = frappe.get_cached_doc("Employee", doc.employee)
			if employee_doc.reports_to:
				manager = frappe.get_cached_doc("Employee", employee_doc.reports_to)
				if manager.user_id and manager.user_id != current_approver:
					# Escalate to manager
					frappe.db.set_value(doctype, doc.name, approver_field, manager.user_id)
					escalated.append(doc.name)
	
	return {"escalated": escalated, "count": len(escalated)}


@frappe.whitelist()
def get_approval_workload_status(approver):
	"""API endpoint for approval workload"""
	try:
		return get_approval_workload(approver)
	except Exception as e:
		frappe.log_error(f"Error in get_approval_workload_status: {str(e)}")
		frappe.throw(_("Error fetching approval workload"))


@frappe.whitelist()
def get_delegation_suggestion(approver, doctype):
	"""API endpoint for delegation suggestions"""
	try:
		return suggest_delegation(approver, doctype)
	except Exception as e:
		frappe.log_error(f"Error in get_delegation_suggestion: {str(e)}")
		frappe.throw(_("Error generating delegation suggestion"))
