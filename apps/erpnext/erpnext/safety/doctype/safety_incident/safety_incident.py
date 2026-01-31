# Copyright (c) 2024, Nexelya and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import now_datetime
from erpnext.projects.api.feature_gating import check_feature_access


class SafetyIncident(Document):
	def validate(self):
		# Check feature access
		if self.project:
			project_doc = frappe.get_doc("Project", self.project)
			if project_doc.company:
				check_feature_access("safety_compliance", project_doc.company, throw=True)
		
		self.set_incident_number()
		self.calculate_osha_metrics()
	
	def set_incident_number(self):
		"""Set incident number if not already set"""
		if not self.incident_number:
			self.incident_number = self.name
	
	def calculate_osha_metrics(self):
		"""Calculate OSHA metrics"""
		if self.osha_recordable:
			# Calculate days away and restricted work
			if self.injured_personnel:
				total_days_away = sum([p.days_away_from_work or 0 for p in self.injured_personnel])
				total_restricted = sum([p.restricted_work_days or 0 for p in self.injured_personnel])
				self.days_away_from_work = total_days_away
				self.restricted_work_days = total_restricted
	
	def on_submit(self):
		"""Update OSHA compliance records when incident is submitted"""
		if self.osha_recordable and self.project:
			project_doc = frappe.get_doc("Project", self.project)
			if project_doc.company:
				update_osha_compliance(project_doc.company)

