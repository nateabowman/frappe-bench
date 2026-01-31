import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, now_datetime


class ChangeOrderRequest(Document):
	def validate(self):
		self.calculate_totals()
		self.set_cor_number()

	def calculate_totals(self):
		"""Calculate total cost with markup"""
		subtotal = sum([flt(item.amount) for item in self.items])
		self.cost_impact = subtotal
		markup_amount = subtotal * (flt(self.markup_percent) / 100)
		self.total_amount = subtotal + markup_amount

	def set_cor_number(self):
		"""Set sequential COR number for this job site"""
		if not self.cor_number:
			count = frappe.db.count(
				"Change Order Request",
				{"job_site": self.job_site, "name": ["!=", self.name or ""]}
			)
			self.cor_number = f"COR-{str(count + 1).zfill(3)}"

	def on_submit(self):
		"""Submit the COR"""
		self.status = "Pending"

	@frappe.whitelist()
	def approve(self, approved_amount=None, approved_schedule_days=None):
		"""Approve the COR and create Change Order"""
		self.status = "Approved"
		self.owner_response = "Approve"
		self.response_date = frappe.utils.today()
		self.approved_by = frappe.session.user
		self.approval_date = now_datetime()
		self.approved_amount = approved_amount or self.total_amount
		self.approved_schedule_days = approved_schedule_days or self.schedule_impact_days
		
		# Create Change Order
		co = self.create_change_order()
		self.change_order = co.name
		
		self.save()
		return co

	def create_change_order(self):
		"""Create a Change Order from this COR"""
		co = frappe.new_doc("Change Order")
		co.job_site = self.job_site
		co.subject = self.subject
		co.description = self.description
		co.reason_for_change = self.reason_for_change
		co.cor_reference = self.name
		co.cost_amount = self.approved_amount
		co.schedule_days = self.approved_schedule_days
		
		# Copy items
		for item in self.items:
			co.append("items", {
				"cost_code": item.cost_code,
				"description": item.description,
				"quantity": item.quantity,
				"unit": item.unit,
				"unit_cost": item.unit_cost,
				"amount": item.amount,
			})
		
		co.insert()
		return co

	@frappe.whitelist()
	def reject(self, reason=None):
		"""Reject the COR"""
		self.status = "Rejected"
		self.owner_response = "Reject"
		self.response_date = frappe.utils.today()
		if reason:
			self.notes = (self.notes or "") + f"\n\nRejection Reason: {reason}"
		self.save()
