frappe.ui.form.on('Job Cost Entry', {
	refresh: function(frm) {
		// Show cost breakdown
		if (!frm.is_new() && frm.doc.total_cost) {
			frm.dashboard.add_indicator(
				__('Total: ') + format_currency(frm.doc.total_cost),
				'blue'
			);
		}
	},

	job_site: function(frm) {
		// Clear budget line when job site changes
		frm.set_value('budget_line', '');
		
		// Set filter for budget line
		frm.set_query('budget_line', function() {
			return {
				filters: {
					job_site: frm.doc.job_site
				}
			};
		});
	},

	cost_code: function(frm) {
		if (frm.doc.cost_code) {
			// Get cost code details
			frappe.call({
				method: 'frappe.client.get',
				args: {
					doctype: 'Cost Code',
					name: frm.doc.cost_code
				},
				callback: function(r) {
					if (r.message) {
						frm.set_value('cost_category', r.message.cost_type);
						if (r.message.unit_of_measure) {
							frm.set_value('unit_of_measure', r.message.unit_of_measure);
						}
					}
				}
			});
			
			// Try to find matching budget line
			if (frm.doc.job_site) {
				frappe.call({
					method: 'frappe.client.get_value',
					args: {
						doctype: 'Budget Line',
						filters: {
							job_site: frm.doc.job_site,
							cost_code: frm.doc.cost_code
						},
						fieldname: 'name'
					},
					callback: function(r) {
						if (r.message && r.message.name) {
							frm.set_value('budget_line', r.message.name);
						}
					}
				});
			}
		}
	},

	quantity: function(frm) {
		calculate_total(frm);
	},

	unit_cost: function(frm) {
		calculate_total(frm);
	},

	labor_cost: function(frm) {
		calculate_total(frm);
	},

	material_cost: function(frm) {
		calculate_total(frm);
	},

	equipment_cost: function(frm) {
		calculate_total(frm);
	},

	subcontract_cost: function(frm) {
		calculate_total(frm);
	},

	other_cost: function(frm) {
		calculate_total(frm);
	}
});

function calculate_total(frm) {
	// Calculate from cost components
	var component_total = 
		flt(frm.doc.labor_cost) + 
		flt(frm.doc.material_cost) + 
		flt(frm.doc.equipment_cost) + 
		flt(frm.doc.subcontract_cost) + 
		flt(frm.doc.other_cost);
	
	// Calculate from quantity
	var quantity_total = flt(frm.doc.quantity) * flt(frm.doc.unit_cost);
	
	// Use component total if > 0, otherwise use quantity total
	frm.set_value('total_cost', component_total > 0 ? component_total : quantity_total);
}
