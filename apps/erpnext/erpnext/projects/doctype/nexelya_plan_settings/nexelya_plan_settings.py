# Copyright (c) 2024, Nexelya and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class NexelyaPlanSettings(Document):
	def validate(self):
		self.set_max_users_by_plan()
		self.update_current_users()

	def set_max_users_by_plan(self):
		"""Set max users based on plan type"""
		if self.plan_type == "Core":
			self.max_users = 10
		elif self.plan_type == "Growth":
			self.max_users = 50
		elif self.plan_type == "Enterprise":
			self.max_users = 999999  # Unlimited

	def update_current_users(self):
		"""Update current user count"""
		if self.company:
			user_count = frappe.db.count("User", {"company": self.company, "enabled": 1})
			self.current_users = user_count

	def is_feature_enabled(self, feature_name):
		"""Check if a feature is enabled for this plan"""
		if self.plan_type == "Enterprise":
			return True  # Enterprise has all features
		
		# Check if feature is in enabled_features table
		for feature in self.enabled_features:
			if feature.feature_name == feature_name and feature.enabled:
				return True
		
		# Check plan-based defaults
		if self.plan_type == "Growth":
			growth_features = [
				"real_time_job_costing",
				"crm_to_project_integration",
				"mobile_timecards",
				"rfi_management",
				"submittal_tracking",
				"daily_logs",
				"real_time_dashboards",
				"approval_chains",
				"job_templates"
			]
			return feature_name in growth_features
		
		# Premium addons are available as add-ons for Core/Growth or included in Enterprise
		premium_addons = [
			"advanced_mobile_app",
			"advanced_analytics_bi",
			"advanced_scheduling",
			"safety_compliance",
			"equipment_fleet_advanced",
			"advanced_estimating_takeoff",
			"financial_management_advanced",
			"payroll_hr_advanced",
			"ai_powered_features",
			"integration_hub",
			"subcontractor_management",
			"quality_control_inspections"
		]
		
		# Premium addons can be enabled via enabled_features table for Core/Growth
		# Enterprise has all features by default
		if self.plan_type == "Enterprise":
			return feature_name in premium_addons or True  # Enterprise has everything
		
		return False


@frappe.whitelist()
def get_plan_settings(company=None):
	"""Get plan settings for a company"""
	if not company:
		company = frappe.defaults.get_user_default("company")
	
	if not company:
		return None
	
	# Check if plan settings exist for this company
	plan_settings_name = frappe.db.get_value("Nexelya Plan Settings", {"company": company}, "name")
	
	if plan_settings_name:
		try:
			plan_settings = frappe.get_doc("Nexelya Plan Settings", plan_settings_name)
			return plan_settings
		except frappe.DoesNotExistError:
			return None
	
	return None


@frappe.whitelist()
def check_feature_access(feature_name, company=None):
	"""Check if a feature is accessible for the current plan"""
	plan_settings = get_plan_settings(company)
	if not plan_settings:
		return False
	
	return plan_settings.is_feature_enabled(feature_name)

