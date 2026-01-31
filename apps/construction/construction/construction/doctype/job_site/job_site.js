frappe.ui.form.on('Job Site', {
	refresh: function(frm) {
		// Add custom buttons
		if (!frm.is_new()) {
			frm.add_custom_button(__('Daily Log'), function() {
				frappe.new_doc('Daily Field Report', {
					job_site: frm.doc.name
				});
			}, __('Create'));

			frm.add_custom_button(__('Punch List'), function() {
				frappe.new_doc('Punch List', {
					job_site: frm.doc.name
				});
			}, __('Create'));

			frm.add_custom_button(__('RFI'), function() {
				frappe.new_doc('RFI', {
					project: frm.doc.project
				});
			}, __('Create'));

			frm.add_custom_button(__('Budget Line'), function() {
				frappe.new_doc('Budget Line', {
					job_site: frm.doc.name
				});
			}, __('Create'));

			frm.add_custom_button(__('Recalculate Costs'), function() {
				frappe.call({
					method: 'construction.construction.doctype.job_site.job_site.update_job_site_costs',
					args: { job_site: frm.doc.name },
					freeze: true,
					freeze_message: __('Recalculating costs...'),
					callback: function(r) {
						if (r.message) {
							frm.reload_doc();
							frappe.show_alert({
								message: __('Costs updated successfully'),
								indicator: 'green'
							});
						}
					}
				});
			}, __('Actions'));

			// Show dashboard
			frm.dashboard.add_indicator(__('Budget: ') + format_currency(frm.doc.current_budget), 
				frm.doc.budget_variance >= 0 ? 'green' : 'red');
			frm.dashboard.add_indicator(__('CPI: ') + (frm.doc.cpi || 1).toFixed(2), 
				frm.doc.cpi >= 1 ? 'green' : frm.doc.cpi >= 0.9 ? 'orange' : 'red');
			frm.dashboard.add_indicator(__('SPI: ') + (frm.doc.spi || 1).toFixed(2), 
				frm.doc.spi >= 1 ? 'green' : frm.doc.spi >= 0.9 ? 'orange' : 'red');
		}

		// Update map if coordinates are available
		if (frm.doc.latitude && frm.doc.longitude) {
			frm.fields_dict.site_map_html.$wrapper.html(`
				<div style="height: 200px; background: #f5f5f5; border-radius: 8px; display: flex; align-items: center; justify-content: center;">
					<a href="https://www.google.com/maps?q=${frm.doc.latitude},${frm.doc.longitude}" target="_blank" class="btn btn-default btn-sm">
						<i class="fa fa-map-marker"></i> View on Google Maps
					</a>
				</div>
			`);
		}

		// Status-based form styling
		if (frm.doc.status === 'Active') {
			frm.page.set_indicator(__('Active'), 'green');
		} else if (frm.doc.status === 'On Hold') {
			frm.page.set_indicator(__('On Hold'), 'orange');
		} else if (frm.doc.status === 'Completed') {
			frm.page.set_indicator(__('Completed'), 'blue');
		}
	},

	customer: function(frm) {
		if (frm.doc.customer) {
			frappe.call({
				method: 'frappe.client.get_value',
				args: {
					doctype: 'Customer',
					filters: { name: frm.doc.customer },
					fieldname: ['customer_name', 'customer_primary_contact', 'customer_primary_address']
				},
				callback: function(r) {
					if (r.message) {
						frm.set_value('customer_name', r.message.customer_name);
						if (r.message.customer_primary_contact) {
							frm.set_value('customer_contact', r.message.customer_primary_contact);
						}
						if (r.message.customer_primary_address) {
							frm.set_value('customer_address', r.message.customer_primary_address);
						}
					}
				}
			});
		}
	},

	contract_value: function(frm) {
		calculate_contract(frm);
	},

	approved_change_orders: function(frm) {
		calculate_contract(frm);
	},

	original_budget: function(frm) {
		calculate_budget(frm);
	},

	site_address: function(frm) {
		// Geocode address if possible
		if (frm.doc.site_address && frm.doc.city && frm.doc.state) {
			geocode_address(frm);
		}
	},

	status: function(frm) {
		// Auto-set dates based on status
		if (frm.doc.status === 'Active' && !frm.doc.actual_start_date) {
			frm.set_value('actual_start_date', frappe.datetime.get_today());
		}
		if (frm.doc.status === 'Completed' && !frm.doc.actual_end_date) {
			frm.set_value('actual_end_date', frappe.datetime.get_today());
			frm.set_value('percent_complete', 100);
		}
	}
});

function calculate_contract(frm) {
	frm.set_value('current_contract_value', 
		flt(frm.doc.contract_value) + flt(frm.doc.approved_change_orders));
}

function calculate_budget(frm) {
	frm.set_value('current_budget', 
		flt(frm.doc.original_budget) + flt(frm.doc.approved_changes));
	
	var variance = flt(frm.doc.current_budget) - flt(frm.doc.actual_cost);
	frm.set_value('budget_variance', variance);
	
	if (frm.doc.current_budget) {
		frm.set_value('budget_variance_percent', (variance / frm.doc.current_budget) * 100);
	}
}

function geocode_address(frm) {
	// Simple geocoding using Nominatim (free)
	var address = encodeURIComponent(
		frm.doc.site_address + ', ' + frm.doc.city + ', ' + frm.doc.state + 
		(frm.doc.zip_code ? ' ' + frm.doc.zip_code : '')
	);
	
	fetch(`https://nominatim.openstreetmap.org/search?q=${address}&format=json&limit=1`)
		.then(response => response.json())
		.then(data => {
			if (data && data.length > 0) {
				frm.set_value('latitude', parseFloat(data[0].lat));
				frm.set_value('longitude', parseFloat(data[0].lon));
				frappe.show_alert({
					message: __('Location coordinates updated'),
					indicator: 'green'
				});
			}
		})
		.catch(err => {
			console.log('Geocoding error:', err);
		});
}
