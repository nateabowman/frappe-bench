# Copyright (c) 2024, Nexelya Technologies Pvt. Ltd. and Contributors
# GNU GPLv3 License. See license.txt

import frappe
from frappe.model.document import Document


class CRMAIInsight(Document):
	def before_save(self):
		if not self.generated_at:
			self.generated_at = frappe.utils.now()
		if not self.generated_by:
			self.generated_by = frappe.session.user
