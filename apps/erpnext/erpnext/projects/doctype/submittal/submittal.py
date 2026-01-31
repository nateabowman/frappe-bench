# Copyright (c) 2024, Nexelya and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from erpnext.projects.api.feature_gating import check_feature_access


class Submittal(Document):
	def validate(self):
		# Check feature access for Growth plan
		if self.project:
			project_doc = frappe.get_doc("Project", self.project)
			if project_doc.company:
				check_feature_access("submittal_tracking", project_doc.company, throw=True)
		
		self.set_submittal_number()
		self.validate_dates()
		self.update_status()

	def set_submittal_number(self):
		"""Set submittal number if not already set"""
		if not self.submittal_number:
			self.submittal_number = self.name

	def validate_dates(self):
		"""Validate that due date is after submitted date"""
		if self.due_date and self.submitted_date:
			if self.due_date < self.submitted_date:
				frappe.throw(_("Due Date cannot be before Submitted Date"))

	def update_status(self):
		"""Update status based on review"""
		if self.review_comments and self.reviewed_by:
			if self.status == "Pending":
				# Status should be set manually by reviewer
				pass

	def on_update(self):
		"""Update project when Submittal is updated"""
		if self.project:
			# Update project's last modified date or add notification
			pass

