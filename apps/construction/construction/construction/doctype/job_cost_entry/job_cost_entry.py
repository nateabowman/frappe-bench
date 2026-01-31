import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class JobCostEntry(Document):
	def validate(self):
		self.calculate_total_cost()
		self.set_budget_line()

	def calculate_total_cost(self):
		"""Calculate total cost from components or quantity"""
		component_total = (
			flt(self.labor_cost) + 
			flt(self.material_cost) + 
			flt(self.equipment_cost) + 
			flt(self.subcontract_cost) + 
			flt(self.other_cost)
		)
		
		quantity_total = flt(self.quantity) * flt(self.unit_cost) if self.quantity and self.unit_cost else 0
		
		# Use component total if specified, otherwise use quantity calculation
		self.total_cost = component_total if component_total > 0 else quantity_total

	def set_budget_line(self):
		"""Auto-link to budget line if not specified"""
		if not self.budget_line and self.job_site and self.cost_code:
			budget_line = frappe.db.get_value(
				"Budget Line",
				{"job_site": self.job_site, "cost_code": self.cost_code},
				"name"
			)
			if budget_line:
				self.budget_line = budget_line

	def on_submit(self):
		"""Update budget line actual costs"""
		self.update_budget_line_costs()

	def on_cancel(self):
		"""Update budget line actual costs on cancellation"""
		self.update_budget_line_costs()

	def update_budget_line_costs(self):
		"""Update the linked budget line's actual costs"""
		if self.budget_line:
			frappe.enqueue(
				"construction.construction.doctype.budget_line.budget_line.recalculate_budget_line",
				budget_line=self.budget_line,
				queue="short"
			)


def create_from_purchase_invoice(doc, method):
	"""Create job cost entries from purchase invoice"""
	settings = frappe.get_single("Construction Settings")
	if not settings.auto_create_cost_entries:
		return
	
	# Check if invoice is linked to a project
	if not doc.project:
		return
	
	# Get linked job site
	job_site = frappe.db.get_value("Job Site", {"project": doc.project}, "name")
	if not job_site:
		return
	
	for item in doc.items:
		# Skip if no cost code
		cost_code = item.get("cost_code")
		if not cost_code:
			continue
		
		# Create cost entry
		entry = frappe.new_doc("Job Cost Entry")
		entry.job_site = job_site
		entry.cost_code = cost_code
		entry.posting_date = doc.posting_date
		entry.description = f"PI: {doc.name} - {item.item_name}"
		entry.source_type = "Purchase Invoice"
		entry.source_doctype = "Purchase Invoice"
		entry.source_name = doc.name
		entry.supplier = doc.supplier
		entry.quantity = item.qty
		entry.unit_of_measure = item.uom
		entry.unit_cost = item.rate
		entry.material_cost = item.amount
		entry.total_cost = item.amount
		entry.insert()
		entry.submit()


def create_from_timesheet(doc, method):
	"""Create job cost entries from timesheet"""
	settings = frappe.get_single("Construction Settings")
	if not settings.auto_create_cost_entries:
		return
	
	for detail in doc.time_logs:
		# Skip if no project
		if not detail.project:
			continue
		
		# Get linked job site
		job_site = frappe.db.get_value("Job Site", {"project": detail.project}, "name")
		if not job_site:
			continue
		
		# Get cost code from activity type or default
		cost_code = frappe.db.get_value("Activity Type", detail.activity_type, "cost_code")
		if not cost_code:
			cost_code = "01"  # Default to General Requirements
		
		# Calculate labor cost
		hours = flt(detail.hours)
		billing_rate = flt(detail.billing_rate) or flt(detail.costing_rate)
		labor_cost = hours * billing_rate
		
		if labor_cost <= 0:
			continue
		
		# Create cost entry
		entry = frappe.new_doc("Job Cost Entry")
		entry.job_site = job_site
		entry.cost_code = cost_code
		entry.posting_date = detail.from_time.date() if detail.from_time else doc.start_date
		entry.description = f"Labor: {doc.employee_name} - {detail.activity_type}"
		entry.source_type = "Timesheet"
		entry.source_doctype = "Timesheet"
		entry.source_name = doc.name
		entry.employee = doc.employee
		entry.quantity = hours
		entry.unit_of_measure = "Hour"
		entry.unit_cost = billing_rate
		entry.labor_cost = labor_cost
		entry.total_cost = labor_cost
		entry.insert()
		entry.submit()


@frappe.whitelist()
def get_cost_summary_by_code(job_site):
	"""Get cost summary grouped by cost code"""
	return frappe.db.sql("""
		SELECT 
			cost_code,
			COUNT(*) as entry_count,
			SUM(labor_cost) as total_labor,
			SUM(material_cost) as total_material,
			SUM(equipment_cost) as total_equipment,
			SUM(subcontract_cost) as total_subcontract,
			SUM(other_cost) as total_other,
			SUM(total_cost) as total_cost
		FROM `tabJob Cost Entry`
		WHERE job_site = %s AND docstatus = 1
		GROUP BY cost_code
		ORDER BY cost_code
	""", job_site, as_dict=True)


@frappe.whitelist()
def get_cost_trend(job_site, days=30):
	"""Get cost trend over time"""
	return frappe.db.sql("""
		SELECT 
			posting_date,
			SUM(total_cost) as daily_cost,
			SUM(SUM(total_cost)) OVER (ORDER BY posting_date) as cumulative_cost
		FROM `tabJob Cost Entry`
		WHERE job_site = %s 
		AND docstatus = 1
		AND posting_date >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
		GROUP BY posting_date
		ORDER BY posting_date
	""", (job_site, days), as_dict=True)
