frappe.ui.form.on('Change Order Request', {
	refresh: function(frm) {
		// Show status indicator
		var status_colors = {
			'Draft': 'gray',
			'Pending': 'orange',
			'Under Review': 'blue',
			'Approved': 'green',
			'Rejected': 'red',
			'Revised': 'purple',
			'Void': 'gray'
		};
		if (frm.doc.status) {
			frm.page.set_indicator(__(frm.doc.status), status_colors[frm.doc.status]);
		}

		// Approval buttons
		if (frm.doc.docstatus === 1 && frm.doc.status === 'Pending') {
			if (frappe.user.has_role('Construction Manager')) {
				frm.add_custom_button(__('Approve'), function() {
					show_approval_dialog(frm);
				}, __('Actions'));

				frm.add_custom_button(__('Reject'), function() {
					frappe.prompt({
						fieldname: 'reason',
						label: __('Rejection Reason'),
						fieldtype: 'Small Text',
						reqd: 1
					}, function(values) {
						frm.call('reject', { reason: values.reason }).then(() => {
							frm.reload_doc();
						});
					}, __('Reject COR'));
				}, __('Actions'));
			}
		}

		// Link to Change Order
		if (frm.doc.change_order) {
			frm.dashboard.add_indicator(
				__('Change Order: ') + frm.doc.change_order,
				'green'
			);
		}
	},

	markup_percent: function(frm) {
		calculate_total(frm);
	}
});

frappe.ui.form.on('Change Order Request Item', {
	quantity: function(frm, cdt, cdn) {
		calculate_item_amount(frm, cdt, cdn);
	},

	unit_cost: function(frm, cdt, cdn) {
		calculate_item_amount(frm, cdt, cdn);
	},

	amount: function(frm) {
		calculate_total(frm);
	},

	items_remove: function(frm) {
		calculate_total(frm);
	}
});

function calculate_item_amount(frm, cdt, cdn) {
	var row = locals[cdt][cdn];
	var amount = flt(row.quantity) * flt(row.unit_cost);
	frappe.model.set_value(cdt, cdn, 'amount', amount);
}

function calculate_total(frm) {
	var subtotal = 0;
	(frm.doc.items || []).forEach(function(item) {
		subtotal += flt(item.amount);
	});
	
	frm.set_value('cost_impact', subtotal);
	var markup = subtotal * (flt(frm.doc.markup_percent) / 100);
	frm.set_value('total_amount', subtotal + markup);
}

function show_approval_dialog(frm) {
	var d = new frappe.ui.Dialog({
		title: __('Approve Change Order Request'),
		fields: [
			{
				fieldname: 'approved_amount',
				label: __('Approved Amount'),
				fieldtype: 'Currency',
				default: frm.doc.total_amount
			},
			{
				fieldname: 'approved_schedule_days',
				label: __('Approved Schedule Days'),
				fieldtype: 'Int',
				default: frm.doc.schedule_impact_days
			}
		],
		primary_action_label: __('Approve'),
		primary_action: function(values) {
			frm.call('approve', {
				approved_amount: values.approved_amount,
				approved_schedule_days: values.approved_schedule_days
			}).then(() => {
				d.hide();
				frm.reload_doc();
				frappe.show_alert({
					message: __('Change Order Request approved'),
					indicator: 'green'
				});
			});
		}
	});
	d.show();
}
