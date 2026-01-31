# Copyright (c) 2024, Nexelya and Contributors
# License: GNU General Public License v3. See license.txt

"""
Advanced Analytics & BI API
"""

import frappe
from frappe import _
from frappe.utils import flt, getdate, add_days
from erpnext.projects.api.feature_gating import check_feature_access


@frappe.whitelist()
def get_project_analytics(project=None, from_date=None, to_date=None, company=None):
	"""
	Get comprehensive project analytics
	
	Returns predictive analytics, KPIs, and insights
	"""
	if company:
		check_feature_access("advanced_analytics_bi", company, throw=True)
	
	filters = {}
	if project:
		filters["name"] = project
	if company:
		filters["company"] = company
	
	projects = frappe.get_all("Project", filters=filters, fields=["*"])
	
	analytics = {
		"projects": [],
		"summary": {
			"total_projects": len(projects),
			"total_value": 0,
			"total_cost": 0,
			"total_margin": 0,
			"at_risk_projects": 0
		}
	}
	
	for proj in projects:
		proj_doc = frappe.get_doc("Project", proj.name)
		proj_doc.update_costing()
		
		# Calculate risk score
		risk_score = calculate_project_risk(proj_doc)
		
		# Predict completion date
		predicted_completion = predict_completion_date(proj_doc)
		
		# Cost overrun prediction
		cost_overrun_risk = predict_cost_overrun(proj_doc)
		
		proj_analytics = {
			"name": proj.name,
			"project_name": proj.project_name,
			"status": proj.status,
			"estimated_cost": proj_doc.estimated_costing or 0,
			"total_committed_cost": proj_doc.total_committed_cost or 0,
			"total_actual_cost": proj_doc.total_actual_cost or 0,
			"gross_margin": proj_doc.gross_margin or 0,
			"per_gross_margin": proj_doc.per_gross_margin or 0,
			"risk_score": risk_score,
			"predicted_completion_date": predicted_completion,
			"cost_overrun_risk": cost_overrun_risk,
			"percent_complete": proj_doc.percent_complete or 0
		}
		
		analytics["projects"].append(proj_analytics)
		analytics["summary"]["total_value"] += proj_doc.estimated_costing or 0
		analytics["summary"]["total_cost"] += proj_doc.total_committed_cost or 0
		analytics["summary"]["total_margin"] += proj_doc.gross_margin or 0
		
		if risk_score > 70:
			analytics["summary"]["at_risk_projects"] += 1
	
	if analytics["summary"]["total_value"]:
		analytics["summary"]["overall_margin_percent"] = (
			analytics["summary"]["total_margin"] / analytics["summary"]["total_value"] * 100
		)
	
	return analytics


def calculate_project_risk(project_doc):
	"""
	Calculate project risk score (0-100)
	Higher score = higher risk
	"""
	risk_factors = 0
	
	# Cost overrun risk
	if project_doc.estimated_costing:
		cost_variance = ((project_doc.total_committed_cost or 0) - project_doc.estimated_costing) / project_doc.estimated_costing * 100
		if cost_variance > 10:
			risk_factors += 30
		elif cost_variance > 5:
			risk_factors += 15
	
	# Schedule risk
	if project_doc.expected_end_date and project_doc.actual_end_date:
		days_overdue = (getdate(project_doc.actual_end_date) - getdate(project_doc.expected_end_date)).days
		if days_overdue > 30:
			risk_factors += 30
		elif days_overdue > 0:
			risk_factors += 15
	elif project_doc.expected_end_date:
		days_remaining = (getdate(project_doc.expected_end_date) - getdate()).days
		if days_remaining < 0:
			risk_factors += 25
	
	# Margin risk
	if project_doc.per_gross_margin < 0:
		risk_factors += 25
	elif project_doc.per_gross_margin < 5:
		risk_factors += 15
	
	# Progress risk
	if project_doc.percent_complete < 50 and project_doc.expected_end_date:
		days_elapsed = (getdate() - getdate(project_doc.expected_start_date or getdate())).days
		total_days = (getdate(project_doc.expected_end_date) - getdate(project_doc.expected_start_date or getdate())).days
		if total_days > 0:
			expected_progress = (days_elapsed / total_days) * 100
			if project_doc.percent_complete < expected_progress - 10:
				risk_factors += 20
	
	return min(risk_factors, 100)


def predict_completion_date(project_doc):
	"""Predict project completion date based on current progress"""
	if not project_doc.expected_end_date or not project_doc.expected_start_date:
		return None
	
	if project_doc.percent_complete >= 100:
		return project_doc.actual_end_date or project_doc.expected_end_date
	
	if project_doc.percent_complete <= 0:
		return project_doc.expected_end_date
	
	# Calculate based on current progress rate
	days_elapsed = (getdate() - getdate(project_doc.expected_start_date)).days
	if days_elapsed <= 0:
		return project_doc.expected_end_date
	
	progress_rate = project_doc.percent_complete / days_elapsed
	if progress_rate <= 0:
		return project_doc.expected_end_date
	
	days_remaining = (100 - project_doc.percent_complete) / progress_rate
	predicted_date = add_days(getdate(), days_remaining)
	
	return predicted_date


def predict_cost_overrun(project_doc):
	"""
	Predict cost overrun risk and amount
	Returns: {"risk": "high/medium/low", "predicted_overrun": amount, "predicted_final_cost": amount}
	"""
	if not project_doc.estimated_costing:
		return {"risk": "unknown", "predicted_overrun": 0, "predicted_final_cost": 0}
	
	current_cost = project_doc.total_committed_cost or project_doc.total_actual_cost or 0
	progress = project_doc.percent_complete or 1  # Avoid division by zero
	
	if progress <= 0:
		return {"risk": "low", "predicted_overrun": 0, "predicted_final_cost": project_doc.estimated_costing}
	
	# Extrapolate final cost based on current spending rate
	if progress > 0:
		predicted_final_cost = (current_cost / progress) * 100
	else:
		predicted_final_cost = project_doc.estimated_costing
	
	predicted_overrun = predicted_final_cost - project_doc.estimated_costing
	
	overrun_percent = (predicted_overrun / project_doc.estimated_costing) * 100 if project_doc.estimated_costing else 0
	
	if overrun_percent > 15:
		risk = "high"
	elif overrun_percent > 5:
		risk = "medium"
	else:
		risk = "low"
	
	return {
		"risk": risk,
		"predicted_overrun": predicted_overrun,
		"predicted_final_cost": predicted_final_cost,
		"overrun_percent": overrun_percent
	}


@frappe.whitelist()
def get_custom_report_data(report_config, company=None):
	"""
	Execute custom SQL-based report
	
	Args:
		report_config: Dict with SQL query and filters
		company: Company for feature gating
	"""
	if company:
		check_feature_access("advanced_analytics_bi", company, throw=True)
	
	# Security: Only allow SELECT queries
	sql = report_config.get("sql", "").strip().upper()
	if not sql.startswith("SELECT"):
		frappe.throw(_("Only SELECT queries are allowed"))
	
	# Execute query
	try:
		result = frappe.db.sql(report_config.get("sql"), as_dict=True)
		return {
			"data": result,
			"count": len(result)
		}
	except Exception as e:
		frappe.throw(_("Query execution failed: {0}").format(str(e)))

