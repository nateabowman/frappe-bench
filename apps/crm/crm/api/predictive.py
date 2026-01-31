import frappe
from frappe import _
from frappe.utils import getdate, flt, today
import json


@frappe.whitelist()
def calculate_deal_win_probability(deal_name):
	"""
	Calculate win probability for a deal using multiple factors
	"""
	deal = frappe.get_doc("CRM Deal", deal_name)

	if not deal:
		return {"probability": 0, "factors": []}

	factors = []
	total_score = 0

	# Factor 1: Deal Stage (0-30 points)
	stage_scores = {
		"Qualification": 5,
		"Proposal": 15,
		"Negotiation": 25,
		"Closed Won": 30,
	}
	stage_score = stage_scores.get(deal.status, 10)
	factors.append({
		"name": "Deal Stage",
		"score": stage_score,
		"max": 30,
		"weight": "high",
	})
	total_score += stage_score

	# Factor 2: Deal Age (0-15 points)
	if deal.creation:
		days_old = (getdate(today()) - getdate(deal.creation)).days
		if days_old < 30:
			age_score = 15
		elif days_old < 60:
			age_score = 12
		elif days_old < 90:
			age_score = 8
		else:
			age_score = 5
		factors.append({
			"name": "Deal Age",
			"score": age_score,
			"max": 15,
			"weight": "medium",
		})
		total_score += age_score

	# Factor 3: Deal Value (0-20 points)
	if deal.deal_value:
		if deal.deal_value > 100000:
			value_score = 20
		elif deal.deal_value > 50000:
			value_score = 15
		elif deal.deal_value > 10000:
			value_score = 10
		else:
			value_score = 5
		factors.append({
			"name": "Deal Value",
			"score": value_score,
			"max": 20,
			"weight": "high",
		})
		total_score += value_score

	# Factor 4: Activity Level (0-15 points)
	# Count recent activities
	recent_activities = frappe.db.count(
		"CRM Task",
		filters={
			"reference_doctype": "CRM Deal",
			"reference_docname": deal.name,
			"creation": [">=", frappe.utils.add_days(today(), -30)],
		},
	)
	activity_score = min(15, recent_activities * 3)
	factors.append({
		"name": "Recent Activity",
		"score": activity_score,
		"max": 15,
		"weight": "medium",
	})
	total_score += activity_score

	# Factor 5: Expected Closure Date (0-20 points)
	if deal.expected_closure_date:
		days_until_close = (getdate(deal.expected_closure_date) - getdate(today())).days
		if 0 <= days_until_close <= 30:
			closure_score = 20
		elif 31 <= days_until_close <= 60:
			closure_score = 15
		elif 61 <= days_until_close <= 90:
			closure_score = 10
		else:
			closure_score = 5
		factors.append({
			"name": "Closure Timeline",
			"score": closure_score,
			"max": 20,
			"weight": "high",
		})
		total_score += closure_score

	# Calculate final probability (0-100%)
	probability = min(100, (total_score / 100) * 100)

	# Update deal probability if different
	if abs(flt(deal.probability or 0) - probability) > 5:
		deal.db_set("probability", flt(probability, 2))

	return {
		"probability": flt(probability, 2),
		"factors": factors,
		"total_score": total_score,
		"max_score": 100,
	}


@frappe.whitelist()
def predict_churn_risk(organization_name):
	"""
	Predict churn risk for an organization
	"""
	org = frappe.get_doc("CRM Organization", organization_name)

	if not org:
		return {"risk_score": 0, "factors": []}

	factors = []
	risk_score = 0

	# Factor 1: Last Activity Date (0-30 points)
	last_activity = frappe.db.sql(
		"""
		SELECT MAX(creation)
		FROM `tabCRM Task`
		WHERE reference_doctype = 'CRM Organization'
		AND reference_docname = %s
		""",
		(organization_name,),
		as_list=True,
	)[0][0]

	if last_activity:
		days_since_activity = (getdate(today()) - getdate(last_activity)).days
		if days_since_activity > 90:
			risk_score += 30
		elif days_since_activity > 60:
			risk_score += 20
		elif days_since_activity > 30:
			risk_score += 10
		factors.append({
			"name": "Days Since Last Activity",
			"value": days_since_activity,
			"risk_contribution": min(30, days_since_activity / 3),
		})
	else:
		risk_score += 30
		factors.append({
			"name": "No Recent Activity",
			"value": "Never",
			"risk_contribution": 30,
		})

	# Factor 2: Support Tickets (0-25 points)
	open_tickets = frappe.db.count(
		"CRM Ticket",
		filters={
			"organization": organization_name,
			"status": ["not in", ["Resolved", "Closed"]],
		},
	) if frappe.db.exists("DocType", "CRM Ticket") else 0

	if open_tickets > 5:
		risk_score += 25
		factors.append({
			"name": "Open Support Tickets",
			"value": open_tickets,
			"risk_contribution": 25,
		})
	elif open_tickets > 2:
		risk_score += 15
		factors.append({
			"name": "Open Support Tickets",
			"value": open_tickets,
			"risk_contribution": 15,
		})

	# Factor 3: Deal Status (0-25 points)
	lost_deals = frappe.db.count(
		"CRM Deal",
		filters={
			"organization": organization_name,
			"status": "Lost",
			"creation": [">=", frappe.utils.add_days(today(), -90)],
		},
	)

	if lost_deals > 2:
		risk_score += 25
		factors.append({
			"name": "Recent Lost Deals",
			"value": lost_deals,
			"risk_contribution": 25,
		})

	# Factor 4: Contract Renewal (0-20 points)
	# Simplified - would need contract management
	# For now, check if there are any active deals
	active_deals = frappe.db.count(
		"CRM Deal",
		filters={
			"organization": organization_name,
			"status": ["not in", ["Won", "Lost"]],
		},
	)

	if active_deals == 0:
		risk_score += 20
		factors.append({
			"name": "No Active Deals",
			"value": "None",
			"risk_contribution": 20,
		})

	# Normalize to 0-100
	churn_risk = min(100, risk_score)

	return {
		"risk_score": flt(churn_risk, 2),
		"risk_level": "High" if churn_risk > 70 else "Medium" if churn_risk > 40 else "Low",
		"factors": factors,
	}


@frappe.whitelist()
def get_next_best_action(deal_name):
	"""
	Recommend next best action for a deal
	"""
	deal = frappe.get_doc("CRM Deal", deal_name)

	if not deal:
		return {"action": "No recommendation", "reason": "Deal not found"}

	# Get recent activities
	recent_tasks = frappe.get_all(
		"CRM Task",
		filters={
			"reference_doctype": "CRM Deal",
			"reference_docname": deal.name,
		},
		order_by="creation desc",
		limit=5,
	)

	# Get last call
	last_call = frappe.db.get_all(
		"CRM Call Log",
		filters={
			"reference_doctype": "CRM Deal",
			"reference_docname": deal.name,
		},
		order_by="creation desc",
		limit=1,
	)

	# Recommendation logic
	if deal.status == "Qualification":
		return {
			"action": "Schedule Discovery Call",
			"reason": "Deal is in qualification stage",
			"priority": "high",
			"type": "call",
		}

	if deal.status == "Proposal" and not recent_tasks:
		return {
			"action": "Send Proposal Follow-up",
			"reason": "No recent activity on proposal",
			"priority": "high",
			"type": "email",
		}

	if deal.expected_closure_date:
		days_until_close = (getdate(deal.expected_closure_date) - getdate(today())).days
		if days_until_close <= 7:
			return {
				"action": "Urgent: Schedule Closing Call",
				"reason": f"Deal closing in {days_until_close} days",
				"priority": "urgent",
				"type": "call",
			}

	if not last_call:
		return {
			"action": "Make Initial Contact Call",
			"reason": "No calls logged for this deal",
			"priority": "medium",
			"type": "call",
		}

	# Default recommendation
	return {
		"action": "Update Deal Status",
		"reason": "Keep deal information current",
		"priority": "low",
		"type": "task",
	}


@frappe.whitelist()
def get_revenue_forecast_ml(from_date=None, to_date=None, user=None):
	"""
	ML-based revenue forecasting (simplified version)
	"""
	from crm.api.analytics import get_revenue_forecast

	# Get base forecast
	forecast = get_revenue_forecast(from_date, to_date, user)

	# Apply ML adjustments (simplified - would use actual ML model)
	# For now, apply historical conversion rate adjustments
	historical_conversion = frappe.db.sql(
		"""
		SELECT 
			COUNT(CASE WHEN status = 'Won' THEN 1 END) * 100.0 / COUNT(*) as conversion_rate
		FROM `tabCRM Deal`
		WHERE creation >= DATE_SUB(NOW(), INTERVAL 90 DAY)
		AND docstatus != 2
		""",
		as_list=True,
	)[0][0] or 0

	# Adjust forecast based on historical conversion
	adjusted_forecast = forecast["total_weighted_revenue"] * (historical_conversion / 100)

	return {
		"base_forecast": forecast["total_weighted_revenue"],
		"adjusted_forecast": flt(adjusted_forecast, 2),
		"confidence": min(95, max(60, historical_conversion)),
		"historical_conversion_rate": flt(historical_conversion, 2),
		"monthly_breakdown": forecast["monthly_breakdown"],
	}

