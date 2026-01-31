# Copyright (c) 2024, Nexelya and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from erpnext.projects.api.feature_gating import check_feature_access


class RFI(Document):
	def validate(self):
		# Check feature access for Growth plan
		if self.project:
			project_doc = frappe.get_doc("Project", self.project)
			if project_doc.company:
				check_feature_access("rfi_management", project_doc.company, throw=True)
		
		self.set_rfi_number()
		self.validate_dates()
		self.update_status()

	def set_rfi_number(self):
		"""Set RFI number if not already set"""
		if not self.rfi_number:
			self.rfi_number = self.name

	def validate_dates(self):
		"""Validate that due date is after requested date"""
		if self.due_date and self.requested_date:
			if self.due_date < self.requested_date:
				frappe.throw(_("Due Date cannot be before Requested Date"))

	def update_status(self):
		"""Update status based on response"""
		if self.response and self.responded_by and not self.status == "Closed":
			if self.status == "Open":
				self.status = "Answered"
		elif not self.response and self.status == "Answered":
			self.status = "Open"

	def on_update(self):
		"""Update project when RFI is updated"""
		if self.project:
			# Update project's last modified date or add notification
			pass

