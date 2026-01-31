# Copyright (c) 2024, Nexelya Technologies Pvt. Ltd. and Contributors
# GNU GPLv3 License. See license.txt

import frappe
from frappe.model.document import Document


class CRMWorkflowTemplate(Document):
	def before_insert(self):
		if not self.created_by:
			self.created_by = frappe.session.user
