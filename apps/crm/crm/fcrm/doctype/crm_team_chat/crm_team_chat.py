# Copyright (c) 2024, Nexelya Technologies Pvt. Ltd. and Contributors
# GNU GPLv3 License. See license.txt

import frappe
from frappe.model.document import Document


class CRMTeamChat(Document):
	def before_insert(self):
		if not self.sent_by:
			self.sent_by = frappe.session.user
		if not self.sent_at:
			self.sent_at = frappe.utils.now()

	def on_update(self):
		if self.has_value_changed("message"):
			self.is_edited = True
			self.edited_at = frappe.utils.now()
