# Copyright (c) 2024, Nexelya and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import add_days, getdate
from erpnext.projects.api.feature_gating import check_feature_access


class ProjectSchedule(Document):
	def validate(self):
		# Check feature access
		if self.project:
			project_doc = frappe.get_doc("Project", self.project)
			if project_doc.company:
				check_feature_access("advanced_scheduling", project_doc.company, throw=True)
		
		self.validate_dates()
		self.calculate_end_dates()
	
	def validate_dates(self):
		"""Validate schedule dates"""
		if self.start_date and self.end_date:
			if getdate(self.end_date) < getdate(self.start_date):
				frappe.throw(_("End Date cannot be before Start Date"))
	
	def calculate_end_dates(self):
		"""Calculate end dates for tasks based on duration"""
		for task in self.schedule_tasks:
			if task.start_date and task.duration:
				task.end_date = add_days(getdate(task.start_date), task.duration - 1)

