# Copyright (c) 2024, Nexelya and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from erpnext.projects.api.feature_gating import check_feature_access


class EquipmentTracking(Document):
	def validate(self):
		# Check feature access - get company from asset or project
		company = None
		if self.asset:
			company = frappe.db.get_value("Asset", self.asset, "company")
		
		if company:
			check_feature_access("equipment_fleet_advanced", company, throw=True)
		
		self.calculate_utilization()
	
	def calculate_utilization(self):
		"""Calculate equipment utilization rate"""
		# This would calculate based on actual usage vs available time
		# Placeholder implementation
		if not self.utilization_rate:
			self.utilization_rate = 0

