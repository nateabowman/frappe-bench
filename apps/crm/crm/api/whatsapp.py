import json

import frappe
from frappe import _

from crm.api.doc import get_assigned_users
from crm.fcrm.doctype.crm_notification.crm_notification import notify_user


def validate(doc, method):
	if doc.type == "Incoming" and doc.get("from"):
		name, doctype = get_lead_or_deal_from_number(doc.get("from"))
		doc.reference_doctype = doctype
		doc.reference_name = name


def on_update(doc, method):
	frappe.publish_realtime(
		"whatsapp_message",
		{
			"reference_doctype": doc.reference_doctype,
			"reference_name": doc.reference_name,
		},
	)

	notify_agent(doc)


def notify_agent(doc):
	if doc.type == "Incoming":
		doctype = doc.reference_doctype
		if doctype.startswith("CRM "):
			doctype = doctype[4:].lower()
		notification_text = f"""
            <div class="mb-2 leading-5 text-ink-gray-5">
                <span class="font-medium text-ink-gray-9">{ _('You') }</span>
                <span>{ _('received a whatsapp message in {0}').format(doctype) }</span>
                <span class="font-medium text-ink-gray-9">{ doc.reference_name }</span>
            </div>
        """
		assigned_users = get_assigned_users(doc.reference_doctype, doc.reference_name)
		for user in assigned_users:
			notify_user(
				{
					"owner": doc.owner,
					"assigned_to": user,
					"notification_type": "WhatsApp",
					"message": doc.message,
					"notification_text": notification_text,
					"reference_doctype": "WhatsApp Message",
					"reference_docname": doc.name,
					"redirect_to_doctype": doc.reference_doctype,
					"redirect_to_docname": doc.reference_name,
				}
			)


def get_lead_or_deal_from_number(number):
	"""Get lead/deal from the given number."""

	def find_record(doctype, mobile_no, where_clause=""):
		# Validate doctype to prevent SQL injection
		allowed_doctypes = ["CRM Deal", "CRM Lead"]
		if doctype not in allowed_doctypes:
			return None
		
		# Parse and validate mobile number
		mobile_no = parse_mobile_no(mobile_no)
		if not mobile_no or not mobile_no.replace("+", "").isdigit():
			return None

		# Use parameterized query to prevent SQL injection
		query = """
            SELECT name, mobile_no
            FROM `tab{doctype}`
            WHERE CONCAT('+', REGEXP_REPLACE(mobile_no, '[^0-9]', '')) = %s
        """.format(doctype=frappe.db.escape(doctype))
		
		# Safely add where clause if provided
		if where_clause:
			# Only allow specific safe where clauses
			if where_clause.strip() == "AND converted is not True":
				query += " " + where_clause
			else:
				# Invalid where clause, ignore it
				pass

		data = frappe.db.sql(query, (mobile_no,), as_dict=True)
		return data[0].name if data else None

	doctype = "CRM Deal"

	doc = find_record(doctype, number) or None
	if not doc:
		doctype = "CRM Lead"
		doc = find_record(doctype, number, "AND converted is not True")
		if not doc:
			doc = find_record(doctype, number)

	return doc, doctype


def parse_mobile_no(mobile_no: str):
	"""Parse mobile number to remove spaces, brackets, etc.
	>>> parse_mobile_no("+91 (766) 667 6666")
	... "+917666676666"
	"""
	return "".join([c for c in mobile_no if c.isdigit() or c == "+"])


@frappe.whitelist()
def is_whatsapp_enabled():
	if not frappe.db.exists("DocType", "WhatsApp Settings"):
		return False
	return frappe.get_cached_value("WhatsApp Settings", "WhatsApp Settings", "enabled")


@frappe.whitelist()
def is_whatsapp_installed():
	if not frappe.db.exists("DocType", "WhatsApp Settings"):
		return False
	return True


@frappe.whitelist()
def get_whatsapp_messages(reference_doctype, reference_name):
	# Validate inputs
	if not reference_doctype or not reference_name:
		frappe.throw(_("Reference doctype and name are required"))
	
	# Validate doctype
	allowed_doctypes = ["CRM Deal", "CRM Lead", "CRM Contact", "CRM Organization"]
	if reference_doctype not in allowed_doctypes:
		frappe.throw(_("Invalid reference doctype"))
	
	# Check permissions
	if not frappe.has_permission(reference_doctype, "read", reference_name):
		frappe.throw(_("Not permitted to access this document"), frappe.PermissionError)
	
	# twilio integration app is not compatible with crm app
	# crm has its own twilio integration in built
	if "twilio_integration" in frappe.get_installed_apps():
		return []
	if not frappe.db.exists("DocType", "WhatsApp Message"):
		return []
	messages = []

	if reference_doctype == "CRM Deal":
		lead = frappe.db.get_value(reference_doctype, reference_name, "lead")
		if lead:
			messages = frappe.get_all(
				"WhatsApp Message",
				filters={
					"reference_doctype": "CRM Lead",
					"reference_name": lead,
				},
				fields=[
					"name",
					"type",
					"to",
					"from",
					"content_type",
					"message_type",
					"attach",
					"template",
					"use_template",
					"message_id",
					"is_reply",
					"reply_to_message_id",
					"creation",
					"message",
					"status",
					"reference_doctype",
					"reference_name",
					"template_parameters",
					"template_header_parameters",
				],
			)

	messages += frappe.get_all(
		"WhatsApp Message",
		filters={
			"reference_doctype": reference_doctype,
			"reference_name": reference_name,
		},
		fields=[
			"name",
			"type",
			"to",
			"from",
			"content_type",
			"message_type",
			"attach",
			"template",
			"use_template",
			"message_id",
			"is_reply",
			"reply_to_message_id",
			"creation",
			"message",
			"status",
			"reference_doctype",
			"reference_name",
			"template_parameters",
			"template_header_parameters",
		],
	)

	# Filter messages to get only Template messages
	template_messages = [message for message in messages if message["message_type"] == "Template"]

	# Iterate through template messages
	for template_message in template_messages:
		# Find the template that this message is using
		template = frappe.get_doc("WhatsApp Templates", template_message["template"])

		# If the template is found, add the template details to the template message
		if template:
			template_message["template_name"] = template.template_name
			if template_message["template_parameters"]:
				parameters = json.loads(template_message["template_parameters"])
				template.template = parse_template_parameters(template.template, parameters)

			template_message["template"] = template.template
			if template_message["template_header_parameters"]:
				header_parameters = json.loads(template_message["template_header_parameters"])
				template.header = parse_template_parameters(template.header, header_parameters)
			template_message["header"] = template.header
			template_message["footer"] = template.footer

	# Filter messages to get only reaction messages
	reaction_messages = [message for message in messages if message["content_type"] == "reaction"]

	# Iterate through reaction messages
	for reaction_message in reaction_messages:
		# Find the message that this reaction is reacting to
		reacted_message = next(
			(m for m in messages if m["message_id"] == reaction_message["reply_to_message_id"]),
			None,
		)

		# If the reacted message is found, add the reaction to it
		if reacted_message:
			reacted_message["reaction"] = reaction_message["message"]

	for message in messages:
		from_name = get_from_name(message) if message["from"] else _("You")
		message["from_name"] = from_name
	# Filter messages to get only replies
	reply_messages = [message for message in messages if message["is_reply"]]

	# Iterate through reply messages
	for reply_message in reply_messages:
		# Find the message that this message is replying to
		replied_message = next(
			(m for m in messages if m["message_id"] == reply_message["reply_to_message_id"]),
			None,
		)

		# If the replied message is found, add the reply details to the reply message
		from_name = get_from_name(reply_message) if replied_message["from"] else _("You")
		if replied_message:
			message = replied_message["message"]
			if replied_message["message_type"] == "Template":
				message = replied_message["template"]
			reply_message["reply_message"] = message
			reply_message["header"] = replied_message.get("header") or ""
			reply_message["footer"] = replied_message.get("footer") or ""
			reply_message["reply_to"] = replied_message["name"]
			reply_message["reply_to_type"] = replied_message["type"]
			reply_message["reply_to_from"] = from_name

	return [message for message in messages if message["content_type"] != "reaction"]


@frappe.whitelist()
def create_whatsapp_message(
	reference_doctype,
	reference_name,
	message,
	to,
	attach,
	reply_to,
	content_type="text",
):
	# Validate inputs
	if not reference_doctype or not reference_name:
		frappe.throw(_("Reference doctype and name are required"))
	
	# Validate doctype
	allowed_doctypes = ["CRM Deal", "CRM Lead", "CRM Contact", "CRM Organization"]
	if reference_doctype not in allowed_doctypes:
		frappe.throw(_("Invalid reference doctype"))
	
	# Check permissions
	if not frappe.has_permission(reference_doctype, "write", reference_name):
		frappe.throw(_("Not permitted to create messages for this document"), frappe.PermissionError)
	
	# Validate content_type
	allowed_content_types = ["text", "image", "video", "audio", "document", "location", "reaction"]
	if content_type not in allowed_content_types:
		frappe.throw(_("Invalid content type"))
	
	doc = frappe.new_doc("WhatsApp Message")

	if reply_to:
		# Validate reply_to exists and user has permission
		if not frappe.db.exists("WhatsApp Message", reply_to):
			frappe.throw(_("Reply message not found"))
		reply_doc = frappe.get_doc("WhatsApp Message", reply_to)
		doc.update(
			{
				"is_reply": True,
				"reply_to_message_id": reply_doc.message_id,
			}
		)

	doc.update(
		{
			"reference_doctype": reference_doctype,
			"reference_name": reference_name,
			"message": message or attach,
			"to": to,
			"attach": attach,
			"content_type": content_type,
		}
	)
	doc.insert()
	return doc.name


@frappe.whitelist()
def send_whatsapp_template(reference_doctype, reference_name, template, to):
	# Validate inputs
	if not reference_doctype or not reference_name:
		frappe.throw(_("Reference doctype and name are required"))
	
	# Validate doctype
	allowed_doctypes = ["CRM Deal", "CRM Lead", "CRM Contact", "CRM Organization"]
	if reference_doctype not in allowed_doctypes:
		frappe.throw(_("Invalid reference doctype"))
	
	# Check permissions
	if not frappe.has_permission(reference_doctype, "write", reference_name):
		frappe.throw(_("Not permitted to send templates for this document"), frappe.PermissionError)
	
	# Validate template exists
	if not frappe.db.exists("WhatsApp Templates", template):
		frappe.throw(_("Template not found"))
	
	doc = frappe.new_doc("WhatsApp Message")
	doc.update(
		{
			"reference_doctype": reference_doctype,
			"reference_name": reference_name,
			"message_type": "Template",
			"message": "Template message",
			"content_type": "text",
			"use_template": True,
			"template": template,
			"to": to,
		}
	)
	doc.insert()
	return doc.name


@frappe.whitelist()
def react_on_whatsapp_message(emoji, reply_to_name):
	# Validate inputs
	if not reply_to_name:
		frappe.throw(_("Reply message name is required"))
	
	if not frappe.db.exists("WhatsApp Message", reply_to_name):
		frappe.throw(_("Message not found"))
	
	reply_to_doc = frappe.get_doc("WhatsApp Message", reply_to_name)
	
	# Check permissions on reference document
	if reply_to_doc.reference_doctype and reply_to_doc.reference_name:
		if not frappe.has_permission(reply_to_doc.reference_doctype, "write", reply_to_doc.reference_name):
			frappe.throw(_("Not permitted to react to this message"), frappe.PermissionError)
	
	# Validate emoji (basic validation - should be a single emoji or short string)
	if not emoji or len(emoji) > 10:
		frappe.throw(_("Invalid emoji"))
	
	to = reply_to_doc.type == "Incoming" and reply_to_doc.get("from") or reply_to_doc.to
	doc = frappe.new_doc("WhatsApp Message")
	doc.update(
		{
			"reference_doctype": reply_to_doc.reference_doctype,
			"reference_name": reply_to_doc.reference_name,
			"message": emoji,
			"to": to,
			"reply_to_message_id": reply_to_doc.message_id,
			"content_type": "reaction",
		}
	)
	doc.insert()
	return doc.name


def parse_template_parameters(string, parameters):
	for i, parameter in enumerate(parameters, start=1):
		placeholder = "{{" + str(i) + "}}"
		string = string.replace(placeholder, parameter)

	return string


def get_from_name(message):
	# Validate inputs
	if not message.get("reference_doctype") or not message.get("reference_name"):
		return ""
	
	# Check permissions before accessing document
	if not frappe.has_permission(message["reference_doctype"], "read", message["reference_name"]):
		return ""
	
	try:
		doc = frappe.get_doc(message["reference_doctype"], message["reference_name"])
		from_name = ""
		if message["reference_doctype"] == "CRM Deal":
			if doc.get("contacts"):
				for c in doc.get("contacts"):
					if c.is_primary:
						from_name = c.full_name or c.mobile_no
						break
			else:
				from_name = doc.get("lead_name")
		else:
			from_name = " ".join(filter(None, [doc.get("first_name"), doc.get("last_name")]))
		return from_name
	except frappe.DoesNotExistError:
		return ""
	except Exception:
		return ""
