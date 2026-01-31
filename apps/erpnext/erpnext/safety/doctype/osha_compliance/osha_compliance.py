# Copyright (c) 2024, Nexelya and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from erpnext.projects.api.feature_gating import check_feature_access


class OSHACompliance(Document):
	def validate(self):
		check_feature_access("safety_compliance", self.company, throw=True)
		self.calculate_rates()
	
	def calculate_rates(self):
		"""Calculate TRIR and DART rates"""
		if self.total_hours_worked and self.total_hours_worked > 0:
			# TRIR = (Number of recordable incidents × 200,000) / Total hours worked
			if self.total_recordable_incidents:
				self.trir = (self.total_recordable_incidents * 200000) / self.total_hours_worked
			
			# DART = ((Days Away + Restricted Days) × 200,000) / Total hours worked
			total_dart_days = (self.total_days_away or 0) + (self.total_restricted_days or 0)
			if total_dart_days:
				self.dart_rate = (total_dart_days * 200000) / self.total_hours_worked


def update_osha_compliance(company):
	"""Update OSHA compliance records when incidents are recorded"""
	# This would be called when a safety incident is submitted
	# Implementation would aggregate incident data for compliance reporting
	pass

