# Copyright (c) 2024, Nexelya and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from erpnext.projects.api.feature_gating import check_feature_access


class InspectionForm(Document):
	def validate(self):
		# Check feature access
		if self.project:
			project_doc = frappe.get_doc("Project", self.project)
			if project_doc.company:
				check_feature_access("quality_control_inspections", project_doc.company, throw=True)

