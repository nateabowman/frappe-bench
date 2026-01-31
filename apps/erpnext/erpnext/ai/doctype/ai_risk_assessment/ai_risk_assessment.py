# Copyright (c) 2024, Nexelya and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from erpnext.projects.api.feature_gating import check_feature_access
from erpnext.analytics.api.analytics import calculate_project_risk, predict_cost_overrun, predict_completion_date


class AIRiskAssessment(Document):
	def validate(self):
		# Check feature access
		if self.project:
			project_doc = frappe.get_doc("Project", self.project)
			if project_doc.company:
				check_feature_access("ai_powered_features", project_doc.company, throw=True)
		
		self.run_ai_analysis()
	
	def run_ai_analysis(self):
		"""Run AI analysis on project"""
		if not self.project:
			return
		
		project_doc = frappe.get_doc("Project", self.project)
		project_doc.update_costing()
		
		# Calculate risk score
		self.overall_risk_score = calculate_project_risk(project_doc)
		
		# Determine risk level
		if self.overall_risk_score >= 75:
			self.risk_level = "Critical"
		elif self.overall_risk_score >= 50:
			self.risk_level = "High"
		elif self.overall_risk_score >= 25:
			self.risk_level = "Medium"
		else:
			self.risk_level = "Low"
		
		# Cost risk analysis
		cost_overrun = predict_cost_overrun(project_doc)
		self.cost_risk_analysis = f"""
Risk Level: {cost_overrun.get('risk', 'Unknown').upper()}
Predicted Overrun: ${cost_overrun.get('predicted_overrun', 0):,.2f}
Predicted Final Cost: ${cost_overrun.get('predicted_final_cost', 0):,.2f}
Overrun Percentage: {cost_overrun.get('overrun_percent', 0):.1f}%
		""".strip()
		
		# Schedule risk analysis
		predicted_completion = predict_completion_date(project_doc)
		if predicted_completion:
			from frappe.utils import getdate, date_diff
			days_delay = date_diff(predicted_completion, project_doc.expected_end_date) if project_doc.expected_end_date else 0
			self.schedule_risk_analysis = f"""
Predicted Completion Date: {predicted_completion}
Expected Completion Date: {project_doc.expected_end_date or 'Not set'}
Days Delay: {days_delay} days
		""".strip()
		
		# Generate recommendations
		recommendations = []
		if cost_overrun.get('risk') == 'high':
			recommendations.append("⚠️ High cost overrun risk detected. Review and optimize project costs immediately.")
		if self.overall_risk_score > 70:
			recommendations.append("⚠️ Project is at high risk. Consider additional resources or scope reduction.")
		if project_doc.percent_complete < 50 and project_doc.expected_end_date:
			recommendations.append("📊 Project progress is behind schedule. Review task dependencies and resource allocation.")
		
		self.recommendations = "\n".join(recommendations) if recommendations else "✅ Project is on track with acceptable risk levels."

