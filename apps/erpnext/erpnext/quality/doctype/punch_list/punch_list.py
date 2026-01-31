# Copyright (c) 2024, Nexelya and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from erpnext.projects.api.feature_gating import check_feature_access


class PunchList(Document):
	def validate(self):
		# Check feature access
		if self.project:
			project_doc = frappe.get_doc("Project", self.project)
			if project_doc.company:
				check_feature_access("quality_control_inspections", project_doc.company, throw=True)
		
		self.update_status()
	
	def update_status(self):
		"""Update status based on punch list items"""
		if self.punch_list_items:
			completed_items = [item for item in self.punch_list_items if item.status == "Completed"]
			if len(completed_items) == len(self.punch_list_items):
				self.status = "Completed"
			elif len(completed_items) > 0:
				self.status = "In Progress"
			else:
				self.status = "Open"

