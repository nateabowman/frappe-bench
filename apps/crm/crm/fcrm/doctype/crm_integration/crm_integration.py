# Copyright (c) 2024, Nexelya Technologies Pvt. Ltd. and Contributors
# GNU GPLv3 License. See license.txt

import frappe
from frappe.model.document import Document


class CRMIntegration(Document):
	def before_insert(self):
		if not self.connected_by:
			self.connected_by = frappe.session.user
		if not self.connected_at:
			self.connected_at = frappe.utils.now()

	def validate(self):
		if self.status == "Connected" and not self.is_active:
			frappe.msgprint("Integration is connected but not active. Please activate it.", alert=True)
