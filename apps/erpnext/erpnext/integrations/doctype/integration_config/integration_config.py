# Copyright (c) 2024, Nexelya and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from erpnext.projects.api.feature_gating import check_feature_access


class IntegrationConfig(Document):
	def validate(self):
		# Check feature access - get company from any linked project or use default
		company = frappe.defaults.get_user_default("company")
		if company:
			check_feature_access("integration_hub", company, throw=True)
		
		self.validate_credentials()
	
	def validate_credentials(self):
		"""Validate integration credentials"""
		if self.integration_type in ["QuickBooks", "Procore", "PlanGrid", "Sage"]:
			if not self.api_key:
				frappe.throw(_("API Key is required for {0} integration").format(self.integration_type))
		
		if self.integration_type in ["Custom API", "Webhook"]:
			if not self.webhook_url:
				frappe.throw(_("Webhook URL is required for {0} integration").format(self.integration_type))

