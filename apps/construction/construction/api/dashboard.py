import frappe
from frappe.utils import today, add_days


@frappe.whitelist()
def get_field_stats():
	"""Get statistics for field app dashboard"""
	user = frappe.session.user
	
	# Active job count
	active_jobs = frappe.db.sql("""
		SELECT COUNT(DISTINCT js.name) as count
		FROM `tabJob Site` js
		LEFT JOIN `tabJob Site Team Member` tm ON tm.parent = js.name
		WHERE js.status IN ('Active', 'Pre-Construction', 'Punch List')
		AND (
			js.project_manager = %(user)s
			OR js.superintendent = %(user)s
			OR tm.user = %(user)s
		)
	""", {"user": user}, as_dict=True)[0].count
	
	# Today's logs
	today_logs = frappe.db.count("Daily Field Report", {
		"submitted_by": user,
		"report_date": today()
	})
	
	# Open punch items
	open_punch = frappe.db.sql("""
		SELECT COUNT(*) as count
		FROM `tabPunch List Item` pli
		JOIN `tabPunch List` pl ON pl.name = pli.parent
		JOIN `tabJob Site` js ON js.name = pl.job_site
		LEFT JOIN `tabJob Site Team Member` tm ON tm.parent = js.name
		WHERE pli.status != 'Completed'
		AND (
			js.project_manager = %(user)s
			OR js.superintendent = %(user)s
			OR tm.user = %(user)s
		)
	""", {"user": user}, as_dict=True)[0].count
	
	# Pending RFIs
	pending_rfis = frappe.db.count("RFI", {"status": "Open"})
	
	return {
		"activeJobs": active_jobs,
		"todayLogs": today_logs,
		"openPunchItems": open_punch,
		"pendingRfis": pending_rfis,
	}


@frappe.whitelist()
def get_field_chart_data():
	"""Get chart data for field dashboard visualizations"""
	user = frappe.session.user
	from frappe.utils import today, add_days, getdate
	from datetime import timedelta
	
	# Daily logs trend (last 30 days)
	thirty_days_ago = add_days(today(), -30)
	daily_logs_data = frappe.db.sql("""
		SELECT 
			report_date as date,
			COUNT(*) as count
		FROM `tabDaily Field Report`
		WHERE submitted_by = %(user)s
		AND report_date >= %(start_date)s
		GROUP BY report_date
		ORDER BY report_date
	""", {"user": user, "start_date": thirty_days_ago}, as_dict=True)
	
	# Punch items by status
	punch_by_status = frappe.db.sql("""
		SELECT 
			pli.status,
			COUNT(*) as count
		FROM `tabPunch List Item` pli
		JOIN `tabPunch List` pl ON pl.name = pli.parent
		JOIN `tabJob Site` js ON js.name = pl.job_site
		LEFT JOIN `tabJob Site Team Member` tm ON tm.parent = js.name
		WHERE (
			js.project_manager = %(user)s
			OR js.superintendent = %(user)s
			OR tm.user = %(user)s
		)
		GROUP BY pli.status
	""", {"user": user}, as_dict=True)
	
	# Activity by type (last 7 days)
	seven_days_ago = add_days(today(), -7)
	activity_data = frappe.db.sql("""
		SELECT 
			'Daily Logs' as type,
			COUNT(*) as count
		FROM `tabDaily Field Report`
		WHERE submitted_by = %(user)s
		AND report_date >= %(start_date)s
		UNION ALL
		SELECT 
			'Punch Items Completed' as type,
			COUNT(*) as count
		FROM `tabPunch List Item` pli
		JOIN `tabPunch List` pl ON pl.name = pli.parent
		JOIN `tabJob Site` js ON js.name = pl.job_site
		LEFT JOIN `tabJob Site Team Member` tm ON tm.parent = js.name
		WHERE pli.status = 'Completed'
		AND pli.completed_date >= %(start_date)s
		AND (
			js.project_manager = %(user)s
			OR js.superintendent = %(user)s
			OR tm.user = %(user)s
		)
		UNION ALL
		SELECT 
			'RFIs Submitted' as type,
			COUNT(*) as count
		FROM `tabRFI`
		WHERE submitted_by = %(user)s
		AND creation >= %(start_date)s
	""", {"user": user, "start_date": seven_days_ago}, as_dict=True)
	
	# Project progress (if user has access to projects)
	project_progress = frappe.db.sql("""
		SELECT 
			js.job_name as name,
			js.percent_complete as progress
		FROM `tabJob Site` js
		LEFT JOIN `tabJob Site Team Member` tm ON tm.parent = js.name
		WHERE js.status IN ('Active', 'Pre-Construction', 'Punch List')
		AND (
			js.project_manager = %(user)s
			OR js.superintendent = %(user)s
			OR tm.user = %(user)s
		)
		ORDER BY js.percent_complete DESC
		LIMIT 5
	""", {"user": user}, as_dict=True)
	
	return {
		"dailyLogsTrend": daily_logs_data,
		"punchByStatus": punch_by_status,
		"activityByType": activity_data,
		"projectProgress": project_progress,
	}


@frappe.whitelist()
def get_project_dashboard(job_site):
	"""Get dashboard data for a specific job site"""
	doc = frappe.get_doc("Job Site", job_site)
	
	# Recent daily logs
	recent_logs = frappe.get_all(
		"Daily Field Report",
		filters={"job_site": job_site},
		fields=["name", "report_date", "total_man_hours", "weather_condition"],
		order_by="report_date desc",
		limit=5
	)
	
	# Open RFIs
	open_rfis = frappe.db.count("RFI", {"project": doc.project, "status": "Open"})
	
	# Open submittals
	open_submittals = frappe.db.count("Submittal", {"project": doc.project, "status": ["in", ["Open", "Pending Review"]]})
	
	# Punch list summary
	punch_summary = frappe.db.sql("""
		SELECT 
			COUNT(*) as total,
			SUM(CASE WHEN pli.status = 'Completed' THEN 1 ELSE 0 END) as completed
		FROM `tabPunch List Item` pli
		JOIN `tabPunch List` pl ON pl.name = pli.parent
		WHERE pl.job_site = %s
	""", job_site, as_dict=True)[0]
	
	# Budget summary
	budget_summary = {
		"original": doc.original_budget,
		"current": doc.current_budget,
		"actual": doc.actual_cost,
		"variance": doc.budget_variance,
		"variance_percent": doc.budget_variance_percent,
		"cpi": doc.cpi,
	}
	
	return {
		"job_site": doc.as_dict(),
		"recent_logs": recent_logs,
		"open_rfis": open_rfis,
		"open_submittals": open_submittals,
		"punch_summary": punch_summary,
		"budget_summary": budget_summary,
	}


@frappe.whitelist()
def get_executive_dashboard():
	"""Get executive-level dashboard data"""
	# All active projects summary
	projects = frappe.get_all(
		"Job Site",
		filters={"status": ["in", ["Active", "Pre-Construction", "Punch List"]]},
		fields=[
			"name", "job_name", "status", "percent_complete",
			"current_budget", "actual_cost", "budget_variance_percent",
			"cpi", "spi", "planned_end_date"
		],
		order_by="planned_end_date"
	)
	
	# Portfolio totals
	total_budget = sum([p.current_budget or 0 for p in projects])
	total_actual = sum([p.actual_cost or 0 for p in projects])
	avg_cpi = sum([p.cpi or 1 for p in projects]) / len(projects) if projects else 1
	avg_spi = sum([p.spi or 1 for p in projects]) / len(projects) if projects else 1
	
	# At-risk projects (CPI < 0.9 or SPI < 0.9)
	at_risk = [p for p in projects if (p.cpi and p.cpi < 0.9) or (p.spi and p.spi < 0.9)]
	
	# Upcoming milestones
	upcoming_milestones = frappe.db.sql("""
		SELECT 
			sa.activity_name,
			gs.job_site,
			js.job_name,
			sa.end_date
		FROM `tabSchedule Activity` sa
		JOIN `tabGantt Schedule` gs ON gs.name = sa.parent
		JOIN `tabJob Site` js ON js.name = gs.job_site
		WHERE sa.is_milestone = 1
		AND sa.status != 'Completed'
		AND sa.end_date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY)
		ORDER BY sa.end_date
		LIMIT 10
	""", as_dict=True)
	
	return {
		"projects": projects,
		"portfolio_totals": {
			"total_budget": total_budget,
			"total_actual": total_actual,
			"total_variance": total_budget - total_actual,
			"avg_cpi": avg_cpi,
			"avg_spi": avg_spi,
		},
		"at_risk_projects": at_risk,
		"upcoming_milestones": upcoming_milestones,
		"project_count": len(projects),
	}
