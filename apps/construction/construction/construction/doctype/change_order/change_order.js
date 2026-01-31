frappe.ui.form.on('Change Order', {
	refresh: function(frm) {
		// Show status indicator
		var status_colors = {
			'Draft': 'gray',
			'Pending Execution': 'orange',
			'Executed': 'green',
			'Void': 'red'
		};
		if (frm.doc.status) {
			frm.page.set_indicator(__(frm.doc.status), status_colors[frm.doc.status]);
		}

		// Show contract impact
		if (frm.doc.cost_amount) {
			var sign = frm.doc.cost_amount >= 0 ? '+' : '';
			frm.dashboard.add_indicator(
				__('Contract Impact: ') + sign + format_currency(frm.doc.cost_amount),
				frm.doc.cost_amount >= 0 ? 'orange' : 'green'
			);
		}
	},

	job_site: function(frm) {
		if (frm.doc.job_site) {
			frappe.call({
				method: 'frappe.client.get_value',
				args: {
					doctype: 'Job Site',
					filters: { name: frm.doc.job_site },
					fieldname: ['current_contract_value', 'contract_value']
				},
				callback: function(r) {
					if (r.message) {
						var contract_value = r.message.current_contract_value || r.message.contract_value;
						frm.set_value('previous_contract_value', contract_value);
					}
				}
			});
		}
	},

	cost_amount: function(frm) {
		frm.set_value('new_contract_value', 
			flt(frm.doc.previous_contract_value) + flt(frm.doc.cost_amount));
	}
});
