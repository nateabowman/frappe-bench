frappe.ui.form.on('Gantt Schedule', {
	refresh: function(frm) {
		if (!frm.is_new()) {
			// Add Gantt view button
			frm.add_custom_button(__('View Gantt Chart'), function() {
				show_gantt_chart(frm);
			});

			// Add recalculate button
			frm.add_custom_button(__('Recalculate CPM'), function() {
				frm.call('calculate_critical_path').then(() => {
					frm.reload_doc();
					frappe.show_alert({
						message: __('Critical path recalculated'),
						indicator: 'green'
					});
				});
			});

			// Add baseline button
			if (!frm.doc.is_baseline) {
				frm.add_custom_button(__('Set as Baseline'), function() {
					frappe.confirm(
						__('Set this schedule as the baseline? This will archive any existing baseline.'),
						function() {
							frm.set_value('is_baseline', 1);
							frm.set_value('status', 'Baseline');
							frm.save();
						}
					);
				});
			}

			// Show dashboard indicators
			frm.dashboard.add_indicator(
				__('Progress: ') + frm.doc.percent_complete.toFixed(1) + '%',
				frm.doc.percent_complete >= 100 ? 'green' : frm.doc.percent_complete >= 50 ? 'blue' : 'orange'
			);

			if (frm.doc.use_cpm) {
				frm.dashboard.add_indicator(
					__('Critical Path: ') + frm.doc.critical_path_length + ' activities',
					'red'
				);
			}
		}
	},

	job_site: function(frm) {
		if (frm.doc.job_site) {
			frappe.call({
				method: 'frappe.client.get_value',
				args: {
					doctype: 'Job Site',
					filters: { name: frm.doc.job_site },
					fieldname: ['planned_start_date', 'planned_end_date', 'job_name']
				},
				callback: function(r) {
					if (r.message) {
						if (r.message.planned_start_date) {
							frm.set_value('start_date', r.message.planned_start_date);
						}
						if (r.message.planned_end_date) {
							frm.set_value('end_date', r.message.planned_end_date);
						}
						if (!frm.doc.schedule_name) {
							frm.set_value('schedule_name', r.message.job_name + ' - Master Schedule');
						}
					}
				}
			});
		}
	}
});

frappe.ui.form.on('Schedule Activity', {
	duration: function(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		if (row.start_date && row.duration) {
			var end_date = frappe.datetime.add_days(row.start_date, row.duration - 1);
			frappe.model.set_value(cdt, cdn, 'end_date', end_date);
		}
	},

	start_date: function(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		if (row.start_date && row.duration) {
			var end_date = frappe.datetime.add_days(row.start_date, row.duration - 1);
			frappe.model.set_value(cdt, cdn, 'end_date', end_date);
		}
	},

	end_date: function(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		if (row.start_date && row.end_date) {
			var duration = frappe.datetime.get_diff(row.end_date, row.start_date) + 1;
			frappe.model.set_value(cdt, cdn, 'duration', duration);
		}
	}
});

function show_gantt_chart(frm) {
	frappe.call({
		method: 'construction.scheduling.doctype.gantt_schedule.gantt_schedule.get_gantt_data',
		args: { schedule_name: frm.doc.name },
		callback: function(r) {
			if (r.message && r.message.tasks.length > 0) {
				var dialog = new frappe.ui.Dialog({
					title: __('Gantt Chart: ') + frm.doc.schedule_name,
					size: 'extra-large',
					fields: [
						{
							fieldname: 'gantt_container',
							fieldtype: 'HTML'
						}
					]
				});

				dialog.show();

				// Render Gantt chart
				setTimeout(function() {
					var container = dialog.fields_dict.gantt_container.$wrapper;
					container.html('<div id="gantt-chart" style="width: 100%; overflow-x: auto;"></div>');
					
					if (typeof Gantt !== 'undefined') {
						var tasks = r.message.tasks.map(function(t) {
							return {
								id: t.id,
								name: t.name,
								start: t.start,
								end: t.end,
								progress: t.progress,
								dependencies: t.dependencies,
								custom_class: t.is_critical ? 'bar-critical' : (t.is_milestone ? 'bar-milestone' : '')
							};
						});

						new Gantt('#gantt-chart', tasks, {
							view_modes: ['Day', 'Week', 'Month'],
							view_mode: 'Week',
							date_format: 'YYYY-MM-DD',
							on_click: function(task) {
								frappe.msgprint({
									title: task.name,
									message: `Start: ${task.start}<br>End: ${task.end}<br>Progress: ${task.progress}%`,
									indicator: task.custom_class === 'bar-critical' ? 'red' : 'blue'
								});
							},
							on_date_change: function(task, start, end) {
								frappe.call({
									method: 'construction.scheduling.doctype.gantt_schedule.gantt_schedule.update_activity_dates',
									args: {
										schedule_name: frm.doc.name,
										activity_id: task.id,
										start_date: start,
										end_date: end
									},
									callback: function() {
										frappe.show_alert({
											message: __('Activity dates updated'),
											indicator: 'green'
										});
									}
								});
							}
						});
					} else {
						container.html('<p class="text-muted">' + __('Gantt library not loaded. Please include frappe-gantt.') + '</p>');
					}
				}, 100);
			} else {
				frappe.msgprint(__('No activities to display'));
			}
		}
	});
}
