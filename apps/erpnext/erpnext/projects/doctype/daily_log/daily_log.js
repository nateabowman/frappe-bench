// Copyright (c) 2024, Nexelya and Contributors
// License: GNU General Public License v3. See license.txt

frappe.ui.form.on("Daily Log", {
	refresh(frm) {
		// Add construction-specific styling
		nexelya.forms.enhanceDailyLogForm(frm);
		
		// Add custom buttons or actions if needed
		if (frm.doc.project) {
			frm.add_custom_button(__("View Job Site"), function() {
				frappe.set_route("Form", "Project", frm.doc.project);
			}, __("Actions"));
		}
		
		// Set submitted_by and submitted_date on new records
		if (frm.is_new()) {
			frm.set_value("submitted_by", frappe.session.user);
			frm.set_value("submitted_date", frappe.datetime.now_datetime());
			
			// Set default date to today
			if (!frm.doc.date) {
				frm.set_value("date", frappe.datetime.get_today());
			}
		}
		
		// Add weather widget if date is set
		if (frm.doc.date && frm.doc.project) {
			nexelya.forms.loadWeatherData(frm);
		}
	},
	
	date(frm) {
		// Load weather when date changes
		if (frm.doc.date && frm.doc.project) {
			nexelya.forms.loadWeatherData(frm);
		}
	}
});

// Enhance Daily Log form with construction-specific features
if (typeof nexelya === 'undefined' || !nexelya.forms) {
	frappe.provide("nexelya.forms");
}

nexelya.forms.enhanceDailyLogForm = function(frm) {
	// Add photo gallery section
	const workPerformedField = frm.get_field('work_performed');
	if (workPerformedField && workPerformedField.$wrapper) {
		// Add photo upload button
		const photoBtn = $('<button class="btn btn-sm btn-primary" type="button" style="margin-top: var(--spacing-sm);"><i class="fa fa-camera"></i> Add Photos</button>');
		photoBtn.on('click', function() {
			const input = $('<input type="file" accept="image/*" multiple style="display:none">');
			input.on('change', function(e) {
				Array.from(e.target.files).forEach(file => {
					frappe.upload.upload_file(file, null, frm.doctype, frm.doc.name);
				});
			});
			input.click();
		});
		workPerformedField.$wrapper.after(photoBtn);
	}
	
	// Add location capture button
	const locationField = frm.get_field('location');
	if (locationField && locationField.$wrapper && navigator.geolocation) {
		const locationBtn = $('<button class="btn btn-sm btn-secondary location-button" type="button" style="margin-left: var(--spacing-sm);"><i class="fa fa-map-marker"></i> Get Location</button>');
		locationBtn.on('click', function() {
			navigator.geolocation.getCurrentPosition(
				position => {
					const lat = position.coords.latitude;
					const lng = position.coords.longitude;
					frm.set_value('location', `${lat}, ${lng}`);
					frappe.show_alert({ message: 'Location captured', indicator: 'green' });
				},
				error => {
					frappe.show_alert({ message: 'Could not get location: ' + error.message, indicator: 'red' });
				}
			);
		});
		locationField.$wrapper.find('.control-input-wrapper').append(locationBtn);
	}
};

// Load weather data for date and project location
nexelya.forms.loadWeatherData = function(frm) {
	// This would integrate with a weather API
	// For now, just add a placeholder for weather widget
	const weatherSection = frm.dashboard?.add_section(
		__("Weather"),
		[
			{
				label: __("Temperature"),
				value: "N/A",
				indicator: "blue"
			},
			{
				label: __("Conditions"),
				value: "N/A",
				indicator: "blue"
			}
		]
	);
};

