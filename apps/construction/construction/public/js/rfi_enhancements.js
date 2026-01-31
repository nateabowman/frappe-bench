// RFI Enhancements for Construction
frappe.ui.form.on('RFI', {
	refresh: function(frm) {
		// Add ball-in-court tracking indicator
		if (frm.doc.ball_in_court) {
			var color = {
				'Contractor': 'blue',
				'Architect': 'orange',
				'Engineer': 'purple',
				'Owner': 'green',
				'Subcontractor': 'gray'
			}[frm.doc.ball_in_court] || 'blue';
			
			frm.dashboard.add_indicator(__('Ball in Court: ') + frm.doc.ball_in_court, color);
		}

		// Show overdue warning
		if (frm.doc.is_overdue) {
			frm.dashboard.add_indicator(__('OVERDUE'), 'red');
		}

		// Show days open
		if (frm.doc.status === 'Open' && frm.doc.days_open) {
			frm.dashboard.add_indicator(__('Days Open: ') + frm.doc.days_open, 
				frm.doc.days_open > 7 ? 'orange' : 'blue');
		}

		// Quick response button
		if (frm.doc.status === 'Open' && !frm.is_new()) {
			frm.add_custom_button(__('Add Response'), function() {
				frappe.prompt([
					{
						fieldname: 'response',
						label: __('Response'),
						fieldtype: 'Text Editor',
						reqd: 1
					},
					{
						fieldname: 'ball_in_court',
						label: __('Ball in Court'),
						fieldtype: 'Select',
						options: 'Contractor\nArchitect\nEngineer\nOwner\nSubcontractor'
					}
				], function(values) {
					frm.set_value('response', values.response);
					frm.set_value('responded_by', frappe.session.user);
					frm.set_value('responded_date', frappe.datetime.get_today());
					if (values.ball_in_court) {
						frm.set_value('ball_in_court', values.ball_in_court);
					}
					frm.save();
				}, __('Add RFI Response'));
			});
		}

		// Create Change Order button
		if (frm.doc.status === 'Closed' && frm.doc.cost_impact) {
			frm.add_custom_button(__('Create Change Order Request'), function() {
				frappe.new_doc('Change Order Request', {
					job_site: frappe.db.get_value('Job Site', {'project': frm.doc.project}, 'name'),
					subject: 'RFI ' + frm.doc.name + ': ' + frm.doc.subject,
					description: frm.doc.response,
					cost_impact: frm.doc.cost_impact,
					schedule_impact_days: frm.doc.schedule_impact_days,
					related_rfi: frm.doc.name,
					reason_for_change: 'Design Change'
				});
			}, __('Actions'));
		}
	},

	validate: function(frm) {
		// Calculate days open
		if (frm.doc.requested_date) {
			var today = frappe.datetime.get_today();
			frm.doc.days_open = frappe.datetime.get_diff(today, frm.doc.requested_date);
		}

		// Check if overdue
		if (frm.doc.due_date && frm.doc.status === 'Open') {
			var today = frappe.datetime.get_today();
			frm.doc.is_overdue = frappe.datetime.get_diff(frm.doc.due_date, today) < 0;
		}
	},

	status: function(frm) {
		// Update ball in court based on status
		if (frm.doc.status === 'Answered' && !frm.doc.ball_in_court) {
			frm.set_value('ball_in_court', 'Contractor');
		}
	}
});

// Submittal Enhancements
frappe.ui.form.on('Submittal', {
	refresh: function(frm) {
		// Show review status indicator
		if (frm.doc.review_status) {
			var colors = {
				'Approved': 'green',
				'Approved as Noted': 'blue',
				'Revise and Resubmit': 'orange',
				'Rejected': 'red',
				'For Information Only': 'gray'
			};
			frm.dashboard.add_indicator(__(frm.doc.review_status), colors[frm.doc.review_status]);
		}

		// Resubmit button
		if (frm.doc.review_status === 'Revise and Resubmit' && !frm.is_new()) {
			frm.add_custom_button(__('Create Resubmittal'), function() {
				frappe.call({
					method: 'frappe.client.get',
					args: { doctype: 'Submittal', name: frm.doc.name },
					callback: function(r) {
						if (r.message) {
							var doc = frappe.model.copy_doc(r.message);
							doc.resubmittal_count = (frm.doc.resubmittal_count || 0) + 1;
							doc.review_status = '';
							doc.reviewer = '';
							doc.review_date = '';
							frappe.set_route('Form', 'Submittal', doc.name);
						}
					}
				});
			});
		}
	}
});
