frappe.ui.form.on('Budget Line', {
	refresh: function(frm) {
		if (!frm.is_new()) {
			// Add recalculate button
			frm.add_custom_button(__('Recalculate Costs'), function() {
				frappe.call({
					method: 'construction.construction.doctype.budget_line.budget_line.recalculate_budget_line',
					args: { budget_line: frm.doc.name },
					freeze: true,
					freeze_message: __('Recalculating...'),
					callback: function(r) {
						if (r.message) {
							frm.reload_doc();
							frappe.show_alert({
								message: __('Costs recalculated'),
								indicator: 'green'
							});
						}
					}
				});
			});

			// Add cost entry button
			frm.add_custom_button(__('Add Cost Entry'), function() {
				frappe.new_doc('Job Cost Entry', {
					job_site: frm.doc.job_site,
					budget_line: frm.doc.name,
					cost_code: frm.doc.cost_code
				});
			});

			// Show variance indicator
			var variance_color = frm.doc.variance >= 0 ? 'green' : 'red';
			var variance_label = frm.doc.variance >= 0 ? 'Under Budget' : 'Over Budget';
			frm.dashboard.add_indicator(
				__(variance_label) + ': ' + format_currency(Math.abs(frm.doc.variance)),
				variance_color
			);
		}
	},

	cost_code: function(frm) {
		if (frm.doc.cost_code) {
			frappe.call({
				method: 'frappe.client.get',
				args: {
					doctype: 'Cost Code',
					name: frm.doc.cost_code
				},
				callback: function(r) {
					if (r.message) {
						frm.set_value('description', r.message.cost_code_name);
						frm.set_value('cost_type', r.message.cost_type);
						if (r.message.unit_of_measure) {
							frm.set_value('unit_of_measure', r.message.unit_of_measure);
						}
						if (r.message.default_unit_cost) {
							frm.set_value('unit_cost', r.message.default_unit_cost);
						}
					}
				}
			});
		}
	},

	original_budget: function(frm) {
		calculate_budget(frm);
	},

	approved_changes: function(frm) {
		calculate_budget(frm);
	},

	quantity: function(frm) {
		calculate_from_quantity(frm);
	},

	unit_cost: function(frm) {
		calculate_from_quantity(frm);
	},

	percent_complete: function(frm) {
		calculate_earned_value(frm);
	},

	estimate_to_complete: function(frm) {
		calculate_eac(frm);
	}
});

function calculate_budget(frm) {
	frm.set_value('current_budget', 
		flt(frm.doc.original_budget) + flt(frm.doc.approved_changes));
	calculate_variance(frm);
	calculate_earned_value(frm);
}

function calculate_from_quantity(frm) {
	if (frm.doc.quantity && frm.doc.unit_cost) {
		var budget = flt(frm.doc.quantity) * flt(frm.doc.unit_cost);
		frm.set_value('original_budget', budget);
	}
}

function calculate_variance(frm) {
	var eac = flt(frm.doc.actual_cost) + flt(frm.doc.estimate_to_complete);
	frm.set_value('estimate_at_completion', eac);
	
	var variance = flt(frm.doc.current_budget) - eac;
	frm.set_value('variance', variance);
	
	if (frm.doc.current_budget) {
		frm.set_value('variance_percent', (variance / frm.doc.current_budget) * 100);
	}
}

function calculate_earned_value(frm) {
	var ev = flt(frm.doc.current_budget) * (flt(frm.doc.percent_complete) / 100);
	frm.set_value('earned_value', ev);
}

function calculate_eac(frm) {
	var eac = flt(frm.doc.actual_cost) + flt(frm.doc.estimate_to_complete);
	frm.set_value('estimate_at_completion', eac);
	calculate_variance(frm);
}
