# Copyright (c) 2024, Nexelya and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import now_datetime
from erpnext.projects.api.feature_gating import check_feature_access


class DailyLog(Document):
	def validate(self):
		# Check feature access for Growth plan
		if self.project:
			project_doc = frappe.get_doc("Project", self.project)
			if project_doc.company:
				check_feature_access("daily_logs", project_doc.company, throw=True)
		
		self.set_submitted_by()
		self.set_submitted_date()

	def set_submitted_by(self):
		"""Set submitted_by to current user if not set"""
		if not self.submitted_by:
			self.submitted_by = frappe.session.user

	def set_submitted_date(self):
		"""Set submitted_date to current datetime"""
		if not self.submitted_date:
			self.submitted_date = now_datetime()

	def on_update(self):
		"""Update project when Daily Log is updated"""
		if self.project:
			# Update project's last modified date or add notification
			pass

