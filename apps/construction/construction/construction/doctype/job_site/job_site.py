import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, getdate, date_diff, today


class JobSite(Document):
	def validate(self):
		self.calculate_contract_value()
		self.calculate_financial_metrics()
		self.calculate_schedule_metrics()
		self.validate_dates()

	def calculate_contract_value(self):
		"""Calculate current contract value"""
		self.current_contract_value = flt(self.contract_value) + flt(self.approved_change_orders)

	def calculate_financial_metrics(self):
		"""Calculate budget and earned value metrics"""
		# Current budget
		self.current_budget = flt(self.original_budget) + flt(self.approved_changes)
		
		# Budget variance
		self.budget_variance = flt(self.current_budget) - flt(self.actual_cost)
		if self.current_budget:
			self.budget_variance_percent = (self.budget_variance / self.current_budget) * 100
		else:
			self.budget_variance_percent = 0
		
		# Earned value (BCWP)
		self.earned_value = flt(self.current_budget) * (flt(self.percent_complete) / 100)
		
		# Cost Performance Index
		if self.actual_cost:
			self.cpi = flt(self.earned_value / self.actual_cost, 3)
		else:
			self.cpi = 1.0
		
		# Projected final cost (EAC)
		if self.cpi and self.cpi > 0:
			self.projected_cost = flt(self.current_budget / self.cpi, 2)
		else:
			self.projected_cost = self.current_budget

	def calculate_schedule_metrics(self):
		"""Calculate schedule performance metrics"""
		if self.planned_end_date:
			self.days_remaining = date_diff(self.planned_end_date, today())
			
			# Schedule variance
			if self.planned_start_date and self.actual_start_date:
				planned_duration = date_diff(self.planned_end_date, self.planned_start_date)
				if planned_duration > 0:
					# Calculate expected percent complete based on elapsed time
					if self.actual_start_date:
						elapsed = date_diff(today(), self.actual_start_date)
						expected_percent = min((elapsed / planned_duration) * 100, 100)
						# SPI = actual progress / expected progress
						if expected_percent > 0:
							self.spi = flt(self.percent_complete / expected_percent, 3)
						else:
							self.spi = 1.0
					else:
						self.spi = 1.0
				else:
					self.spi = 1.0
			
			# Schedule variance in days
			if self.spi and self.spi != 1:
				total_duration = date_diff(self.planned_end_date, self.planned_start_date or today())
				self.schedule_variance_days = int(total_duration * (1 - (1 / self.spi))) if self.spi else 0

	def validate_dates(self):
		"""Validate date fields"""
		if self.planned_start_date and self.planned_end_date:
			if getdate(self.planned_end_date) < getdate(self.planned_start_date):
				frappe.throw(_("Planned End Date cannot be before Planned Start Date"))
		
		if self.actual_start_date and self.actual_end_date:
			if getdate(self.actual_end_date) < getdate(self.actual_start_date):
				frappe.throw(_("Actual End Date cannot be before Actual Start Date"))

	def on_update(self):
		"""After save actions"""
		self.sync_to_project()
		self.check_budget_alerts()

	def sync_to_project(self):
		"""Sync changes to linked ERPNext Project"""
		if self.project:
			frappe.db.set_value("Project", self.project, {
				"status": self.get_project_status(),
				"percent_complete": self.percent_complete,
				"expected_start_date": self.planned_start_date,
				"expected_end_date": self.planned_end_date,
				"actual_start_date": self.actual_start_date,
				"actual_end_date": self.actual_end_date,
			}, update_modified=False)

	def get_project_status(self):
		"""Map job site status to project status"""
		status_map = {
			"Bidding": "Open",
			"Awarded": "Open",
			"Pre-Construction": "Open",
			"Active": "Open",
			"On Hold": "Open",
			"Punch List": "Open",
			"Closeout": "Open",
			"Completed": "Completed",
			"Cancelled": "Cancelled",
		}
		return status_map.get(self.status, "Open")

	def check_budget_alerts(self):
		"""Check and send budget variance alerts"""
		settings = frappe.get_single("Construction Settings")
		if settings.notify_on_budget_variance:
			threshold = flt(settings.budget_variance_threshold)
			if self.budget_variance_percent and abs(self.budget_variance_percent) > threshold:
				self.send_budget_alert()

	def send_budget_alert(self):
		"""Send budget variance notification"""
		if not self.project_manager:
			return
		
		variance_type = "under" if self.budget_variance > 0 else "over"
		
		frappe.sendmail(
			recipients=[frappe.db.get_value("User", self.project_manager, "email")],
			subject=f"Budget Alert: {self.job_name}",
			message=f"""
				<p>Budget variance alert for job site: <strong>{self.job_name}</strong></p>
				<p>Current budget: {frappe.format_value(self.current_budget, {'fieldtype': 'Currency'})}</p>
				<p>Actual cost: {frappe.format_value(self.actual_cost, {'fieldtype': 'Currency'})}</p>
				<p>Variance: {frappe.format_value(abs(self.budget_variance), {'fieldtype': 'Currency'})} ({variance_type} budget)</p>
				<p>Variance %: {abs(self.budget_variance_percent):.1f}%</p>
			""",
			now=True,
		)


def sync_project_to_job_site(doc, method):
	"""Sync Project changes to Job Site"""
	job_sites = frappe.get_all("Job Site", filters={"project": doc.name}, pluck="name")
	for js in job_sites:
		frappe.db.set_value("Job Site", js, {
			"percent_complete": doc.percent_complete,
		}, update_modified=False)


def on_project_update(doc, method):
	"""Handle Project updates"""
	sync_project_to_job_site(doc, method)


def get_permission_query_conditions(user):
	"""Return permission query conditions for Job Site"""
	if not user:
		user = frappe.session.user

	if "System Manager" in frappe.get_roles(user) or "Construction Manager" in frappe.get_roles(user):
		return ""

	# Users can see job sites they are assigned to
	return f"""(
		`tabJob Site`.project_manager = {frappe.db.escape(user)}
		OR `tabJob Site`.superintendent = {frappe.db.escape(user)}
		OR `tabJob Site`.estimator = {frappe.db.escape(user)}
		OR EXISTS (
			SELECT 1 FROM `tabJob Site Team Member`
			WHERE `tabJob Site Team Member`.parent = `tabJob Site`.name
			AND `tabJob Site Team Member`.user = {frappe.db.escape(user)}
		)
	)"""


def has_permission(doc, ptype, user):
	"""Check if user has permission on Job Site"""
	if not user:
		user = frappe.session.user

	if "System Manager" in frappe.get_roles(user) or "Construction Manager" in frappe.get_roles(user):
		return True

	# Check if user is on the team
	if doc.project_manager == user or doc.superintendent == user or doc.estimator == user:
		return True

	# Check team members
	for member in doc.team_members:
		if member.user == user:
			return True

	return False


@frappe.whitelist()
def get_budget_summary(job_site):
	"""Get budget summary for job site"""
	doc = frappe.get_doc("Job Site", job_site)
	
	# Get budget lines
	budget_lines = frappe.get_all(
		"Budget Line",
		filters={"job_site": job_site},
		fields=["cost_code", "description", "original_budget", "approved_changes", 
				"current_budget", "actual_cost", "committed_cost", "variance"]
	)
	
	return {
		"original_budget": doc.original_budget,
		"approved_changes": doc.approved_changes,
		"current_budget": doc.current_budget,
		"actual_cost": doc.actual_cost,
		"committed_cost": doc.committed_cost,
		"projected_cost": doc.projected_cost,
		"budget_variance": doc.budget_variance,
		"budget_variance_percent": doc.budget_variance_percent,
		"cpi": doc.cpi,
		"budget_lines": budget_lines,
	}


@frappe.whitelist()
def update_job_site_costs(job_site):
	"""Recalculate job site costs from budget lines and cost entries"""
	# Sum actual costs from job cost entries
	actual = frappe.db.sql("""
		SELECT COALESCE(SUM(total_cost), 0) as total
		FROM `tabJob Cost Entry`
		WHERE job_site = %s AND docstatus = 1
	""", job_site, as_dict=True)[0].total
	
	# Sum committed costs from purchase orders
	committed = frappe.db.sql("""
		SELECT COALESCE(SUM(base_net_total), 0) as total
		FROM `tabPurchase Order`
		WHERE project = (SELECT project FROM `tabJob Site` WHERE name = %s)
		AND docstatus = 1
		AND status NOT IN ('Closed', 'Completed')
	""", job_site, as_dict=True)[0].total
	
	# Sum approved changes from budget lines
	approved_changes = frappe.db.sql("""
		SELECT COALESCE(SUM(approved_changes), 0) as total
		FROM `tabBudget Line`
		WHERE job_site = %s
	""", job_site, as_dict=True)[0].total
	
	frappe.db.set_value("Job Site", job_site, {
		"actual_cost": actual,
		"committed_cost": committed,
		"approved_changes": approved_changes,
	})
	
	# Trigger recalculation
	doc = frappe.get_doc("Job Site", job_site)
	doc.save()
	
	return doc.as_dict()


def update_job_site_progress():
	"""Scheduled task to update job site progress"""
	active_sites = frappe.get_all(
		"Job Site",
		filters={"status": ["in", ["Active", "Punch List"]]},
		pluck="name"
	)
	
	for site in active_sites:
		try:
			update_job_site_costs(site)
		except Exception as e:
			frappe.log_error(f"Error updating job site {site}: {str(e)}")
