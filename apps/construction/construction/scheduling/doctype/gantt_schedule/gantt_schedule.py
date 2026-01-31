import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, getdate, add_days, date_diff


class GanttSchedule(Document):
	def validate(self):
		self.calculate_schedule_metrics()
		if self.use_cpm:
			self.calculate_critical_path()

	def calculate_schedule_metrics(self):
		"""Calculate schedule summary metrics"""
		self.total_activities = len(self.activities)
		self.completed_activities = len([a for a in self.activities if a.status == "Completed"])
		
		if self.total_activities:
			self.percent_complete = (self.completed_activities / self.total_activities) * 100
		else:
			self.percent_complete = 0
		
		# Calculate end date from activities (only when at least one has end_date)
		activity_end_dates = [getdate(a.end_date) for a in self.activities if a.end_date]
		if activity_end_dates:
			self.end_date = max(activity_end_dates)
		elif self.activities and self.start_date:
			# No activity end dates yet: use schedule start as fallback
			self.end_date = self.start_date

	def calculate_critical_path(self):
		"""Calculate critical path using CPM algorithm"""
		if not self.activities:
			return
		
		# Build activity graph
		activities = {a.activity_id: a for a in self.activities}
		
		# Forward pass - calculate early start and early finish
		for activity in self.activities:
			self._forward_pass(activity, activities)
		
		# Backward pass - calculate late start and late finish
		max_early_finish = max([a.early_finish or 0 for a in self.activities])
		for activity in reversed(self.activities):
			self._backward_pass(activity, activities, max_early_finish)
		
		# Calculate float and identify critical path
		critical_path_activities = []
		for activity in self.activities:
			activity.total_float = flt(activity.late_start or 0) - flt(activity.early_start or 0)
			activity.free_float = self._calculate_free_float(activity, activities)
			activity.is_critical = activity.total_float == 0
			if activity.is_critical:
				critical_path_activities.append(activity)
		
		# Update schedule metrics
		self.critical_path_length = len(critical_path_activities)
		self.total_float = min([a.total_float for a in self.activities]) if self.activities else 0

	def _forward_pass(self, activity, activities):
		"""Calculate early start and early finish"""
		predecessors = activity.predecessors.split(",") if activity.predecessors else []
		predecessors = [p.strip() for p in predecessors if p.strip()]
		
		if not predecessors:
			activity.early_start = 0
		else:
			max_pred_finish = 0
			for pred_id in predecessors:
				if pred_id in activities:
					pred = activities[pred_id]
					pred_finish = flt(pred.early_finish or 0)
					# Handle lag
					lag = self._get_lag(activity.predecessors, pred_id)
					max_pred_finish = max(max_pred_finish, pred_finish + lag)
			activity.early_start = max_pred_finish
		
		activity.early_finish = flt(activity.early_start) + flt(activity.duration or 0)

	def _backward_pass(self, activity, activities, max_finish):
		"""Calculate late start and late finish"""
		successors = self._get_successors(activity.activity_id, activities)
		
		if not successors:
			activity.late_finish = max_finish
		else:
			min_succ_start = max_finish
			for succ in successors:
				succ_start = flt(succ.late_start or max_finish)
				lag = self._get_lag(succ.predecessors, activity.activity_id)
				min_succ_start = min(min_succ_start, succ_start - lag)
			activity.late_finish = min_succ_start
		
		activity.late_start = flt(activity.late_finish) - flt(activity.duration or 0)

	def _get_successors(self, activity_id, activities):
		"""Get successor activities"""
		successors = []
		for act in activities.values():
			if act.predecessors:
				preds = [p.strip().split("+")[0].split("-")[0] for p in act.predecessors.split(",")]
				if activity_id in preds:
					successors.append(act)
		return successors

	def _get_lag(self, predecessors_str, pred_id):
		"""Extract lag from predecessor string (e.g., 'A+2' means A with 2 day lag)"""
		if not predecessors_str:
			return 0
		for pred in predecessors_str.split(","):
			pred = pred.strip()
			if pred.startswith(pred_id):
				if "+" in pred:
					return int(pred.split("+")[1])
				elif "-" in pred and pred.index("-") > 0:
					return -int(pred.split("-")[1])
		return 0

	def _calculate_free_float(self, activity, activities):
		"""Calculate free float"""
		successors = self._get_successors(activity.activity_id, activities)
		if not successors:
			return flt(activity.late_finish or 0) - flt(activity.early_finish or 0)
		
		min_succ_early_start = min([flt(s.early_start or 0) for s in successors])
		return min_succ_early_start - flt(activity.early_finish or 0)

	def on_update(self):
		"""Update job site schedule data"""
		if self.status == "Active":
			frappe.db.set_value("Job Site", self.job_site, {
				"planned_start_date": self.start_date,
				"planned_end_date": self.end_date,
			})


@frappe.whitelist()
def get_gantt_data(schedule_name):
	"""Get data formatted for Gantt chart rendering"""
	doc = frappe.get_doc("Gantt Schedule", schedule_name)
	
	tasks = []
	for activity in doc.activities:
		task = {
			"id": activity.activity_id,
			"name": activity.activity_name,
			"start": str(activity.start_date) if activity.start_date else str(doc.start_date),
			"end": str(activity.end_date) if activity.end_date else str(add_days(doc.start_date, activity.duration or 1)),
			"progress": activity.percent_complete or 0,
			"dependencies": activity.predecessors or "",
			"is_critical": activity.is_critical,
			"is_milestone": activity.is_milestone,
			"custom_class": "critical" if activity.is_critical else "",
		}
		tasks.append(task)
	
	return {
		"tasks": tasks,
		"schedule_name": doc.schedule_name,
		"start_date": str(doc.start_date),
		"end_date": str(doc.end_date),
	}


@frappe.whitelist()
def get_schedule_status(job_site):
	"""Get schedule status for a job site"""
	schedule = frappe.db.get_value(
		"Gantt Schedule",
		{"job_site": job_site, "status": "Active"},
		["name", "percent_complete", "schedule_variance_days", "critical_path_length"],
		as_dict=True
	)
	return schedule


@frappe.whitelist()
def update_activity_dates(schedule_name, activity_id, start_date, end_date):
	"""Update activity dates from Gantt chart drag"""
	doc = frappe.get_doc("Gantt Schedule", schedule_name)
	
	for activity in doc.activities:
		if activity.activity_id == activity_id:
			activity.start_date = start_date
			activity.end_date = end_date
			activity.duration = date_diff(end_date, start_date) + 1
			break
	
	doc.save()
	return doc.as_dict()


def recalculate_critical_paths():
	"""Scheduled task to recalculate critical paths"""
	active_schedules = frappe.get_all(
		"Gantt Schedule",
		filters={"status": "Active", "use_cpm": 1},
		pluck="name"
	)
	
	for schedule in active_schedules:
		try:
			doc = frappe.get_doc("Gantt Schedule", schedule)
			doc.calculate_critical_path()
			doc.db_update()
		except Exception as e:
			frappe.log_error(f"Error recalculating CPM for {schedule}: {str(e)}")
