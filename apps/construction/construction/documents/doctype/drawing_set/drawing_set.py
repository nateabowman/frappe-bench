import frappe
from frappe.model.document import Document


class DrawingSet(Document):
	def on_update(self):
		"""Create Drive folder if integration is enabled"""
		if not self.drive_folder:
			self.create_drive_folder()

	def create_drive_folder(self):
		"""Create a folder in Frappe Drive for this drawing set"""
		try:
			# Check if Drive app is installed
			if "drive" not in frappe.get_installed_apps():
				return
			
			# Create folder structure: Job Site / Drawings / Discipline
			job_site_name = frappe.db.get_value("Job Site", self.job_site, "job_name")
			folder_name = f"{job_site_name} - {self.discipline} - {self.set_name}"
			
			# This would integrate with Frappe Drive API
			# For now, just store a reference
			self.db_set("drive_folder", folder_name)
			
		except Exception as e:
			frappe.log_error(f"Could not create Drive folder: {str(e)}")


@frappe.whitelist()
def get_drawing_sets_for_job(job_site):
	"""Get all drawing sets for a job site"""
	return frappe.get_all(
		"Drawing Set",
		filters={"job_site": job_site},
		fields=["name", "set_name", "discipline", "revision", "status", "issue_date"],
		order_by="discipline, set_name"
	)


@frappe.whitelist()
def create_new_revision(drawing_set):
	"""Create a new revision of a drawing set"""
	doc = frappe.get_doc("Drawing Set", drawing_set)
	
	# Archive current version
	doc.status = "Superseded"
	doc.save()
	
	# Create new revision
	new_doc = frappe.copy_doc(doc)
	current_rev = doc.revision or "0"
	
	# Increment revision (handle numeric and alpha revisions)
	if current_rev.isdigit():
		new_doc.revision = str(int(current_rev) + 1)
	else:
		# Alpha revision (A, B, C...)
		new_doc.revision = chr(ord(current_rev) + 1)
	
	new_doc.status = "Current"
	new_doc.issue_date = frappe.utils.today()
	new_doc.insert()
	
	return new_doc.name
