frappe.ui.form.on('Punch List', {
	refresh: function(frm) {
		// Show completion progress
		if (frm.doc.total_items > 0) {
			frm.dashboard.add_indicator(
				__('Progress: ') + frm.doc.completed_items + '/' + frm.doc.total_items,
				frm.doc.percent_complete === 100 ? 'green' : 'blue'
			);
		}

		// Add bulk actions
		if (!frm.is_new() && frm.doc.items && frm.doc.items.length > 0) {
			frm.add_custom_button(__('Mark All Complete'), function() {
				frappe.confirm(
					__('Mark all items as completed?'),
					function() {
						var items = frm.doc.items.map(i => i.name);
						frappe.call({
							method: 'construction.field.doctype.punch_list.punch_list.batch_complete_items',
							args: { items: items },
							freeze: true,
							callback: function(r) {
								if (r.message) {
									frm.reload_doc();
									frappe.show_alert({
										message: __('Completed {0} items', [r.message.completed]),
										indicator: 'green'
									});
								}
							}
						});
					}
				);
			}, __('Actions'));

			frm.add_custom_button(__('Print List'), function() {
				frappe.set_route('print', 'Punch List', frm.doc.name);
			}, __('Actions'));
		}

		// Priority indicator
		var priority_colors = {
			'Low': 'blue',
			'Medium': 'orange',
			'High': 'red',
			'Urgent': 'red'
		};
		if (frm.doc.priority) {
			frm.page.set_indicator(__(frm.doc.priority), priority_colors[frm.doc.priority]);
		}
	},

	assigned_to_type: function(frm) {
		if (frm.doc.assigned_to_type !== 'Subcontractor') {
			frm.set_value('assigned_subcontractor', '');
		}
		if (frm.doc.assigned_to_type !== 'Employee') {
			frm.set_value('assigned_employee', '');
		}
	}
});

frappe.ui.form.on('Punch List Item', {
	status: function(frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		if (row.status === 'Completed' && !row.completed_date) {
			frappe.model.set_value(cdt, cdn, 'completed_date', frappe.datetime.get_today());
			frappe.model.set_value(cdt, cdn, 'completed_by', frappe.session.user);
		}
		calculate_completion(frm);
	},

	items_remove: function(frm) {
		calculate_completion(frm);
	}
});

function calculate_completion(frm) {
	var total = frm.doc.items ? frm.doc.items.length : 0;
	var completed = 0;
	
	(frm.doc.items || []).forEach(function(item) {
		if (item.status === 'Completed') {
			completed++;
		}
	});

	frm.set_value('total_items', total);
	frm.set_value('completed_items', completed);
	frm.set_value('percent_complete', total > 0 ? (completed / total) * 100 : 0);
}
