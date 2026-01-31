import frappe
from frappe import _
from frappe.utils import getdate, today, add_days


@frappe.whitelist()
def calculate_customer_health(organization_name):
	"""
	Calculate customer health score
	"""
	org = frappe.get_doc("CRM Organization", organization_name)

	if not org:
		return {"health_score": 0, "factors": []}

	factors = []
	health_score = 100  # Start with perfect score

	# Factor 1: Recent Activity (-20 points if no activity in 90 days)
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
			health_score -= 20
			factors.append({
				"name": "No Recent Activity",
				"impact": -20,
				"details": f"{days_since_activity} days since last activity",
			})
		elif days_since_activity > 60:
			health_score -= 10
			factors.append({
				"name": "Low Activity",
				"impact": -10,
				"details": f"{days_since_activity} days since last activity",
			})
	else:
		health_score -= 20
		factors.append({
			"name": "No Activity Recorded",
			"impact": -20,
			"details": "No tasks or activities found",
		})

	# Factor 2: Support Tickets (-15 points for open tickets)
	open_tickets = frappe.db.count(
		"CRM Ticket",
		filters={
			"organization": organization_name,
			"status": ["not in", ["Resolved", "Closed"]],
		},
	) if frappe.db.exists("DocType", "CRM Ticket") else 0

	if open_tickets > 3:
		health_score -= 15
		factors.append({
			"name": "Multiple Open Tickets",
			"impact": -15,
			"details": f"{open_tickets} open support tickets",
		})
	elif open_tickets > 0:
		health_score -= 5
		factors.append({
			"name": "Open Support Tickets",
			"impact": -5,
			"details": f"{open_tickets} open ticket(s)",
		})

	# Factor 3: Deal Status (-10 points for lost deals)
	lost_deals = frappe.db.count(
		"CRM Deal",
		filters={
			"organization": organization_name,
			"status": "Lost",
			"creation": [">=", add_days(today(), -90)],
		},
	)

	if lost_deals > 2:
		health_score -= 10
		factors.append({
			"name": "Recent Lost Deals",
			"impact": -10,
			"details": f"{lost_deals} deals lost in last 90 days",
		})

	# Factor 4: Active Deals (+10 points for active deals)
	active_deals = frappe.db.count(
		"CRM Deal",
		filters={
			"organization": organization_name,
			"status": ["not in", ["Won", "Lost"]],
		},
	)

	if active_deals > 0:
		health_score += min(10, active_deals * 2)
		factors.append({
			"name": "Active Deals",
			"impact": min(10, active_deals * 2),
			"details": f"{active_deals} active deal(s)",
		})

	# Normalize to 0-100
	health_score = max(0, min(100, health_score))

	# Determine health level
	if health_score >= 80:
		health_level = "Excellent"
		health_color = "green"
	elif health_score >= 60:
		health_level = "Good"
		health_color = "blue"
	elif health_score >= 40:
		health_level = "Fair"
		health_color = "yellow"
	else:
		health_level = "At Risk"
		health_color = "red"

	return {
		"health_score": flt(health_score, 2),
		"health_level": health_level,
		"health_color": health_color,
		"factors": factors,
		"churn_risk": 100 - health_score,
	}

