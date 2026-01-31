// Construction App JavaScript

frappe.provide("construction");

// Initialize Construction App
construction.init = function() {
	// Add construction-specific quick actions
	construction.setup_quick_actions();
	
	// Setup keyboard shortcuts
	construction.setup_shortcuts();
};

construction.setup_quick_actions = function() {
	// Add quick action buttons to desk
	if (frappe.boot.construction_enabled) {
		frappe.quick_actions = frappe.quick_actions || [];
		frappe.quick_actions.push({
			label: __("New Daily Log"),
			action: () => frappe.new_doc("Daily Field Report"),
			icon: "clipboard",
		});
	}
};

construction.setup_shortcuts = function() {
	// Ctrl+Shift+D - New Daily Log
	frappe.ui.keys.add_shortcut({
		shortcut: "ctrl+shift+d",
		action: () => frappe.new_doc("Daily Field Report"),
		description: __("Create New Daily Log"),
		page: "*",
	});
	
	// Ctrl+Shift+R - New RFI
	frappe.ui.keys.add_shortcut({
		shortcut: "ctrl+shift+r",
		action: () => frappe.new_doc("RFI"),
		description: __("Create New RFI"),
		page: "*",
	});
};

// Job Site Utilities
construction.JobSite = {
	get_budget_summary: function(job_site, callback) {
		frappe.call({
			method: "construction.construction.doctype.job_site.job_site.get_budget_summary",
			args: { job_site: job_site },
			callback: function(r) {
				if (callback) callback(r.message);
			}
		});
	},
	
	get_schedule_status: function(job_site, callback) {
		frappe.call({
			method: "construction.scheduling.doctype.gantt_schedule.gantt_schedule.get_schedule_status",
			args: { job_site: job_site },
			callback: function(r) {
				if (callback) callback(r.message);
			}
		});
	}
};

// Cost Code Utilities
construction.CostCode = {
	get_hierarchy: function(callback) {
		frappe.call({
			method: "construction.construction.doctype.cost_code.cost_code.get_cost_code_hierarchy",
			callback: function(r) {
				if (callback) callback(r.message);
			}
		});
	},
	
	get_budget_by_code: function(job_site, cost_code, callback) {
		frappe.call({
			method: "construction.construction.doctype.budget_line.budget_line.get_budget_by_code",
			args: { job_site: job_site, cost_code: cost_code },
			callback: function(r) {
				if (callback) callback(r.message);
			}
		});
	}
};

// Weather Integration
construction.Weather = {
	fetch_current: function(latitude, longitude, callback) {
		frappe.call({
			method: "construction.api.weather.get_weather_for_location",
			args: { latitude: latitude, longitude: longitude },
			callback: function(r) {
				if (callback) callback(r.message);
			}
		});
	},
	
	auto_fill_daily_log: function(frm) {
		if (frm.doc.job_site) {
			frappe.db.get_value("Job Site", frm.doc.job_site, ["latitude", "longitude"], function(r) {
				if (r && r.latitude && r.longitude) {
					construction.Weather.fetch_current(r.latitude, r.longitude, function(weather) {
						if (weather && weather.success) {
							frm.set_value("weather_condition", weather.condition);
							frm.set_value("temperature", weather.temperature);
							frm.set_value("wind_speed", weather.wind_speed);
							frm.set_value("precipitation", weather.precipitation);
							frappe.show_alert({
								message: __("Weather data updated"),
								indicator: "green"
							});
						}
					});
				}
			});
		}
	}
};

// Gantt Chart Utilities
construction.Gantt = {
	render: function(container, schedule_name, options) {
		options = options || {};
		
		frappe.call({
			method: "construction.scheduling.doctype.gantt_schedule.gantt_schedule.get_gantt_data",
			args: { schedule_name: schedule_name },
			callback: function(r) {
				if (r.message) {
					construction.Gantt._render_chart(container, r.message, options);
				}
			}
		});
	},
	
	_render_chart: function(container, data, options) {
		// Use Frappe Gantt or custom implementation
		if (typeof Gantt !== "undefined") {
			new Gantt(container, data.tasks, {
				view_modes: ["Day", "Week", "Month"],
				view_mode: options.view_mode || "Week",
				custom_popup_html: function(task) {
					return construction.Gantt._get_popup_html(task);
				},
				on_click: function(task) {
					if (options.on_click) options.on_click(task);
				},
				on_date_change: function(task, start, end) {
					if (options.on_date_change) options.on_date_change(task, start, end);
				}
			});
		}
	},
	
	_get_popup_html: function(task) {
		return `
			<div class="gantt-popup">
				<h4>${task.name}</h4>
				<p>Start: ${frappe.datetime.str_to_user(task.start)}</p>
				<p>End: ${frappe.datetime.str_to_user(task.end)}</p>
				<p>Progress: ${task.progress}%</p>
				${task.is_critical ? '<span class="badge badge-danger">Critical Path</span>' : ''}
			</div>
		`;
	}
};

// Punch List Utilities
construction.PunchList = {
	capture_photo: function(callback) {
		// Mobile camera capture
		if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
			frappe.require("assets/frappe/js/lib/webcam.min.js", function() {
				// Implement webcam capture
				if (callback) callback(null, "Camera not implemented");
			});
		} else {
			frappe.msgprint(__("Camera not available on this device"));
		}
	},
	
	batch_complete: function(items, callback) {
		frappe.call({
			method: "construction.field.doctype.punch_list.punch_list.batch_complete_items",
			args: { items: items },
			callback: function(r) {
				if (callback) callback(r.message);
			}
		});
	}
};

// Format helpers
construction.format = {
	currency: function(value, currency) {
		return format_currency(value, currency);
	},
	
	variance: function(budget, actual) {
		var variance = budget - actual;
		var percent = budget ? ((variance / budget) * 100).toFixed(1) : 0;
		var cls = variance >= 0 ? "variance-positive" : "variance-negative";
		return `<span class="${cls}">${construction.format.currency(variance)} (${percent}%)</span>`;
	},
	
	progress_bar: function(percent, status) {
		status = status || (percent >= 100 ? "on-track" : percent >= 75 ? "at-risk" : "behind");
		return `
			<div class="construction-progress">
				<div class="progress-bar ${status}" style="width: ${Math.min(percent, 100)}%"></div>
			</div>
		`;
	}
};

// Initialize on ready
$(document).ready(function() {
	construction.init();
});
