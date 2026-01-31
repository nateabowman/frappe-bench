// Copyright (c) 2024, Nexelya and Contributors
// License: GNU General Public License v3. See license.txt

frappe.ui.form.on("RFI", {
	refresh(frm) {
		// Add construction-specific styling
		nexelya.forms.enhanceRFIForm(frm);
		
		// Add custom buttons or actions if needed
		if (frm.doc.project) {
			frm.add_custom_button(__("View Job Site"), function() {
				frappe.set_route("Form", "Project", frm.doc.project);
			}, __("Actions"));
		}
		
		// Add priority-based styling
		if (frm.doc.priority) {
			const formWrapper = frm.wrapper;
			formWrapper.classList.remove('rfi-priority-high', 'rfi-priority-medium', 'rfi-priority-low');
			formWrapper.classList.add('rfi-priority-' + frm.doc.priority.toLowerCase());
		}
		
		// Add status badge styling
		if (frm.doc.status) {
			const statusField = frm.get_field('status');
			if (statusField && statusField.$wrapper) {
				statusField.$wrapper.find('.control-value').addClass('rfi-status-badge', 'rfi-status-' + frm.doc.status.toLowerCase().replace(' ', '-'));
			}
		}
	},
	
	status(frm) {
		// Auto-set responded_by and responded_date when status changes to Answered
		if (frm.doc.status === "Answered" && !frm.doc.responded_by) {
			frm.set_value("responded_by", frappe.session.user);
			frm.set_value("responded_date", frappe.datetime.get_today());
		}
	},
	
	priority(frm) {
		// Update form styling based on priority
		if (frm.doc.priority) {
			const formWrapper = frm.wrapper;
			formWrapper.classList.remove('rfi-priority-high', 'rfi-priority-medium', 'rfi-priority-low');
			formWrapper.classList.add('rfi-priority-' + frm.doc.priority.toLowerCase());
		}
	}
});

// Enhance RFI form with construction-specific features
if (typeof nexelya === 'undefined' || !nexelya.forms) {
	frappe.provide("nexelya.forms");
}

nexelya.forms.enhanceRFIForm = function(frm) {
	// Add photo upload if not already present
	const questionField = frm.get_field('question');
	if (questionField && questionField.$wrapper) {
		// Add attachment button for photos
		const attachBtn = questionField.$wrapper.find('.btn-attach');
		if (attachBtn.length === 0) {
			const btn = $('<button class="btn btn-sm btn-secondary" type="button"><i class="fa fa-camera"></i> Add Photo</button>');
			btn.on('click', function() {
				// Trigger file upload for images
				const input = $('<input type="file" accept="image/*" style="display:none">');
				input.on('change', function(e) {
					const file = e.target.files[0];
					if (file) {
						// Upload and attach to RFI
						frappe.upload.upload_file(file, null, frm.doctype, frm.doc.name);
					}
				});
				input.click();
			});
			questionField.$wrapper.append(btn);
		}
	}
};

