# Copyright (c) 2024, Nexelya and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt
from erpnext.projects.api.feature_gating import check_feature_access


class Retainage(Document):
	def validate(self):
		# Check feature access
		if self.project:
			project_doc = frappe.get_doc("Project", self.project)
			if project_doc.company:
				check_feature_access("financial_management_advanced", project_doc.company, throw=True)
		
		self.calculate_retainage_amount()
	
	def calculate_retainage_amount(self):
		"""Calculate retainage amount from invoice"""
		if self.invoice and self.retainage_percent:
			invoice_doc = frappe.get_doc("Sales Invoice", self.invoice)
			self.retainage_amount = (flt(invoice_doc.grand_total) * flt(self.retainage_percent)) / 100

