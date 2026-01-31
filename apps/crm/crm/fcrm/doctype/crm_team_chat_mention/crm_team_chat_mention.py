# Copyright (c) 2024, Nexelya Technologies Pvt. Ltd. and Contributors
# GNU GPLv3 License. See license.txt

import frappe
from frappe.model.document import Document


class CRMTeamChatMention(Document):
	def before_insert(self):
		if not self.mentioned_at:
			self.mentioned_at = frappe.utils.now()
