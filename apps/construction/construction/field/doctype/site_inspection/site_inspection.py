import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime


class SiteInspection(Document):
	def validate(self):
		self.calculate_results()

	def calculate_results(self):
		"""Calculate inspection results"""
		self.total_items = len(self.inspection_items)
		self.passed_items = len([i for i in self.inspection_items if i.result == "Pass"])
		self.failed_items = len([i for i in self.inspection_items if i.result == "Fail"])
		
		if self.total_items:
			self.pass_rate = (self.passed_items / self.total_items) * 100
		else:
			self.pass_rate = 0
		
		# Determine overall result
		if self.total_items == 0:
			self.overall_result = ""
		elif self.failed_items == 0:
			self.overall_result = "Pass"
		elif self.pass_rate >= 80:
			self.overall_result = "Conditional Pass"
		else:
			self.overall_result = "Fail"
		
		# Update result field based on overall
		if self.overall_result:
			result_map = {
				"Pass": "Passed",
				"Conditional Pass": "Passed with Comments",
				"Fail": "Failed"
			}
			self.result = result_map.get(self.overall_result, "Pending")

	def on_submit(self):
		self.status = "Completed"
		if self.inspector_signature:
			self.signature_date = now_datetime()

	def before_submit(self):
		if self.overall_result == "Fail":
			self.status = "Re-inspection Required"
