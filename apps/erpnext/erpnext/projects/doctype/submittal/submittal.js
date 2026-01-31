// Copyright (c) 2024, Nexelya and Contributors
// License: GNU General Public License v3. See license.txt

frappe.ui.form.on("Submittal", {
	refresh(frm) {
		// Add construction-specific styling
		nexelya.forms.enhanceSubmittalForm(frm);
		
		// Add custom buttons or actions if needed
		if (frm.doc.project) {
			frm.add_custom_button(__("View Job Site"), function() {
				frappe.set_route("Form", "Project", frm.doc.project);
			}, __("Actions"));
		}
		
		// Add timeline visualization
		if (frm.doc.status) {
			nexelya.forms.showSubmittalTimeline(frm);
		}
	},
	
	status(frm) {
		// Auto-set reviewed_by and reviewed_date when status changes from Pending
		if (frm.doc.status !== "Pending" && !frm.doc.reviewed_by) {
			frm.set_value("reviewed_by", frappe.session.user);
			frm.set_value("reviewed_date", frappe.datetime.get_today());
		}
		
		// Update timeline
		nexelya.forms.showSubmittalTimeline(frm);
	}
});

// Enhance Submittal form
if (typeof nexelya === 'undefined' || !nexelya.forms) {
	frappe.provide("nexelya.forms");
}

nexelya.forms.enhanceSubmittalForm = function(frm) {
	// Add document upload section
	const descriptionField = frm.get_field('description');
	if (descriptionField && descriptionField.$wrapper) {
		const uploadBtn = $('<button class="btn btn-sm btn-primary" type="button" style="margin-top: var(--spacing-sm);"><i class="fa fa-upload"></i> Upload Documents</button>');
		uploadBtn.on('click', function() {
			const input = $('<input type="file" multiple style="display:none">');
			input.on('change', function(e) {
				Array.from(e.target.files).forEach(file => {
					frappe.upload.upload_file(file, null, frm.doctype, frm.doc.name);
				});
			});
			input.click();
		});
		descriptionField.$wrapper.after(uploadBtn);
	}
};

// Show submittal timeline
nexelya.forms.showSubmittalTimeline = function(frm) {
	if (!frm.dashboard) return;
	
	const statuses = ['Pending', 'Under Review', 'Approved', 'Rejected'];
	const currentIndex = statuses.indexOf(frm.doc.status);
	
	const timelineHtml = `
		<div class="submittal-timeline" style="margin: var(--spacing-lg) 0;">
			${statuses.map((status, index) => `
				<div class="submittal-timeline-item ${index <= currentIndex ? 'completed' : ''} ${index === currentIndex ? 'pending' : ''}" style="padding-bottom: var(--spacing-md);">
					<div style="font-weight: var(--font-weight-semibold); margin-bottom: var(--spacing-xs);">${status}</div>
					${index === currentIndex && frm.doc.reviewed_date ? `<div style="font-size: var(--font-size-sm); color: var(--text-tertiary);">${frm.doc.reviewed_date}</div>` : ''}
				</div>
			`).join('')}
		</div>
	`;
	
	// Add timeline to dashboard if not already present
	if (!frm.dashboard.$wrapper.find('.submittal-timeline').length) {
		frm.dashboard.add_section(__("Status Timeline"), timelineHtml);
	}
};

