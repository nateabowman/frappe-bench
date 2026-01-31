# Copyright (c) 2024, Nexelya and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt
from erpnext.projects.api.feature_gating import check_feature_access


class WIPReport(Document):
	def validate(self):
		# Check feature access
		if self.project:
			project_doc = frappe.get_doc("Project", self.project)
			if project_doc.company:
				check_feature_access("financial_management_advanced", project_doc.company, throw=True)
		
		self.calculate_wip()
	
	def calculate_wip(self):
		"""Calculate Work in Progress values"""
		if not self.project:
			return
		
		project_doc = frappe.get_doc("Project", self.project)
		project_doc.update_costing()
		
		# Get costs and billing
		self.total_costs_incurred = (
			flt(project_doc.total_actual_cost) or 
			flt(project_doc.total_committed_cost) or 0
		)
		self.total_billed = flt(project_doc.total_billed_amount) or 0
		self.costs_incurred = self.total_costs_incurred
		
		# Calculate percent complete
		if self.total_contract_value:
			self.percent_complete = (self.total_costs_incurred / self.total_contract_value) * 100
		else:
			self.percent_complete = project_doc.percent_complete or 0
		
		# Calculate revenue recognized (percentage of completion method)
		if self.total_contract_value:
			self.revenue_recognized = (self.percent_complete / 100) * self.total_contract_value
		else:
			self.revenue_recognized = 0
		
		# Calculate WIP Asset (unbilled revenue)
		self.unbilled_revenue = self.revenue_recognized - self.total_billed
		
		# Calculate WIP Liability (over billings)
		if self.total_billed > self.revenue_recognized:
			self.over_billings = self.total_billed - self.revenue_recognized
		else:
			self.over_billings = 0

