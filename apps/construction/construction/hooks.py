app_name = "construction"
app_title = "Nexelya Construction"
app_publisher = "Nexelya Technologies Pvt. Ltd."
app_description = "Construction Management Platform - Project Management, Job Costing, Field Operations"
app_email = "support@nexelya.io"
app_license = "AGPLv3"
app_icon_url = "/assets/construction/images/logo.svg"
app_icon_title = "Construction"
app_icon_route = "/construction"

# Apps
# ------------------

required_apps = ["frappe", "erpnext"]

add_to_apps_screen = [
	{
		"name": "construction",
		"logo": "/assets/construction/images/logo.svg",
		"title": "Construction",
		"route": "/app/construction",
	}
]

# Includes in <head>
# ------------------

app_include_css = "/assets/construction/css/construction.css"
app_include_js = "/assets/construction/js/construction.js"

# Website routes
website_route_rules = [
	{"from_route": "/subcontractor-portal", "to_route": "subcontractor_portal"},
]

# Installation
# ------------

before_install = "construction.install.before_install"
after_install = "construction.install.after_install"

# Uninstallation
# ------------

before_uninstall = "construction.uninstall.before_uninstall"

# DocType Class
# ---------------

override_doctype_class = {}

# Document Events
# ---------------

doc_events = {
	"Project": {
		"validate": ["construction.construction.doctype.job_site.job_site.sync_project_to_job_site"],
		"on_update": ["construction.construction.doctype.job_site.job_site.on_project_update"],
	},
	"Purchase Invoice": {
		"on_submit": ["construction.construction.doctype.job_cost_entry.job_cost_entry.create_from_purchase_invoice"],
	},
	"Timesheet": {
		"on_submit": ["construction.construction.doctype.job_cost_entry.job_cost_entry.create_from_timesheet"],
	},
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	"daily": [
		"construction.construction.doctype.job_site.job_site.update_job_site_progress",
		"construction.scheduling.doctype.gantt_schedule.gantt_schedule.recalculate_critical_paths",
	],
	"hourly": [
		"construction.api.weather.fetch_weather_for_active_sites",
	],
}

# Jinja
# ----------

jinja = {
	"methods": "construction.utils.jinja_methods",
}

# Fixtures
# --------

fixtures = [
	{
		"doctype": "Role",
		"filters": [["name", "in", [
			"Construction Manager",
			"Project Superintendent",
			"Field Worker",
			"Subcontractor User",
			"Estimator",
		]]]
	},
	{
		"doctype": "Custom Field",
		"filters": [["dt", "in", ["Project", "Task", "Supplier"]]]
	},
]

# Permission query conditions
# ---------------------------

permission_query_conditions = {
	"Job Site": "construction.construction.doctype.job_site.job_site.get_permission_query_conditions",
	"Daily Field Report": "construction.field.doctype.daily_field_report.daily_field_report.get_permission_query_conditions",
}

has_permission = {
	"Job Site": "construction.construction.doctype.job_site.job_site.has_permission",
}

# Standard portal menu items
# --------------------------

standard_portal_menu_items = [
	{"title": "Job Sites", "route": "/job-sites", "role": "Customer"},
	{"title": "Subcontractor Portal", "route": "/subcontractor-portal", "role": "Subcontractor User"},
]

# DocType JS overrides
# --------------------

doctype_js = {
	"Project": "public/js/project.js",
	"Task": "public/js/task.js",
}

# Notification config
# -------------------

notification_config = "construction.notifications.get_notification_config"
