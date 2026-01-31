import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class ChangeOrder(Document):
	def validate(self):
		self.set_co_number()
		self.calculate_contract_values()

	def set_co_number(self):
		"""Set sequential CO number for this job site"""
		if not self.co_number:
			count = frappe.db.count(
				"Change Order",
				{"job_site": self.job_site, "name": ["!=", self.name or ""]}
			)
			self.co_number = f"CO-{str(count + 1).zfill(3)}"

	def calculate_contract_values(self):
		"""Calculate previous and new contract values"""
		job_site = frappe.get_doc("Job Site", self.job_site)
		self.previous_contract_value = job_site.current_contract_value or job_site.contract_value
		self.new_contract_value = flt(self.previous_contract_value) + flt(self.cost_amount)

	def on_submit(self):
		"""Execute the change order"""
		self.status = "Executed"
		self.update_job_site()
		self.update_budget_lines()

	def on_cancel(self):
		"""Cancel the change order"""
		self.status = "Void"
		# Reverse the job site updates
		frappe.db.set_value("Job Site", self.job_site, {
			"approved_change_orders": frappe.db.get_value("Job Site", self.job_site, "approved_change_orders") - self.cost_amount
		})

	def update_job_site(self):
		"""Update job site with change order amounts"""
		job_site = frappe.get_doc("Job Site", self.job_site)
		
		# Update approved change orders total
		total_cos = frappe.db.sql("""
			SELECT COALESCE(SUM(cost_amount), 0) as total
			FROM `tabChange Order`
			WHERE job_site = %s AND docstatus = 1
		""", self.job_site, as_dict=True)[0].total
		
		job_site.approved_change_orders = total_cos
		
		# Update schedule if days added
		if self.schedule_days and job_site.planned_end_date:
			from frappe.utils import add_days
			job_site.planned_end_date = add_days(job_site.planned_end_date, self.schedule_days)
		
		job_site.save()

	def update_budget_lines(self):
		"""Update budget lines with approved changes"""
		for item in self.items:
			if item.cost_code:
				# Find or create budget line
				budget_line = frappe.db.get_value(
					"Budget Line",
					{"job_site": self.job_site, "cost_code": item.cost_code},
					"name"
				)
				if budget_line:
					current = frappe.db.get_value("Budget Line", budget_line, "approved_changes") or 0
					frappe.db.set_value("Budget Line", budget_line, 
						"approved_changes", flt(current) + flt(item.amount))


@frappe.whitelist()
def get_change_order_summary(job_site):
	"""Get change order summary for a job site"""
	cos = frappe.get_all(
		"Change Order",
		filters={"job_site": job_site, "docstatus": 1},
		fields=["name", "co_number", "subject", "cost_amount", "schedule_days", "effective_date"]
	)
	
	total_amount = sum([co.cost_amount for co in cos])
	total_days = sum([co.schedule_days or 0 for co in cos])
	
	return {
		"change_orders": cos,
		"count": len(cos),
		"total_amount": total_amount,
		"total_days": total_days,
	}
