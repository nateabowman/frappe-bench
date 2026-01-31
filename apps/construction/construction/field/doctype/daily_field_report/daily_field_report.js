frappe.ui.form.on('Daily Field Report', {
	refresh: function(frm) {
		// Add weather fetch button
		if (!frm.is_new()) {
			frm.add_custom_button(__('Fetch Weather'), function() {
				fetch_weather(frm);
			});
		}

		// Add approve button for managers
		if (frm.doc.docstatus === 1 && frm.doc.status === 'Submitted') {
			if (frappe.user.has_role(['Construction Manager', 'Project Superintendent'])) {
				frm.add_custom_button(__('Approve'), function() {
					frm.call('approve').then(() => {
						frm.reload_doc();
						frappe.show_alert({
							message: __('Report approved'),
							indicator: 'green'
						});
					});
				}, __('Actions'));
			}
		}

		// Add GPS capture button
		if (frm.doc.docstatus === 0) {
			frm.add_custom_button(__('Capture Location'), function() {
				capture_gps_location(frm);
			});
		}

		// Show man hours summary
		if (frm.doc.total_man_hours) {
			frm.dashboard.add_indicator(
				__('Man Hours: ') + frm.doc.total_man_hours.toFixed(1),
				'blue'
			);
		}

		// Show safety alert
		if (frm.doc.safety_incidents > 0) {
			frm.dashboard.add_indicator(
				__('Safety Incidents: ') + frm.doc.safety_incidents,
				'red'
			);
		}
	},

	job_site: function(frm) {
		if (frm.doc.job_site && !frm.doc.weather_condition) {
			// Auto-fetch weather
			fetch_weather(frm);
		}
	},

	superintendent_signature: function(frm) {
		if (frm.doc.superintendent_signature) {
			frm.set_value('signature_date', frappe.datetime.now_datetime());
		}
	}
});

frappe.ui.form.on('Daily Field Report Crew', {
	hours_worked: function(frm, cdt, cdn) {
		calculate_total_hours(frm);
	},

	crew_members_remove: function(frm) {
		calculate_total_hours(frm);
	}
});

function calculate_total_hours(frm) {
	var total = 0;
	(frm.doc.crew_members || []).forEach(function(row) {
		total += flt(row.hours_worked);
	});
	frm.set_value('total_man_hours', total);
}

function fetch_weather(frm) {
	if (!frm.doc.job_site) {
		frappe.msgprint(__('Please select a Job Site first'));
		return;
	}

	frappe.call({
		method: 'construction.field.doctype.daily_field_report.daily_field_report.fetch_weather_for_report',
		args: { job_site: frm.doc.job_site },
		freeze: true,
		freeze_message: __('Fetching weather data...'),
		callback: function(r) {
			if (r.message && r.message.success) {
				frm.set_value('weather_condition', r.message.condition);
				frm.set_value('temperature', r.message.temperature);
				frm.set_value('wind_speed', r.message.wind_speed);
				frm.set_value('precipitation', r.message.precipitation);
				frm.set_value('humidity', r.message.humidity);
				frappe.show_alert({
					message: __('Weather data updated'),
					indicator: 'green'
				});
			} else {
				frappe.msgprint(__('Could not fetch weather data. Please enter manually.'));
			}
		}
	});
}

function capture_gps_location(frm) {
	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(
			function(position) {
				frm.set_value('latitude', position.coords.latitude);
				frm.set_value('longitude', position.coords.longitude);
				frm.set_value('location_accuracy', position.coords.accuracy);
				frappe.show_alert({
					message: __('Location captured'),
					indicator: 'green'
				});
			},
			function(error) {
				frappe.msgprint(__('Could not capture location: ') + error.message);
			},
			{
				enableHighAccuracy: true,
				timeout: 10000,
				maximumAge: 0
			}
		);
	} else {
		frappe.msgprint(__('Geolocation is not supported by this browser'));
	}
}
