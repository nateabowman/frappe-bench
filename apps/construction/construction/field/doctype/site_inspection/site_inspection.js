frappe.ui.form.on('Site Inspection', {
	refresh: function(frm) {
		// Show result indicator
		var result_colors = {
			'Passed': 'green',
			'Passed with Comments': 'orange',
			'Failed': 'red',
			'Pending': 'gray'
		};
		if (frm.doc.result) {
			frm.page.set_indicator(__(frm.doc.result), result_colors[frm.doc.result]);
		}

		// Show pass rate
		if (frm.doc.total_items > 0) {
			frm.dashboard.add_indicator(
				__('Pass Rate: ') + frm.doc.pass_rate.toFixed(1) + '%',
				frm.doc.pass_rate >= 80 ? 'green' : 'red'
			);
		}
	},

	inspector_signature: function(frm) {
		if (frm.doc.inspector_signature) {
			frm.set_value('signature_date', frappe.datetime.now_datetime());
		}
	}
});

frappe.ui.form.on('Inspection Item', {
	result: function(frm) {
		calculate_results(frm);
	},

	inspection_items_remove: function(frm) {
		calculate_results(frm);
	}
});

function calculate_results(frm) {
	var total = frm.doc.inspection_items ? frm.doc.inspection_items.length : 0;
	var passed = 0;
	var failed = 0;

	(frm.doc.inspection_items || []).forEach(function(item) {
		if (item.result === 'Pass') passed++;
		if (item.result === 'Fail') failed++;
	});

	frm.set_value('total_items', total);
	frm.set_value('passed_items', passed);
	frm.set_value('failed_items', failed);
	frm.set_value('pass_rate', total > 0 ? (passed / total) * 100 : 0);
}
