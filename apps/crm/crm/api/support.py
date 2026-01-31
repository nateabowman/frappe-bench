import frappe
from frappe import _
from frappe.utils import now, getdate, today, flt


@frappe.whitelist()
def create_ticket(subject, description, organization=None, contact=None, priority="Medium"):
	"""
	Create a support ticket
	"""
	# Validate inputs
	if not subject:
		frappe.throw(_("Subject is required"))
	
	if not description:
		frappe.throw(_("Description is required"))
	
	# Validate priority
	allowed_priorities = ["Low", "Medium", "High", "Critical"]
	if priority not in allowed_priorities:
		frappe.throw(_("Invalid priority"))
	
	# Validate organization if provided
	if organization and not frappe.db.exists("CRM Organization", organization):
		frappe.throw(_("Invalid organization"))
	
	# Validate contact if provided
	if contact and not frappe.db.exists("CRM Contact", contact):
		frappe.throw(_("Invalid contact"))
	
	ticket = frappe.get_doc({
		"doctype": "CRM Ticket",
		"subject": subject,
		"description": description,
		"organization": organization,
		"contact": contact,
		"priority": priority,
		"status": "Open",
		"opened_by": frappe.session.user,
		"opened_on": now(),
	})
	ticket.insert()

	return ticket.name


@frappe.whitelist()
def assign_ticket(ticket_name, assignee):
	"""
	Assign a ticket to a user
	"""
	# Validate inputs
	if not ticket_name:
		frappe.throw(_("Ticket name is required"))
	
	if not assignee:
		frappe.throw(_("Assignee is required"))
	
	# Check if ticket exists
	if not frappe.db.exists("CRM Ticket", ticket_name):
		frappe.throw(_("Ticket not found"))
	
	# Validate assignee exists
	if not frappe.db.exists("User", assignee):
		frappe.throw(_("Invalid assignee"))
	
	ticket = frappe.get_doc("CRM Ticket", ticket_name)
	
	# Check permissions
	if not frappe.has_permission("CRM Ticket", "write", ticket):
		frappe.throw(_("Not permitted to modify this ticket"), frappe.PermissionError)
	
	# Only ticket owner, assigned user, or managers can assign tickets
	roles = frappe.get_roles()
	can_assign = (
		ticket.opened_by == frappe.session.user or
		ticket.assigned_to == frappe.session.user or
		"Support Manager" in roles or
		frappe.session.user == "Administrator"
	)
	
	if not can_assign:
		frappe.throw(_("Not permitted to assign this ticket"), frappe.PermissionError)
	
	ticket.assigned_to = assignee
	ticket.save()

	return {"status": "assigned"}


@frappe.whitelist()
def update_ticket_status(ticket_name, status, resolution=None):
	"""
	Update ticket status
	"""
	# Validate inputs
	if not ticket_name:
		frappe.throw(_("Ticket name is required"))
	
	if not status:
		frappe.throw(_("Status is required"))
	
	# Validate status
	allowed_statuses = ["Open", "In Progress", "Resolved", "Closed"]
	if status not in allowed_statuses:
		frappe.throw(_("Invalid status"))
	
	# Check if ticket exists
	if not frappe.db.exists("CRM Ticket", ticket_name):
		frappe.throw(_("Ticket not found"))
	
	ticket = frappe.get_doc("CRM Ticket", ticket_name)
	
	# Check permissions
	if not frappe.has_permission("CRM Ticket", "write", ticket):
		frappe.throw(_("Not permitted to modify this ticket"), frappe.PermissionError)
	
	# Only ticket owner, assigned user, or managers can update ticket status
	roles = frappe.get_roles()
	can_update = (
		ticket.opened_by == frappe.session.user or
		ticket.assigned_to == frappe.session.user or
		"Support Manager" in roles or
		frappe.session.user == "Administrator"
	)
	
	if not can_update:
		frappe.throw(_("Not permitted to update this ticket"), frappe.PermissionError)
	
	ticket.status = status
	
	if status == "Resolved" and resolution:
		ticket.resolution = resolution
		ticket.resolved_on = now()
		ticket.resolved_by = frappe.session.user
	
	ticket.save()

	return {"status": "updated"}


@frappe.whitelist()
def get_ticket_metrics(from_date=None, to_date=None, user=None):
	"""
	Get support ticket metrics
	"""
	# Validate user parameter if provided
	if user:
		if not frappe.db.exists("User", user):
			frappe.throw(_("Invalid user"))
		
		# Users can only view their own metrics unless they're managers
		roles = frappe.get_roles()
		if user != frappe.session.user and "Support Manager" not in roles and frappe.session.user != "Administrator":
			frappe.throw(_("Not permitted to view metrics for other users"), frappe.PermissionError)
	
	filters = {}
	if from_date:
		filters["creation"] = [">=", from_date]
	if to_date:
		filters["creation"] = ["<=", to_date]
	if user:
		filters["assigned_to"] = user
	else:
		# If no user specified, limit to current user's tickets unless manager
		roles = frappe.get_roles()
		if "Support Manager" not in roles and frappe.session.user != "Administrator":
			filters["assigned_to"] = frappe.session.user

	tickets = frappe.get_all(
		"CRM Ticket",
		filters=filters,
		fields=["name", "status", "priority", "creation", "resolved_on"],
	)

	total = len(tickets)
	open_tickets = len([t for t in tickets if t.status == "Open"])
	resolved = len([t for t in tickets if t.status == "Resolved"])
	closed = len([t for t in tickets if t.status == "Closed"])

	# Calculate average resolution time
	resolution_times = []
	for t in tickets:
		if t.resolved_on and t.creation:
			days = (getdate(t.resolved_on) - getdate(t.creation)).days
			resolution_times.append(days)

	avg_resolution_time = sum(resolution_times) / len(resolution_times) if resolution_times else 0

	return {
		"total": total,
		"open": open_tickets,
		"resolved": resolved,
		"closed": closed,
		"avg_resolution_time_days": flt(avg_resolution_time, 2),
	}

