"""AI features for construction management"""
import frappe
from frappe import _


@frappe.whitelist()
def summarize_daily_log(daily_log):
	"""Use AI to summarize a daily field report"""
	doc = frappe.get_doc("Daily Field Report", daily_log)
	
	# Build context
	context = f"""
	Daily Log for {doc.job_site} on {doc.report_date}
	
	Weather: {doc.weather_condition}, {doc.temperature}°F
	Total Man Hours: {doc.total_man_hours}
	
	Work Performed:
	{doc.work_performed}
	
	Issues/Delays:
	{doc.issues_delays or 'None reported'}
	"""
	
	# Call AI API (using existing next_ai or frappe_openai_integration)
	try:
		summary = call_ai_api(
			prompt="Summarize this construction daily log in 2-3 sentences for a project manager:",
			context=context
		)
		return {"summary": summary}
	except Exception as e:
		return {"error": str(e)}


@frappe.whitelist()
def suggest_rfi_response(rfi):
	"""Suggest a response for an RFI based on context"""
	doc = frappe.get_doc("RFI", rfi)
	
	context = f"""
	RFI Subject: {doc.subject}
	Description: {doc.description}
	Drawing Reference: {doc.get('drawing_reference', 'Not specified')}
	Spec Section: {doc.get('spec_section', 'Not specified')}
	"""
	
	try:
		suggestion = call_ai_api(
			prompt="Suggest a professional response for this construction RFI. Include any clarifications that may be needed:",
			context=context
		)
		return {"suggestion": suggestion}
	except Exception as e:
		return {"error": str(e)}


@frappe.whitelist()
def predict_cost_overrun(job_site):
	"""Predict likelihood of cost overrun based on historical data"""
	doc = frappe.get_doc("Job Site", job_site)
	
	# Get historical cost data
	cost_trend = frappe.db.sql("""
		SELECT posting_date, SUM(total_cost) as daily_cost
		FROM `tabJob Cost Entry`
		WHERE job_site = %s AND docstatus = 1
		GROUP BY posting_date
		ORDER BY posting_date
	""", job_site, as_dict=True)
	
	# Calculate burn rate
	if len(cost_trend) >= 7:
		recent_burn = sum([c.daily_cost for c in cost_trend[-7:]]) / 7
		total_spent = doc.actual_cost or 0
		remaining_budget = (doc.current_budget or 0) - total_spent
		
		# Days to completion estimate
		if recent_burn > 0:
			days_at_current_rate = remaining_budget / recent_burn
			planned_days_remaining = doc.days_remaining or 30
			
			risk_score = 0
			if doc.cpi and doc.cpi < 0.9:
				risk_score += 30
			if doc.spi and doc.spi < 0.9:
				risk_score += 20
			if days_at_current_rate < planned_days_remaining * 0.8:
				risk_score += 25
			
			return {
				"risk_score": min(risk_score, 100),
				"risk_level": "High" if risk_score > 50 else "Medium" if risk_score > 25 else "Low",
				"daily_burn_rate": recent_burn,
				"projected_overrun": max(0, (recent_burn * planned_days_remaining) - remaining_budget),
				"recommendation": get_risk_recommendation(risk_score)
			}
	
	return {
		"risk_score": 0,
		"risk_level": "Insufficient Data",
		"recommendation": "Need more cost data to predict overrun risk"
	}


def get_risk_recommendation(risk_score):
	"""Get recommendation based on risk score"""
	if risk_score > 50:
		return "Consider cost reduction measures and review scope. Schedule a project review meeting."
	elif risk_score > 25:
		return "Monitor costs closely. Review upcoming purchases and consider value engineering."
	else:
		return "Project is on track. Continue monitoring."


@frappe.whitelist()
def classify_document(file_url):
	"""Classify a construction document using AI"""
	# This would use document analysis AI
	categories = [
		"Drawing",
		"Specification",
		"Contract",
		"Change Order",
		"RFI",
		"Submittal",
		"Invoice",
		"Safety Report",
		"Inspection Report",
		"Meeting Minutes",
		"Other"
	]
	
	try:
		classification = call_ai_api(
			prompt=f"Classify this construction document into one of these categories: {', '.join(categories)}",
			context=f"Document URL: {file_url}"
		)
		return {"category": classification}
	except Exception as e:
		return {"error": str(e)}


def call_ai_api(prompt, context):
	"""Call the AI API - integrates with existing AI apps"""
	# Try to use existing AI integration
	if "next_ai" in frappe.get_installed_apps():
		# Use Next AI
		from next_ai.api import generate_response
		return generate_response(prompt=prompt, context=context)
	
	elif "frappe_openai_integration" in frappe.get_installed_apps():
		# Use OpenAI integration
		from frappe_openai_integration.api import complete
		return complete(prompt=f"{prompt}\n\nContext:\n{context}")
	
	else:
		# Fallback - no AI available
		raise Exception("No AI integration available. Install next_ai or frappe_openai_integration.")
