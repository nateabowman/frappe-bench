frappe.ui.form.on('Cost Code', {
	refresh: function(frm) {
		// Add button to import CSI MasterFormat codes
		if (frappe.user.has_role('System Manager')) {
			frm.add_custom_button(__('Import CSI MasterFormat'), function() {
				frappe.call({
					method: 'construction.construction.doctype.cost_code.cost_code.import_csi_masterformat',
					freeze: true,
					freeze_message: __('Importing CSI MasterFormat codes...'),
					callback: function(r) {
						if (r.message) {
							frappe.msgprint(__('Created {0} cost codes', [r.message.created]));
							frm.reload_doc();
						}
					}
				});
			});
		}

		// Show tree view button
		frm.add_custom_button(__('View Tree'), function() {
			frappe.set_route('Tree', 'Cost Code');
		});
	},

	parent_cost_code: function(frm) {
		if (frm.doc.parent_cost_code) {
			// Generate suggested code based on parent
			frappe.call({
				method: 'frappe.client.get_value',
				args: {
					doctype: 'Cost Code',
					filters: { name: frm.doc.parent_cost_code },
					fieldname: ['cost_code', 'is_group']
				},
				callback: function(r) {
					if (r.message && r.message.is_group) {
						// Suggest next code number
						var parent_code = r.message.cost_code;
						frappe.call({
							method: 'frappe.client.get_count',
							args: {
								doctype: 'Cost Code',
								filters: { parent_cost_code: frm.doc.parent_cost_code }
							},
							callback: function(r) {
								var next_num = (r.message || 0) + 1;
								var suggested = parent_code + '.' + String(next_num).padStart(2, '0');
								frm.set_value('cost_code', suggested);
							}
						});
					}
				}
			});
		}
	}
});

// Tree view configuration
frappe.treeview_settings['Cost Code'] = {
	breadcrumb: 'Construction',
	title: __('Cost Codes'),
	get_tree_root: true,
	root_label: 'Cost Codes',
	get_tree_nodes: 'construction.construction.doctype.cost_code.cost_code.get_child_cost_codes',
	add_tree_node: 'construction.construction.doctype.cost_code.cost_code.add_cost_code',
	filters: [],
	fields: [
		{
			fieldtype: 'Data',
			fieldname: 'cost_code',
			label: __('Cost Code'),
			reqd: 1
		},
		{
			fieldtype: 'Data',
			fieldname: 'cost_code_name',
			label: __('Name'),
			reqd: 1
		},
		{
			fieldtype: 'Check',
			fieldname: 'is_group',
			label: __('Is Group')
		}
	],
	onrender: function(node) {
		if (node.data.is_group) {
			node.$a.find('.tree-label').css('font-weight', '600');
		}
	}
};
