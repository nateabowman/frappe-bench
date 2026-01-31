import frappe
from frappe import _


@frappe.whitelist()
def get_email_suggestions(context, recipient_email=None):
	"""
	Get AI-powered email content suggestions
	"""
	# Simplified version - would integrate with actual AI service
	suggestions = []

	# Get context from document
	if context.get("doctype") and context.get("docname"):
		doc = frappe.get_doc(context["doctype"], context["docname"])
		
		# Generate greeting
		if recipient_email:
			contact = frappe.db.get_value("CRM Contact", {"email": recipient_email}, "first_name")
			if contact:
				suggestions.append({
					"type": "greeting",
					"text": f"Hi {contact},",
				})

		# Generate context-based suggestions
		if context["doctype"] == "CRM Deal":
			suggestions.append({
				"type": "body",
				"text": f"I wanted to follow up on our discussion about {doc.name}. I believe this could be a great fit for your needs.",
			})
		elif context["doctype"] == "CRM Lead":
			suggestions.append({
				"type": "body",
				"text": f"Thank you for your interest in our services. I'd love to schedule a call to discuss how we can help.",
			})

		# Generate closing
		suggestions.append({
			"type": "closing",
			"text": "Looking forward to hearing from you.",
		})

	return {
		"suggestions": suggestions,
		"full_text": "\n\n".join([s["text"] for s in suggestions]),
	}


@frappe.whitelist()
def analyze_sentiment(text):
	"""
	Analyze sentiment of communication text
	"""
	# Simplified sentiment analysis
	positive_words = ["great", "excellent", "good", "happy", "pleased", "thank", "appreciate"]
	negative_words = ["bad", "terrible", "disappointed", "unhappy", "problem", "issue", "concern"]

	text_lower = text.lower()
	positive_count = sum(1 for word in positive_words if word in text_lower)
	negative_count = sum(1 for word in negative_words if word in text_lower)

	if positive_count > negative_count:
		sentiment = "positive"
		score = min(1.0, 0.5 + (positive_count - negative_count) * 0.1)
	elif negative_count > positive_count:
		sentiment = "negative"
		score = max(0.0, 0.5 - (negative_count - positive_count) * 0.1)
	else:
		sentiment = "neutral"
		score = 0.5

	return {
		"sentiment": sentiment,
		"score": score,
		"positive_words": positive_count,
		"negative_words": negative_count,
	}


@frappe.whitelist()
def get_smart_reply_suggestions(communication_text, context=None):
	"""
	Get smart reply suggestions based on incoming communication
	"""
	# Simplified smart reply - would use actual AI
	suggestions = []

	if "thank" in communication_text.lower():
		suggestions.append("You're welcome! Happy to help.")
	
	if "meeting" in communication_text.lower() or "call" in communication_text.lower():
		suggestions.append("I'd be happy to schedule a call. What time works best for you?")
	
	if "price" in communication_text.lower() or "cost" in communication_text.lower():
		suggestions.append("I'd be happy to discuss pricing options. Let me send you our pricing information.")
	
	if "question" in communication_text.lower():
		suggestions.append("I'd be happy to answer your questions. What would you like to know?")

	# Default suggestions
	if not suggestions:
		suggestions = [
			"Thank you for reaching out. I'll get back to you shortly.",
			"I appreciate your message. Let me look into this and get back to you.",
		]

	return {
		"suggestions": suggestions[:3],  # Return top 3
	}


@frappe.whitelist()
def auto_categorize_communication(communication_text, doctype=None, docname=None):
	"""
	Automatically categorize communication
	"""
	categories = {
		"inquiry": ["question", "interested", "information", "tell me"],
		"support": ["problem", "issue", "help", "support", "error"],
		"sales": ["price", "cost", "quote", "purchase", "buy"],
		"meeting": ["meeting", "call", "schedule", "appointment"],
		"follow_up": ["follow up", "checking in", "status", "update"],
	}

	text_lower = communication_text.lower()
	
	# Find matching category
	for category, keywords in categories.items():
		if any(keyword in text_lower for keyword in keywords):
			return {
				"category": category,
				"confidence": 0.8,
			}

	return {
		"category": "general",
		"confidence": 0.5,
	}


@frappe.whitelist()
def extract_document_data(file_url, file_type=None):
	"""
	Extract data from documents (emails, PDFs, etc.)
	"""
	# Simplified - would use actual document parsing/AI
	return {
		"extracted_data": {},
		"entities": [],
		"summary": "Document processing would be implemented here",
	}


@frappe.whitelist()
def get_ai_insights(reference_type, reference_name):
	"""
	Get AI insights for a specific record
	"""
	insights = frappe.get_all(
		"CRM AI Insight",
		filters={
			"reference_type": reference_type,
			"reference_name": reference_name,
			"is_active": 1
		},
		fields=["*"],
		order_by="generated_at desc",
		limit=10
	)
	
	return insights


@frappe.whitelist()
def generate_ai_insight(reference_type, reference_name, insight_type="Predictive Analytics"):
	"""
	Generate AI insight for a record
	"""
	# Get the document
	doc = frappe.get_doc(reference_type, reference_name)
	
	# Generate insight based on type
	insight_data = {
		"reference_type": reference_type,
		"reference_name": reference_name,
		"insight_type": insight_type,
		"generated_by": frappe.session.user,
	}
	
	if insight_type == "Deal Health Score":
		# Calculate health score based on deal data
		health_score = calculate_deal_health_score(doc)
		insight_data.update({
			"insight_title": "Deal Health Score",
			"insight_description": f"This deal has a health score of {health_score}% based on various factors.",
			"health_score": health_score,
			"confidence_score": 0.85,
		})
	elif insight_type == "Next Best Action":
		next_action = suggest_next_action(doc)
		insight_data.update({
			"insight_title": "Next Best Action",
			"insight_description": next_action.get("description", ""),
			"next_best_action": next_action.get("action", ""),
			"confidence_score": next_action.get("confidence", 0.7),
		})
	elif insight_type == "Predictive Analytics":
		prediction = predict_deal_outcome(doc)
		insight_data.update({
			"insight_title": "Predictive Analytics",
			"insight_description": prediction.get("description", ""),
			"predicted_value": prediction.get("value"),
			"predicted_close_date": prediction.get("close_date"),
			"confidence_score": prediction.get("confidence", 0.75),
		})
	
	# Create insight document
	insight = frappe.get_doc({
		"doctype": "CRM AI Insight",
		**insight_data
	})
	insight.insert()
	frappe.db.commit()
	
	return insight.as_dict()


def calculate_deal_health_score(doc):
	"""Calculate deal health score"""
	score = 50  # Base score
	
	# Factors that increase score
	if doc.get("probability"):
		score += doc.probability * 0.3
	if doc.get("deal_value"):
		score += min(20, doc.deal_value / 10000)  # Cap at 20 points
	if doc.get("expected_closure_date"):
		days_until_close = (getdate(doc.expected_closure_date) - getdate(today())).days
		if 0 <= days_until_close <= 30:
			score += 10  # Urgency bonus
	
	# Factors that decrease score
	if not doc.get("contacts"):
		score -= 10
	if not doc.get("organization"):
		score -= 10
	
	return min(100, max(0, score))


def suggest_next_action(doc):
	"""Suggest next best action"""
	actions = []
	
	if not doc.get("contacts"):
		actions.append({
			"action": "Add Contact",
			"description": "Add a contact to this deal to improve engagement.",
			"confidence": 0.9
		})
	
	if doc.get("status") == "Open" and not doc.get("expected_closure_date"):
		actions.append({
			"action": "Set Expected Close Date",
			"description": "Setting an expected close date helps track deal progress.",
			"confidence": 0.85
		})
	
	if doc.get("probability") and doc.probability < 50:
		actions.append({
			"action": "Schedule Follow-up",
			"description": "Schedule a follow-up call or meeting to move the deal forward.",
			"confidence": 0.8
		})
	
	return actions[0] if actions else {
		"action": "Continue Engagement",
		"description": "Continue regular engagement with the customer.",
		"confidence": 0.7
	}


def predict_deal_outcome(doc):
	"""Predict deal outcome"""
	from frappe.utils import getdate, today, add_days
	
	# Simple prediction based on probability and historical data
	predicted_value = doc.get("deal_value") or doc.get("expected_deal_value") or 0
	if doc.get("probability"):
		predicted_value = predicted_value * (doc.probability / 100)
	
	# Predict close date
	if doc.get("expected_closure_date"):
		predicted_close_date = doc.expected_closure_date
	else:
		# Default to 30 days from now
		predicted_close_date = add_days(today(), 30)
	
	confidence = doc.get("probability", 50) / 100 if doc.get("probability") else 0.5
	
	return {
		"value": predicted_value,
		"close_date": predicted_close_date,
		"confidence": confidence,
		"description": f"Based on current data, this deal has a {doc.get('probability', 50)}% probability of closing with an estimated value of {predicted_value}."
	}


@frappe.whitelist()
def get_recommendations(reference_type, reference_name):
	"""
	Get AI recommendations for a record
	"""
	doc = frappe.get_doc(reference_type, reference_name)
	recommendations = []
	
	# Generate various recommendations
	next_action = suggest_next_action(doc)
	recommendations.append({
		"type": "action",
		"title": "Next Best Action",
		"description": next_action.get("description"),
		"action": next_action.get("action"),
		"priority": "high"
	})
	
	return {
		"recommendations": recommendations,
		"total": len(recommendations)
	}


@frappe.whitelist()
def chat_with_ai(reference_type, reference_name, message):
	"""
	Chat with AI assistant about a specific record
	"""
	if not message:
		frappe.throw(_("Message is required"))
	
	# Get document context
	doc = frappe.get_doc(reference_type, reference_name)
	
	# Simplified AI response - would integrate with actual AI service
	response = {
		"message": f"I received your message about {reference_type} {reference_name}: {message}. This is a placeholder response. Actual AI integration would be implemented here.",
		"reference_type": reference_type,
		"reference_name": reference_name
	}
	
	return response

