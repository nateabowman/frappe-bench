# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe.model.document import Document


class EmployeeRecognition(Document):
	def validate(self):
		# Set default points if not provided
		if not self.points:
			point_map = {
				"Achievement": 10,
				"Excellence": 15,
				"Innovation": 20,
				"Teamwork": 10,
				"Leadership": 25,
			}
			self.points = point_map.get(self.recognition_type, 10)
	
	def on_submit(self):
		# Could trigger notifications or update employee records here
		pass
