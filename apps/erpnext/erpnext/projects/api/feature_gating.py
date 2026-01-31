# Copyright (c) 2024, Nexelya and Contributors
# License: GNU General Public License v3. See license.txt

"""
Feature gating utilities for Nexelya plans
"""

import frappe
from frappe import _


def check_feature_access(feature_name, company=None, throw=False):
	"""
	Check if a feature is accessible for the current plan
	
	Args:
		feature_name: Name of the feature to check
		company: Company name (defaults to user's default company)
		throw: If True, throw an error if feature is not accessible
	
	Returns:
		bool: True if feature is accessible, False otherwise
	"""
	if not company:
		company = frappe.defaults.get_user_default("company")
	
	if not company:
		if throw:
			frappe.throw(_("Please set a default company"))
		return False
	
	try:
		plan_settings = frappe.get_doc("Nexelya Plan Settings", {"company": company})
		has_access = plan_settings.is_feature_enabled(feature_name)
		
		if not has_access and throw:
			frappe.throw(
				_("This feature is only available in Growth or Enterprise plans. Please upgrade your plan."),
				title=_("Feature Not Available")
			)
		
		return has_access
	except frappe.DoesNotExistError:
		# No plan settings found, assume Core plan (most restrictive)
		if throw:
			frappe.throw(
				_("This feature is only available in Growth or Enterprise plans. Please upgrade your plan."),
				title=_("Feature Not Available")
			)
		return False


def require_feature(feature_name, company=None):
	"""
	Decorator to require a feature for a function
	
	Usage:
		@require_feature("real_time_job_costing")
		def my_function():
			pass
	"""
	def decorator(func):
		def wrapper(*args, **kwargs):
			check_feature_access(feature_name, company, throw=True)
			return func(*args, **kwargs)
		return wrapper
	return decorator

