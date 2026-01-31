import frappe
from frappe import _
from frappe.utils import now
import json


@frappe.whitelist()
def get_activity_feed(doctype=None, docname=None, limit=50):
	"""
	Get activity feed for a document or global feed
	"""
	# Validate limit
	if limit and (not isinstance(limit, int) or limit < 1 or limit > 1000):
		frappe.throw(_("Invalid limit. Must be between 1 and 1000"))
	
	# Validate doctype and docname if provided
	if doctype and docname:
		# Validate doctype exists
		if not frappe.db.exists("DocType", doctype):
			frappe.throw(_("Invalid doctype"))
		
		# Check permissions on the document
		if not frappe.has_permission(doctype, "read", docname):
			frappe.throw(_("Not permitted to access this document"), frappe.PermissionError)
	
	filters = {}
	if doctype and docname:
		filters["reference_doctype"] = doctype
		filters["reference_docname"] = docname

	# Get comments
	comments = frappe.get_all(
		"Comment",
		filters={
			**filters,
			"comment_type": "Comment",
		},
		fields=["name", "content", "owner", "creation", "reference_doctype", "reference_docname"],
		order_by="creation desc",
		limit=limit,
	)

	# Get tasks
	tasks = frappe.get_all(
		"CRM Task",
		filters=filters,
		fields=["name", "title", "status", "owner", "creation", "reference_doctype", "reference_docname"],
		order_by="creation desc",
		limit=limit,
	)

	# Get notes
	notes = frappe.get_all(
		"FCRM Note",
		filters=filters,
		fields=["name", "title", "owner", "creation", "reference_doctype", "reference_docname"],
		order_by="creation desc",
		limit=limit,
	)

	# Combine and sort
	activities = []
	for c in comments:
		activities.append({
			"type": "comment",
			"id": c.name,
			"content": c.content,
			"owner": c.owner,
			"creation": c.creation,
			"reference_doctype": c.reference_doctype,
			"reference_docname": c.reference_docname,
		})

	for t in tasks:
		activities.append({
			"type": "task",
			"id": t.name,
			"title": t.title,
			"status": t.status,
			"owner": t.owner,
			"creation": t.creation,
			"reference_doctype": t.reference_doctype,
			"reference_docname": t.reference_docname,
		})

	for n in notes:
		activities.append({
			"type": "note",
			"id": n.name,
			"title": n.title,
			"owner": n.owner,
			"creation": n.creation,
			"reference_doctype": n.reference_doctype,
			"reference_docname": n.reference_docname,
		})

	# Sort by creation date
	activities.sort(key=lambda x: x["creation"], reverse=True)

	return activities[:limit]


@frappe.whitelist()
def create_workspace(name, description=None, members=None, is_private=False):
	"""
	Create a shared workspace
	"""
	# Validate inputs
	if not name:
		frappe.throw(_("Workspace name is required"))
	
	# Sanitize name and description
	import html
	name = html.escape(str(name))
	if description:
		description = html.escape(str(description))
	
	# Parse members if string
	if isinstance(members, str):
		try:
			members = json.loads(members) if members else []
		except json.JSONDecodeError:
			frappe.throw(_("Invalid members format"))
	
	# Validate members
	if members:
		if not isinstance(members, list):
			frappe.throw(_("Members must be a list"))
		
		# Validate each member exists
		for member in members:
			if not frappe.db.exists("User", member):
				frappe.throw(_("Invalid user: {0}").format(member))

	workspace = frappe.get_doc({
		"doctype": "CRM Workspace",
		"title": name,
		"description": description,
		"is_private": is_private,
		"owner": frappe.session.user,
	})
	workspace.insert()

	# Add members
	if members:
		for member in members:
			frappe.get_doc({
				"doctype": "CRM Workspace Member",
				"workspace": workspace.name,
				"user": member,
			}).insert()

	return workspace.name


@frappe.whitelist()
def get_workspaces():
	"""
	Get all workspaces accessible to current user
	"""
	# Get workspaces where user is owner or member
	workspaces = frappe.get_all(
		"CRM Workspace",
		filters={
			"owner": frappe.session.user,
		},
		fields=["name", "title", "description", "is_private", "owner"],
	)

	# Also get workspaces where user is a member
	member_workspaces = frappe.get_all(
		"CRM Workspace Member",
		filters={"user": frappe.session.user},
		fields=["workspace"],
		pluck="workspace",
	)

	for ws_name in member_workspaces:
		# Check if workspace exists and user has permission
		if not frappe.db.exists("CRM Workspace", ws_name):
			continue
		
		ws = frappe.get_doc("CRM Workspace", ws_name)
		
		# Check permissions
		if not frappe.has_permission("CRM Workspace", "read", ws):
			continue
		
		workspaces.append({
			"name": ws.name,
			"title": ws.title,
			"description": ws.description,
			"is_private": ws.is_private,
			"owner": ws.owner,
		})

	return workspaces


@frappe.whitelist()
def add_mention(doctype, docname, mentioned_user, comment_text):
	"""
	Add a mention to a comment
	"""
	# Validate inputs
	if not doctype:
		frappe.throw(_("Doctype is required"))
	
	if not docname:
		frappe.throw(_("Document name is required"))
	
	if not mentioned_user:
		frappe.throw(_("Mentioned user is required"))
	
	if not comment_text:
		frappe.throw(_("Comment text is required"))
	
	# Validate doctype exists
	if not frappe.db.exists("DocType", doctype):
		frappe.throw(_("Invalid doctype"))
	
	# Validate document exists
	if not frappe.db.exists(doctype, docname):
		frappe.throw(_("Document not found"))
	
	# Check permissions on the document
	if not frappe.has_permission(doctype, "read", docname):
		frappe.throw(_("Not permitted to comment on this document"), frappe.PermissionError)
	
	# Validate mentioned user exists
	if not frappe.db.exists("User", mentioned_user):
		frappe.throw(_("Invalid user"))
	
	# Sanitize comment text to prevent XSS
	import html
	comment_text = html.escape(str(comment_text))
	
	# Create comment with mention
	comment = frappe.get_doc({
		"doctype": "Comment",
		"comment_type": "Comment",
		"reference_doctype": doctype,
		"reference_docname": docname,
		"content": comment_text,
		"comment_by": frappe.session.user,
	})
	comment.insert()

	# Create notification for mentioned user
	frappe.get_doc({
		"doctype": "CRM Notification",
		"type": "Mention",
		"user": mentioned_user,
		"reference_doctype": doctype,
		"reference_docname": docname,
		"message": f"{frappe.session.user} mentioned you in a comment",
	}).insert()

	return comment.name


@frappe.whitelist()
def send_team_chat_message(reference_type, reference_name, message, mentioned_users=None):
	"""
	Send a team chat message
	"""
	import json
	
	if not message:
		frappe.throw(_("Message is required"))
	
	# Parse mentioned users if string
	if isinstance(mentioned_users, str):
		try:
			mentioned_users = json.loads(mentioned_users) if mentioned_users else []
		except json.JSONDecodeError:
			mentioned_users = []
	
	# Create chat message
	chat = frappe.get_doc({
		"doctype": "CRM Team Chat",
		"reference_type": reference_type,
		"reference_name": reference_name,
		"message": message,
		"sent_by": frappe.session.user,
		"sent_at": now(),
	})
	chat.insert()
	
	# Add mentions
	if mentioned_users:
		for user in mentioned_users:
			if frappe.db.exists("User", user):
				chat.append("mentioned_users", {
					"user": user,
					"mentioned_at": now()
				})
				# Create notification
				frappe.get_doc({
					"doctype": "CRM Notification",
					"type": "Mention",
					"user": user,
					"reference_doctype": reference_type,
					"reference_docname": reference_name,
					"message": f"{frappe.session.user} mentioned you in a team chat",
				}).insert()
	
	chat.save()
	frappe.db.commit()
	
	return chat.as_dict()


@frappe.whitelist()
def get_team_chat_messages(reference_type, reference_name, limit=50):
	"""
	Get team chat messages for a record
	"""
	messages = frappe.get_all(
		"CRM Team Chat",
		filters={
			"reference_type": reference_type,
			"reference_name": reference_name,
		},
		fields=["*"],
		order_by="sent_at desc",
		limit=limit,
	)
	
	# Get mentioned users for each message
	for msg in messages:
		msg["mentioned_users"] = frappe.get_all(
			"CRM Team Chat Mention",
			filters={"parent": msg.name},
			fields=["user", "mentioned_at"]
		)
	
	return list(reversed(messages))  # Return in chronological order


@frappe.whitelist()
def edit_team_chat_message(chat_name, new_message):
	"""
	Edit a team chat message
	"""
	if not new_message:
		frappe.throw(_("Message is required"))
	
	chat = frappe.get_doc("CRM Team Chat", chat_name)
	
	# Check permissions
	if chat.sent_by != frappe.session.user:
		frappe.throw(_("You can only edit your own messages"), frappe.PermissionError)
	
	chat.message = new_message
	chat.is_edited = True
	chat.edited_at = now()
	chat.save()
	frappe.db.commit()
	
	return chat.as_dict()

