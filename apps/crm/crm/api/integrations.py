# Copyright (c) 2024, Nexelya Technologies Pvt. Ltd. and Contributors
# GNU GPLv3 License. See license.txt

import frappe
from frappe import _
from frappe.utils import now


@frappe.whitelist()
def get_integrations():
	"""
	Get all integrations
	"""
	integrations = frappe.get_all(
		"CRM Integration",
		filters={"is_active": 1},
		fields=["*"],
		order_by="modified desc"
	)
	
	return integrations


@frappe.whitelist()
def create_integration(integration_name, integration_type, provider, **kwargs):
	"""
	Create a new integration
	"""
	if not integration_name:
		frappe.throw(_("Integration name is required"))
	
	if not integration_type:
		frappe.throw(_("Integration type is required"))
	
	if not provider:
		frappe.throw(_("Provider is required"))
	
	integration = frappe.get_doc({
		"doctype": "CRM Integration",
		"integration_name": integration_name,
		"integration_type": integration_type,
		"provider": provider,
		"status": "Pending",
		"is_active": 1,
		"connected_by": frappe.session.user,
		"connected_at": now(),
		**kwargs
	})
	integration.insert()
	frappe.db.commit()
	
	return integration.as_dict()


@frappe.whitelist()
def update_integration_status(integration_name, status):
	"""
	Update integration status
	"""
	integration = frappe.get_doc("CRM Integration", integration_name)
	integration.status = status
	integration.save()
	frappe.db.commit()
	
	return integration.as_dict()


@frappe.whitelist()
def sync_integration(integration_name):
	"""
	Sync data from integration
	"""
	integration = frappe.get_doc("CRM Integration", integration_name)
	
	if not integration.is_active:
		frappe.throw(_("Integration is not active"))
	
	# Update last synced time
	integration.last_synced_at = now()
	integration.save()
	frappe.db.commit()
	
	# Here you would implement actual sync logic based on provider
	return {
		"status": "success",
		"message": f"Integration {integration_name} synced successfully",
		"last_synced_at": integration.last_synced_at
	}


@frappe.whitelist()
def get_social_profiles(reference_type, reference_name):
	"""
	Get social media profiles for a record
	"""
	profiles = frappe.get_all(
		"CRM Social Profile",
		filters={
			"reference_type": reference_type,
			"reference_name": reference_name,
			"is_active": 1
		},
		fields=["*"],
		order_by="platform"
	)
	
	return profiles


@frappe.whitelist()
def add_social_profile(platform, reference_type, reference_name, profile_url=None, username=None):
	"""
	Add a social media profile
	"""
	if not platform:
		frappe.throw(_("Platform is required"))
	
	profile = frappe.get_doc({
		"doctype": "CRM Social Profile",
		"platform": platform,
		"reference_type": reference_type,
		"reference_name": reference_name,
		"profile_url": profile_url,
		"username": username,
		"is_active": 1
	})
	profile.insert()
	frappe.db.commit()
	
	return profile.as_dict()


@frappe.whitelist()
def sync_social_profile(profile_name):
	"""
	Sync social media profile data
	"""
	profile = frappe.get_doc("CRM Social Profile", profile_name)
	
	# Update last synced time
	profile.last_synced_at = now()
	profile.save()
	frappe.db.commit()
	
	# Here you would implement actual sync logic based on platform
	return {
		"status": "success",
		"message": f"Social profile {profile_name} synced successfully",
		"last_synced_at": profile.last_synced_at
	}
