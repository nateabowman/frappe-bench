frappe.pages['construction-dashboard'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Construction Dashboard',
		single_column: true
	});

	// Add filters
	page.add_field({
		fieldname: 'job_site',
		label: __('Job Site'),
		fieldtype: 'Link',
		options: 'Job Site',
		change: function() {
			render_dashboard(page);
		}
	});

	page.add_field({
		fieldname: 'view_type',
		label: __('View'),
		fieldtype: 'Select',
		options: 'Project\nExecutive',
		default: 'Project',
		change: function() {
			render_dashboard(page);
		}
	});

	// Initial render
	render_dashboard(page);
};

function render_dashboard(page) {
	var view_type = page.fields_dict.view_type.get_value() || 'Project';
	var job_site = page.fields_dict.job_site.get_value();

	$(page.body).empty();

	if (view_type === 'Executive') {
		render_executive_dashboard(page);
	} else if (job_site) {
		render_project_dashboard(page, job_site);
	} else {
		render_dashboard_placeholder(page);
	}
}

function render_dashboard_placeholder(page) {
	$(page.body).html(`
		<div class="text-center py-5">
			<h4 class="text-muted">Select a Job Site to view project dashboard</h4>
			<p class="text-muted">Or switch to Executive view for portfolio overview</p>
		</div>
	`);
}

function render_project_dashboard(page, job_site) {
	$(page.body).html('<div class="frappe-loading"></div>');

	frappe.call({
		method: 'construction.api.dashboard.get_project_dashboard',
		args: { job_site: job_site },
		callback: function(r) {
			if (r.message) {
				var data = r.message;
				var html = `
					<div class="row">
						<!-- Budget Card -->
						<div class="col-md-6">
							<div class="construction-dashboard-card">
								<h5>Budget Overview</h5>
								<div class="row mt-3">
									<div class="col-6">
										<div class="card-title">Original Budget</div>
										<div class="card-value">${format_currency(data.budget_summary.original)}</div>
									</div>
									<div class="col-6">
										<div class="card-title">Current Budget</div>
										<div class="card-value">${format_currency(data.budget_summary.current)}</div>
									</div>
								</div>
								<div class="row mt-3">
									<div class="col-6">
										<div class="card-title">Actual Cost</div>
										<div class="card-value">${format_currency(data.budget_summary.actual)}</div>
									</div>
									<div class="col-6">
										<div class="card-title">Variance</div>
										<div class="card-value ${data.budget_summary.variance >= 0 ? 'variance-positive' : 'variance-negative'}">
											${format_currency(data.budget_summary.variance)}
										</div>
									</div>
								</div>
								<div class="mt-3">
									<div class="card-title">CPI: ${(data.budget_summary.cpi || 1).toFixed(2)}</div>
									<div class="construction-progress">
										<div class="progress-bar ${data.budget_summary.cpi >= 1 ? 'on-track' : 'behind'}" 
											 style="width: ${Math.min((data.budget_summary.cpi || 1) * 100, 100)}%"></div>
									</div>
								</div>
							</div>
						</div>

						<!-- Schedule Card -->
						<div class="col-md-6">
							<div class="construction-dashboard-card">
								<h5>Schedule Status</h5>
								<div class="row mt-3">
									<div class="col-6">
										<div class="card-title">Progress</div>
										<div class="card-value">${(data.job_site.percent_complete || 0).toFixed(1)}%</div>
									</div>
									<div class="col-6">
										<div class="card-title">Days Remaining</div>
										<div class="card-value">${data.job_site.days_remaining || 0}</div>
									</div>
								</div>
								<div class="mt-3">
									<div class="card-title">Schedule Progress</div>
									<div class="construction-progress">
										<div class="progress-bar on-track" style="width: ${data.job_site.percent_complete || 0}%"></div>
									</div>
								</div>
							</div>
						</div>

						<!-- Open Items -->
						<div class="col-md-4">
							<div class="construction-dashboard-card">
								<div class="card-title">Open RFIs</div>
								<div class="card-value">${data.open_rfis}</div>
							</div>
						</div>
						<div class="col-md-4">
							<div class="construction-dashboard-card">
								<div class="card-title">Open Submittals</div>
								<div class="card-value">${data.open_submittals}</div>
							</div>
						</div>
						<div class="col-md-4">
							<div class="construction-dashboard-card">
								<div class="card-title">Punch Items</div>
								<div class="card-value">${data.punch_summary.completed || 0} / ${data.punch_summary.total || 0}</div>
							</div>
						</div>
					</div>
				`;
				$(page.body).html(html);
			}
		}
	});
}

function render_executive_dashboard(page) {
	$(page.body).html('<div class="frappe-loading"></div>');

	frappe.call({
		method: 'construction.api.dashboard.get_executive_dashboard',
		callback: function(r) {
			if (r.message) {
				var data = r.message;
				var html = `
					<div class="row">
						<!-- Portfolio Summary -->
						<div class="col-md-3">
							<div class="construction-dashboard-card">
								<div class="card-title">Active Projects</div>
								<div class="card-value">${data.project_count}</div>
							</div>
						</div>
						<div class="col-md-3">
							<div class="construction-dashboard-card">
								<div class="card-title">Total Budget</div>
								<div class="card-value">${format_currency(data.portfolio_totals.total_budget)}</div>
							</div>
						</div>
						<div class="col-md-3">
							<div class="construction-dashboard-card">
								<div class="card-title">Avg CPI</div>
								<div class="card-value ${data.portfolio_totals.avg_cpi >= 1 ? 'variance-positive' : 'variance-negative'}">
									${data.portfolio_totals.avg_cpi.toFixed(2)}
								</div>
							</div>
						</div>
						<div class="col-md-3">
							<div class="construction-dashboard-card">
								<div class="card-title">At Risk</div>
								<div class="card-value text-danger">${data.at_risk_projects.length}</div>
							</div>
						</div>
					</div>

					<!-- Projects Table -->
					<div class="construction-dashboard-card mt-4">
						<h5>All Projects</h5>
						<table class="table table-hover mt-3">
							<thead>
								<tr>
									<th>Project</th>
									<th>Status</th>
									<th>Progress</th>
									<th>Budget</th>
									<th>CPI</th>
									<th>SPI</th>
								</tr>
							</thead>
							<tbody>
								${data.projects.map(p => `
									<tr onclick="frappe.set_route('Form', 'Job Site', '${p.name}')">
										<td>${p.job_name}</td>
										<td><span class="job-site-status-${p.status.toLowerCase().replace(' ', '-')}">${p.status}</span></td>
										<td>
											<div class="construction-progress" style="width: 100px;">
												<div class="progress-bar on-track" style="width: ${p.percent_complete || 0}%"></div>
											</div>
										</td>
										<td>${format_currency(p.current_budget)}</td>
										<td class="${(p.cpi || 1) >= 1 ? 'variance-positive' : 'variance-negative'}">${(p.cpi || 1).toFixed(2)}</td>
										<td class="${(p.spi || 1) >= 1 ? 'variance-positive' : 'variance-negative'}">${(p.spi || 1).toFixed(2)}</td>
									</tr>
								`).join('')}
							</tbody>
						</table>
					</div>
				`;
				$(page.body).html(html);
			}
		}
	});
}
