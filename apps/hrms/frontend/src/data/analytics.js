import { createResource } from "frappe-ui"
import { employeeResource } from "./employee"

// Attendance Heatmap Data
export const attendanceHeatmapData = createResource({
	url: "hrms.analytics.api.charts.get_attendance_heatmap_data",
	params: () => ({
		employee: employeeResource.data?.name,
		period: "month",
	}),
	cache: "hrms:attendance_heatmap",
	auto: false,
})

// Payroll Trends Data
export const payrollTrendsData = createResource({
	url: "hrms.analytics.api.charts.get_payroll_trends",
	params: () => ({
		employee: employeeResource.data?.name,
		period: "year",
	}),
	cache: "hrms:payroll_trends",
	auto: false,
})

// Leave Utilization Data
export const leaveUtilizationData = createResource({
	url: "hrms.analytics.api.charts.get_leave_utilization",
	params: () => ({
		employee: employeeResource.data?.name,
		period: "year",
	}),
	cache: "hrms:leave_utilization",
	auto: false,
})

// Performance Metrics Data
export const performanceMetricsData = createResource({
	url: "hrms.analytics.api.charts.get_performance_metrics",
	params: () => ({
		employee: employeeResource.data?.name,
	}),
	cache: "hrms:performance_metrics",
	auto: false,
})

// Workforce Demographics Data
export const workforceDemographicsData = createResource({
	url: "hrms.analytics.api.charts.get_workforce_demographics",
	params: () => ({}),
	cache: "hrms:workforce_demographics",
	auto: false,
})

// Cost Analysis Data
export const costAnalysisData = createResource({
	url: "hrms.analytics.api.charts.get_cost_analysis",
	params: () => ({
		period: "year",
	}),
	cache: "hrms:cost_analysis",
	auto: false,
})

// Engagement Metrics Data
export const engagementMetricsData = createResource({
	url: "hrms.analytics.api.charts.get_engagement_metrics",
	params: () => ({}),
	cache: "hrms:engagement_metrics",
	auto: false,
})

// Attendance Trends Data
export const attendanceTrendsData = createResource({
	url: "hrms.analytics.api.charts.get_attendance_trends",
	params: () => ({
		employee: employeeResource.data?.name,
		period: "month",
	}),
	cache: "hrms:attendance_trends",
	auto: false,
})

// HR Manager specific resources (with department filter)
export const hrPayrollTrendsData = createResource({
	url: "hrms.analytics.api.charts.get_payroll_trends",
	params: (department) => ({
		department: department,
		period: "year",
	}),
	cache: "hrms:hr_payroll_trends",
	auto: false,
})

export const hrWorkforceDemographicsData = createResource({
	url: "hrms.analytics.api.charts.get_workforce_demographics",
	params: (department) => ({
		department: department,
	}),
	cache: "hrms:hr_workforce_demographics",
	auto: false,
})

export const hrCostAnalysisData = createResource({
	url: "hrms.analytics.api.charts.get_cost_analysis",
	params: (department) => ({
		department: department,
		period: "year",
	}),
	cache: "hrms:hr_cost_analysis",
	auto: false,
})
