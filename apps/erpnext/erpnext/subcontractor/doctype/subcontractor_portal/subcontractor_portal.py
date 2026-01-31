# Copyright (c) 2024, Nexelya and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import random_string
from erpnext.projects.api.feature_gating import check_feature_access


class SubcontractorPortal(Document):
	def validate(self):
		# Check feature access
		if self.project:
			project_doc = frappe.get_doc("Project", self.project)
			if project_doc.company:
				check_feature_access("subcontractor_management", project_doc.company, throw=True)
		
		self.generate_access_code()
	
	def generate_access_code(self):
		"""Generate access code for portal if not set"""
		if self.portal_access_enabled and not self.access_code:
			self.access_code = random_string(12)

