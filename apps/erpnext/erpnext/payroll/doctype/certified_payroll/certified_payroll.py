# Copyright (c) 2024, Nexelya and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt
from erpnext.projects.api.feature_gating import check_feature_access


class CertifiedPayroll(Document):
	def validate(self):
		# Check feature access
		if self.project:
			project_doc = frappe.get_doc("Project", self.project)
			if project_doc.company:
				check_feature_access("payroll_hr_advanced", project_doc.company, throw=True)
		
		self.calculate_total_hours()
	
	def calculate_total_hours(self):
		"""Calculate total hours from timesheets for this pay period"""
		if self.project and self.pay_period_start and self.pay_period_end:
			timesheets = frappe.get_all(
				"Timesheet",
				filters={
					"project": self.project,
					"start_date": [">=", self.pay_period_start],
					"end_date": ["<=", self.pay_period_end],
					"docstatus": 1
				},
				fields=["sum(total_hours) as total_hours"]
			)
			
			if timesheets and timesheets[0].total_hours:
				self.total_hours = flt(timesheets[0].total_hours)

