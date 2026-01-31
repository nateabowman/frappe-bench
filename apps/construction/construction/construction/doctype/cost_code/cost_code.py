import frappe
from frappe import _
from frappe.utils.nestedset import NestedSet


class CostCode(NestedSet):
	nsm_parent_field = "parent_cost_code"
	
	def validate(self):
		self.validate_parent()
	
	def validate_parent(self):
		"""Validate parent cost code"""
		if self.parent_cost_code:
			parent = frappe.get_doc("Cost Code", self.parent_cost_code)
			if not parent.is_group:
				frappe.throw(_("Parent Cost Code must be a group"))

	def on_update(self):
		super().on_update()
	
	def on_trash(self):
		# Check if cost code is used in any budget lines
		if frappe.db.exists("Budget Line", {"cost_code": self.name}):
			frappe.throw(_("Cannot delete Cost Code that is used in Budget Lines"))
		super().on_trash()


@frappe.whitelist()
def get_cost_code_hierarchy():
	"""Get hierarchical cost code structure"""
	cost_codes = frappe.get_all(
		"Cost Code",
		fields=["name", "cost_code", "cost_code_name", "parent_cost_code", "is_group", "cost_type"],
		order_by="cost_code"
	)
	
	# Build tree structure
	code_map = {cc["name"]: cc for cc in cost_codes}
	tree = []
	
	for cc in cost_codes:
		if not cc["parent_cost_code"]:
			tree.append(build_tree_node(cc, code_map, cost_codes))
	
	return tree


def build_tree_node(node, code_map, all_codes):
	"""Build tree node with children"""
	children = [
		build_tree_node(cc, code_map, all_codes) 
		for cc in all_codes 
		if cc["parent_cost_code"] == node["name"]
	]
	return {
		"name": node["name"],
		"code": node["cost_code"],
		"label": f"{node['cost_code']} - {node['cost_code_name']}",
		"is_group": node["is_group"],
		"cost_type": node["cost_type"],
		"children": children if children else None
	}


@frappe.whitelist()
def get_child_cost_codes(parent=None):
	"""Get child cost codes for a parent"""
	filters = {"parent_cost_code": parent} if parent else {"parent_cost_code": ["is", "not set"]}
	
	return frappe.get_all(
		"Cost Code",
		filters=filters,
		fields=["name", "cost_code", "cost_code_name", "is_group", "cost_type"],
		order_by="cost_code"
	)


@frappe.whitelist()
def import_csi_masterformat():
	"""Import full CSI MasterFormat cost codes"""
	# This would import a comprehensive list of CSI codes
	# For now, create the main divisions
	divisions = [
		("00", "Procurement and Contracting Requirements", True),
		("01", "General Requirements", True),
		("02", "Existing Conditions", True),
		("03", "Concrete", True),
		("04", "Masonry", True),
		("05", "Metals", True),
		("06", "Wood, Plastics, and Composites", True),
		("07", "Thermal and Moisture Protection", True),
		("08", "Openings", True),
		("09", "Finishes", True),
		("10", "Specialties", True),
		("11", "Equipment", True),
		("12", "Furnishings", True),
		("13", "Special Construction", True),
		("14", "Conveying Equipment", True),
		("21", "Fire Suppression", True),
		("22", "Plumbing", True),
		("23", "Heating, Ventilating, and Air Conditioning (HVAC)", True),
		("25", "Integrated Automation", True),
		("26", "Electrical", True),
		("27", "Communications", True),
		("28", "Electronic Safety and Security", True),
		("31", "Earthwork", True),
		("32", "Exterior Improvements", True),
		("33", "Utilities", True),
		("34", "Transportation", True),
		("35", "Waterway and Marine Construction", True),
		("40", "Process Interconnections", True),
		("41", "Material Processing and Handling Equipment", True),
		("42", "Process Heating, Cooling, and Drying Equipment", True),
		("43", "Process Gas and Liquid Handling, Purification, and Storage Equipment", True),
		("44", "Pollution and Waste Control Equipment", True),
		("45", "Industry-Specific Manufacturing Equipment", True),
		("46", "Water and Wastewater Equipment", True),
		("48", "Electrical Power Generation", True),
	]
	
	created = 0
	for code, name, is_group in divisions:
		if not frappe.db.exists("Cost Code", code):
			doc = frappe.new_doc("Cost Code")
			doc.cost_code = code
			doc.cost_code_name = name
			doc.is_group = is_group
			doc.insert(ignore_permissions=True)
			created += 1
	
	frappe.db.commit()
	return {"created": created}
