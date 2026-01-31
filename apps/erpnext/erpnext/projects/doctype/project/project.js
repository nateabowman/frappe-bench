// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt
frappe.ui.form.on("Project", {
	setup(frm) {
		frm.make_methods = {
			Timesheet: () => {
				open_form(frm, "Timesheet", "Timesheet Detail", "time_logs");
			},
			"Purchase Order": () => {
				open_form(frm, "Purchase Order", "Purchase Order Item", "items");
			},
			"Purchase Receipt": () => {
				open_form(frm, "Purchase Receipt", "Purchase Receipt Item", "items");
			},
			"Purchase Invoice": () => {
				open_form(frm, "Purchase Invoice", "Purchase Invoice Item", "items");
			},
			RFI: () => {
				frappe.model.with_doctype("RFI", () => {
					let new_doc = frappe.model.get_new_doc("RFI");
					new_doc.project = frm.doc.name;
					frappe.set_route("Form", "RFI", new_doc.name);
				});
			},
			Submittal: () => {
				frappe.model.with_doctype("Submittal", () => {
					let new_doc = frappe.model.get_new_doc("Submittal");
					new_doc.project = frm.doc.name;
					frappe.set_route("Form", "Submittal", new_doc.name);
				});
			},
			"Daily Log": () => {
				frappe.model.with_doctype("Daily Log", () => {
					let new_doc = frappe.model.get_new_doc("Daily Log");
					new_doc.project = frm.doc.name;
					frappe.set_route("Form", "Daily Log", new_doc.name);
				});
			},
		};
	},
	onload: function (frm) {
		const so = frm.get_docfield("sales_order");
		so.get_route_options_for_new_doc = () => {
			if (frm.is_new()) return {};
			return {
				customer: frm.doc.customer,
				project_name: frm.doc.name,
			};
		};

		frm.set_query("user", "users", function () {
			return {
				query: "erpnext.projects.doctype.project.project.get_users_for_project",
			};
		});

		frm.set_query("department", function (doc) {
			return {
				filters: {
					company: doc.company,
				},
			};
		});

		// sales order
		frm.set_query("sales_order", function () {
			var filters = {
				project: ["in", frm.doc.__islocal ? [""] : [frm.doc.name, ""]],
				company: frm.doc.company,
			};

			if (frm.doc.customer) {
				filters["customer"] = frm.doc.customer;
			}

			return {
				filters: filters,
			};
		});

		frm.set_query("cost_center", () => {
			return {
				filters: {
					company: frm.doc.company,
				},
			};
		});
	},

	refresh: function (frm) {
		if (frm.doc.__islocal) {
			frm.web_link && frm.web_link.remove();
		} else {
			frm.add_web_link("/projects?project=" + encodeURIComponent(frm.doc.name));

			frm.trigger("show_dashboard");
			frm.trigger("show_job_costing_dashboard");
		}
		frm.trigger("set_custom_buttons");
		frm.trigger("check_feature_access");
	},
	
	show_job_costing_dashboard: function(frm) {
		// Check if real-time job costing feature is enabled
		if (!frm.doc.company) return;
		
		frappe.call({
			method: "erpnext.projects.doctype.nexelya_plan_settings.nexelya_plan_settings.check_feature_access",
			args: {
				feature_name: "real_time_job_costing",
				company: frm.doc.company
			},
			callback: function(r) {
				if (r.message) {
					// Feature is enabled, show job costing dashboard
					frappe.call({
						method: "erpnext.projects.doctype.project.project_dashboard.get_job_costing_dashboard",
						args: {
							project: frm.doc.name
						},
						callback: function(costing_data) {
							if (costing_data.message && frm.dashboard) {
								const data = costing_data.message;
								const currency = frm.doc.currency || frappe.defaults.get_default("currency");
								
								// Enhanced dashboard with construction styling
								frm.dashboard.add_section(
									__("Real-Time Job Costing"),
									[
										{
											label: __("Estimated Cost"),
											value: frappe.format(data.estimated_cost, {fieldtype: "Currency", options: currency}),
											indicator: "blue"
										},
										{
											label: __("Actual Cost"),
											value: frappe.format(data.total_actual_cost, {fieldtype: "Currency", options: currency}),
											indicator: "green"
										},
										{
											label: __("Committed Cost"),
											value: frappe.format(data.total_committed_cost, {fieldtype: "Currency", options: currency}),
											indicator: data.cost_variance > 0 ? "red" : "green"
										},
										{
											label: __("Cost Variance"),
											value: frappe.format(data.cost_variance, {fieldtype: "Currency", options: currency}) + 
												" (" + data.cost_variance_percent.toFixed(1) + "%)",
											indicator: data.cost_variance > 0 ? "red" : "green"
										}
									]
								);
							}
						}
					});
				}
			}
		});
	},
	
	check_feature_access: function(frm) {
		// Hide/show features based on plan
		if (!frm.doc.company) return;
		
		frappe.call({
			method: "erpnext.projects.doctype.nexelya_plan_settings.nexelya_plan_settings.get_plan_settings",
			args: {
				company: frm.doc.company
			},
			callback: function(r) {
				if (r.message) {
					const plan = r.message.plan_type;
					
					// Hide construction management features for Core plan
					if (plan === "Core") {
						// These features are only in Growth+
						frm.set_df_property("committed_purchase_cost", "hidden", 1);
						frm.set_df_property("committed_sales_amount", "hidden", 1);
						frm.set_df_property("total_committed_cost", "hidden", 1);
						frm.set_df_property("total_actual_cost", "hidden", 1);
					}
				}
			}
		});
	},

	set_custom_buttons: function (frm) {
		if (!frm.is_new()) {
			frm.add_custom_button(
				__("Duplicate Project with Tasks"),
				() => {
					frm.events.create_duplicate(frm);
				},
				__("Actions")
			);

			frm.add_custom_button(
				__("Update Total Purchase Cost"),
				() => {
					frm.events.update_total_purchase_cost(frm);
				},
				__("Actions")
			);

			frm.trigger("set_project_status_button");

			if (frappe.model.can_read("Task")) {
				frm.add_custom_button(
					__("Gantt Chart"),
					function () {
						frappe.route_options = {
							project: frm.doc.name,
						};
						frappe.set_route("List", "Task", "Gantt");
					},
					__("View")
				);

				frm.add_custom_button(
					__("Kanban Board"),
					() => {
						frappe
							.call(
								"erpnext.projects.doctype.project.project.create_kanban_board_if_not_exists",
								{
									project: frm.doc.name,
								}
							)
							.then(() => {
								frappe.set_route("List", "Task", "Kanban", frm.doc.project_name);
							});
					},
					__("View")
				);
			}
		}
	},

	update_total_purchase_cost: function (frm) {
		frappe.call({
			method: "erpnext.projects.doctype.project.project.recalculate_project_total_purchase_cost",
			args: { project: frm.doc.name },
			freeze: true,
			freeze_message: __("Recalculating Purchase Cost against this Project..."),
			callback: function (r) {
				if (r && !r.exc) {
					frappe.msgprint(__("Total Purchase Cost has been updated"));
					frm.refresh();
				}
			},
		});
	},

	set_project_status_button: function (frm) {
		frm.add_custom_button(
			__("Set Project Status"),
			() => frm.events.get_project_status_dialog(frm).show(),
			__("Actions")
		);
	},

	get_project_status_dialog: function (frm) {
		const dialog = new frappe.ui.Dialog({
			title: __("Set Project Status"),
			fields: [
				{
					fieldname: "status",
					fieldtype: "Select",
					label: "Status",
					reqd: 1,
					options: "Completed\nCancelled",
				},
			],
			primary_action: function () {
				frm.events.set_status(frm, dialog.get_values().status);
				dialog.hide();
			},
			primary_action_label: __("Set Project Status"),
		});
		return dialog;
	},

	create_duplicate: function (frm) {
		return new Promise((resolve) => {
			frappe.prompt("Project Name", (data) => {
				frappe
					.xcall("erpnext.projects.doctype.project.project.create_duplicate_project", {
						prev_doc: frm.doc,
						project_name: data.value,
					})
					.then(() => {
						frappe.set_route("Form", "Project", data.value);
						frappe.show_alert(__("Duplicate project has been created"));
					});
				resolve();
			});
		});
	},

	set_status: function (frm, status) {
		frappe.confirm(__("Set Project and all Tasks to status {0}?", [__(status).bold()]), () => {
			frappe
				.xcall("erpnext.projects.doctype.project.project.set_project_status", {
					project: frm.doc.name,
					status: status,
				})
				.then(() => {
					frm.reload_doc();
				});
		});
	},

	collect_progress: function (frm) {
		if (frm.doc.collect_progress && !frm.doc.subject) {
			frm.set_value("subject", __("For project {0}, update your status", [frm.doc.name]));
		}
	},
});

function open_form(frm, doctype, child_doctype, parentfield) {
	frappe.model.with_doctype(doctype, () => {
		let new_doc = frappe.model.get_new_doc(doctype);

		// add a new row and set the project
		let new_child_doc = frappe.model.get_new_doc(child_doctype);
		new_child_doc.project = frm.doc.name;
		new_child_doc.parent = new_doc.name;
		new_child_doc.parentfield = parentfield;
		new_child_doc.parenttype = doctype;
		new_doc[parentfield] = [new_child_doc];
		new_doc.project = frm.doc.name;

		frappe.ui.form.make_quick_entry(doctype, null, null, new_doc);
	});
}
