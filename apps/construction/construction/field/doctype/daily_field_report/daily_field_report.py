import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, now_datetime


class DailyFieldReport(Document):
	def validate(self):
		self.calculate_man_hours()
		self.validate_report_date()

	def calculate_man_hours(self):
		"""Calculate total man hours from crew"""
		total = 0
		for crew in self.crew_members:
			total += flt(crew.hours_worked)
		self.total_man_hours = total

	def validate_report_date(self):
		"""Ensure report date is not in the future"""
		from frappe.utils import getdate, today
		if getdate(self.report_date) > getdate(today()):
			frappe.throw(_("Report date cannot be in the future"))

	def on_submit(self):
		"""Actions on submit"""
		self.status = "Submitted"
		self.update_job_site_weather_delay()

	def on_cancel(self):
		"""Actions on cancel"""
		self.status = "Cancelled"

	def update_job_site_weather_delay(self):
		"""Update job site weather delay days"""
		if self.weather_delay_hours > 0:
			# Convert hours to days (assuming 8-hour workday)
			delay_days = flt(self.weather_delay_hours / 8, 2)
			current_delay = frappe.db.get_value("Job Site", self.job_site, "weather_delay_days") or 0
			frappe.db.set_value("Job Site", self.job_site, 
				"weather_delay_days", flt(current_delay) + delay_days)

	@frappe.whitelist()
	def approve(self):
		"""Approve the daily report"""
		self.status = "Approved"
		self.approved_by = frappe.session.user
		self.approval_date = now_datetime()
		self.save()


@frappe.whitelist()
def fetch_weather_for_report(job_site):
	"""Fetch current weather for daily report"""
	from construction.api.weather import get_weather_for_location
	
	coords = frappe.db.get_value("Job Site", job_site, ["latitude", "longitude"], as_dict=True)
	if coords and coords.latitude and coords.longitude:
		return get_weather_for_location(coords.latitude, coords.longitude)
	return None


@frappe.whitelist()
def get_reports_summary(job_site, start_date=None, end_date=None):
	"""Get summary of daily reports for a job site"""
	filters = {"job_site": job_site, "docstatus": 1}
	if start_date:
		filters["report_date"] = [">=", start_date]
	if end_date:
		if "report_date" in filters:
			filters["report_date"] = ["between", [start_date, end_date]]
		else:
			filters["report_date"] = ["<=", end_date]
	
	reports = frappe.get_all(
		"Daily Field Report",
		filters=filters,
		fields=[
			"report_date",
			"total_man_hours",
			"weather_delay_hours",
			"weather_condition",
			"safety_incidents"
		],
		order_by="report_date"
	)
	
	return {
		"reports": reports,
		"total_man_hours": sum([r.total_man_hours for r in reports]),
		"total_weather_delay": sum([r.weather_delay_hours for r in reports]),
		"total_incidents": sum([r.safety_incidents for r in reports]),
		"report_count": len(reports),
	}


def get_permission_query_conditions(user):
	"""Return permission query conditions for Daily Field Report"""
	if not user:
		user = frappe.session.user

	if "System Manager" in frappe.get_roles(user) or "Construction Manager" in frappe.get_roles(user):
		return ""

	# Field workers can see reports they submitted
	# Superintendents can see reports for their job sites
	return f"""(
		`tabDaily Field Report`.submitted_by = {frappe.db.escape(user)}
		OR EXISTS (
			SELECT 1 FROM `tabJob Site`
			WHERE `tabJob Site`.name = `tabDaily Field Report`.job_site
			AND (`tabJob Site`.superintendent = {frappe.db.escape(user)}
				OR `tabJob Site`.project_manager = {frappe.db.escape(user)})
		)
	)"""
