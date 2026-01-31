# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe.model.document import Document


class EmployeePulse(Document):
	def validate(self):
		self.calculate_engagement_score()
	
	def calculate_engagement_score(self):
		"""Calculate overall engagement score from ratings"""
		ratings = [
			self.overall_satisfaction,
			self.work_life_balance,
			self.career_growth,
			self.team_collaboration,
			self.management_support,
			self.workload,
			self.compensation,
			self.work_environment,
		]
		
		# Filter out None values and calculate average
		valid_ratings = [r for r in ratings if r is not None]
		if valid_ratings:
			self.engagement_score = sum(valid_ratings) / len(valid_ratings)
		else:
			self.engagement_score = 0
