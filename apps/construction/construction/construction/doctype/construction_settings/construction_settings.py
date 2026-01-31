import frappe
from frappe.model.document import Document


class ConstructionSettings(Document):
	pass


def get_construction_settings():
	"""Get construction settings as dict"""
	return frappe.get_single("Construction Settings").as_dict()


@frappe.whitelist()
def get_default_values():
	"""Get default values for construction forms"""
	settings = get_construction_settings()
	return {
		"company": settings.get("default_company"),
		"cost_center": settings.get("default_cost_center"),
		"currency": settings.get("default_currency"),
		"retention_percent": settings.get("default_retention_percent"),
		"markup_percent": settings.get("default_markup_percent"),
		"overhead_percent": settings.get("default_overhead_percent"),
	}
