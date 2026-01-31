import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class BudgetLine(Document):
	def validate(self):
		self.calculate_budget()
		self.calculate_costs()
		self.calculate_variance()
		self.calculate_earned_value()

	def calculate_budget(self):
		"""Calculate current budget"""
		self.current_budget = flt(self.original_budget) + flt(self.approved_changes)

	def calculate_costs(self):
		"""Calculate total costs"""
		self.total_cost = flt(self.actual_cost) + flt(self.committed_cost)
		
		# Calculate Estimate at Completion
		self.estimate_at_completion = flt(self.actual_cost) + flt(self.estimate_to_complete)

	def calculate_variance(self):
		"""Calculate budget variance"""
		self.variance = flt(self.current_budget) - flt(self.estimate_at_completion)
		
		if self.current_budget:
			self.variance_percent = (self.variance / self.current_budget) * 100
		else:
			self.variance_percent = 0

	def calculate_earned_value(self):
		"""Calculate earned value (BCWP)"""
		self.earned_value = flt(self.current_budget) * (flt(self.percent_complete) / 100)

	def on_update(self):
		"""Update job site totals"""
		self.update_job_site_budget()

	def on_trash(self):
		"""Update job site totals after deletion"""
		frappe.enqueue(
			"construction.construction.doctype.budget_line.budget_line.update_job_site_from_budget_lines",
			job_site=self.job_site,
			queue="short"
		)

	def update_job_site_budget(self):
		"""Update job site budget totals"""
		update_job_site_from_budget_lines(self.job_site)


def update_job_site_from_budget_lines(job_site):
	"""Aggregate budget lines to update job site"""
	totals = frappe.db.sql("""
		SELECT 
			COALESCE(SUM(original_budget), 0) as original_budget,
			COALESCE(SUM(approved_changes), 0) as approved_changes,
			COALESCE(SUM(actual_cost), 0) as actual_cost,
			COALESCE(SUM(committed_cost), 0) as committed_cost,
			COALESCE(SUM(estimate_at_completion), 0) as projected_cost
		FROM `tabBudget Line`
		WHERE job_site = %s
	""", job_site, as_dict=True)[0]
	
	frappe.db.set_value("Job Site", job_site, {
		"original_budget": totals.original_budget,
		"approved_changes": totals.approved_changes,
		"actual_cost": totals.actual_cost,
		"committed_cost": totals.committed_cost,
		"projected_cost": totals.projected_cost,
	})


@frappe.whitelist()
def get_budget_by_code(job_site, cost_code):
	"""Get budget information for a specific cost code"""
	budget = frappe.db.get_value(
		"Budget Line",
		{"job_site": job_site, "cost_code": cost_code},
		["name", "current_budget", "actual_cost", "committed_cost", "variance", "percent_complete"],
		as_dict=True
	)
	return budget


@frappe.whitelist()
def create_budget_from_estimate(job_site, estimate):
	"""Create budget lines from an estimate"""
	# Get estimate items
	estimate_doc = frappe.get_doc("Estimate Template", estimate)
	
	created = 0
	for item in estimate_doc.items:
		if not frappe.db.exists("Budget Line", {"job_site": job_site, "cost_code": item.cost_code}):
			doc = frappe.new_doc("Budget Line")
			doc.job_site = job_site
			doc.cost_code = item.cost_code
			doc.description = item.description
			doc.original_budget = item.total_amount
			doc.quantity = item.quantity
			doc.unit_of_measure = item.uom
			doc.unit_cost = item.unit_cost
			doc.insert()
			created += 1
	
	return {"created": created}


@frappe.whitelist()
def recalculate_budget_line(budget_line):
	"""Recalculate a budget line's actual costs from job cost entries"""
	# Sum actual costs
	actual = frappe.db.sql("""
		SELECT COALESCE(SUM(total_cost), 0) as total
		FROM `tabJob Cost Entry`
		WHERE budget_line = %s AND docstatus = 1
	""", budget_line, as_dict=True)[0].total
	
	# Sum committed from POs
	bl = frappe.get_doc("Budget Line", budget_line)
	committed = frappe.db.sql("""
		SELECT COALESCE(SUM(poi.base_net_amount), 0) as total
		FROM `tabPurchase Order Item` poi
		JOIN `tabPurchase Order` po ON po.name = poi.parent
		WHERE poi.cost_code = %s
		AND po.project = (SELECT project FROM `tabJob Site` WHERE name = %s)
		AND po.docstatus = 1
		AND po.status NOT IN ('Closed', 'Completed')
	""", (bl.cost_code, bl.job_site), as_dict=True)[0].total
	
	frappe.db.set_value("Budget Line", budget_line, {
		"actual_cost": actual,
		"committed_cost": committed,
	})
	
	# Trigger recalculation
	doc = frappe.get_doc("Budget Line", budget_line)
	doc.save()
	
	return doc.as_dict()
