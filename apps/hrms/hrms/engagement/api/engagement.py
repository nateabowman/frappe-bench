# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _
from datetime import datetime, timedelta
from collections import defaultdict


@frappe.whitelist()
def get_engagement_score(employee=None, department=None):
	"""Calculate employee engagement score"""
	
	# This is a placeholder - would integrate with pulse surveys
	# For now, return a calculated score based on various factors
	
	filters = {}
	if employee:
		filters["employee"] = employee
	if department:
		filters["department"] = department
	
	# Factors that contribute to engagement:
	# 1. Recent appraisals (positive feedback)
	# 2. Training participation
	# 3. Recognition received
	# 4. Leave utilization (balanced usage)
	
	score = 70  # Base score
	
	# Check for recent positive appraisals
	if employee:
		recent_appraisal = frappe.db.get_value(
			"Appraisal",
			{"employee": employee, "docstatus": 1},
			["final_score"],
			order_by="creation desc"
		)
		if recent_appraisal and recent_appraisal > 80:
			score += 10
	
	# Check for training participation
	if employee:
		training_count = frappe.db.count(
			"Training Event Employee",
			{"employee": employee}
		)
		if training_count > 0:
			score += 5
	
	return {
		"overall_score": min(score, 100),
		"factors": {
			"appraisals": recent_appraisal if employee else None,
			"training": training_count if employee else None
		}
	}


@frappe.whitelist()
def get_recognition_summary(employee=None, department=None):
	"""Get recognition summary for employee or department"""
	
	filters = {}
	if employee:
		filters["employee"] = employee
	if department:
		filters["department"] = department
	
	# This would query Employee Recognition doctype when created
	# For now, return placeholder
	return {
		"total_recognitions": 0,
		"recent_recognitions": [],
		"by_type": {}
	}


@frappe.whitelist()
def get_announcements(employee=None, department=None):
	"""Get relevant announcements"""
	
	filters = {"published": 1}
	
	# Get company-wide and department-specific announcements
	announcements = frappe.get_all(
		"Announcement",
		filters=filters,
		fields=["name", "title", "message", "department", "publish_date"],
		order_by="publish_date desc",
		limit=10
	)
	
	# Filter by department if specified
	if department:
		relevant = [a for a in announcements if not a.department or a.department == department]
	else:
		relevant = [a for a in announcements if not a.department]
	
	return {
		"announcements": relevant[:5],
		"total": len(relevant)
	}
