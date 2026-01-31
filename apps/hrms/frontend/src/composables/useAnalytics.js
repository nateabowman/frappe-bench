import { computed, ref } from "vue"
import { createResource } from "frappe-ui"
import { employeeResource } from "@/data/employee"

/**
 * Composable for analytics data management
 */
export function useAnalytics() {
	const selectedPeriod = ref("month")
	const selectedEmployee = ref(null)
	const selectedDepartment = ref(null)

	const attendanceHeatmap = createResource({
		url: "hrms.analytics.api.charts.get_attendance_heatmap_data",
		params: () => ({
			employee: selectedEmployee.value || employeeResource.data?.name,
			department: selectedDepartment.value,
			period: selectedPeriod.value,
		}),
		cache: "hrms:attendance_heatmap",
		auto: false,
	})

	const payrollTrends = createResource({
		url: "hrms.analytics.api.charts.get_payroll_trends",
		params: () => ({
			employee: selectedEmployee.value || employeeResource.data?.name,
			department: selectedDepartment.value,
			period: selectedPeriod.value,
		}),
		cache: "hrms:payroll_trends",
		auto: false,
	})

	const leaveUtilization = createResource({
		url: "hrms.analytics.api.charts.get_leave_utilization",
		params: () => ({
			employee: selectedEmployee.value || employeeResource.data?.name,
			department: selectedDepartment.value,
			period: selectedPeriod.value,
		}),
		cache: "hrms:leave_utilization",
		auto: false,
	})

	const performanceMetrics = createResource({
		url: "hrms.analytics.api.charts.get_performance_metrics",
		params: () => ({
			employee: selectedEmployee.value || employeeResource.data?.name,
			department: selectedDepartment.value,
		}),
		cache: "hrms:performance_metrics",
		auto: false,
	})

	const workforceDemographics = createResource({
		url: "hrms.analytics.api.charts.get_workforce_demographics",
		params: () => ({
			department: selectedDepartment.value,
		}),
		cache: "hrms:workforce_demographics",
		auto: false,
	})

	const costAnalysis = createResource({
		url: "hrms.analytics.api.charts.get_cost_analysis",
		params: () => ({
			department: selectedDepartment.value,
			period: selectedPeriod.value,
		}),
		cache: "hrms:cost_analysis",
		auto: false,
	})

	const engagementMetrics = createResource({
		url: "hrms.analytics.api.charts.get_engagement_metrics",
		params: () => ({
			department: selectedDepartment.value,
		}),
		cache: "hrms:engagement_metrics",
		auto: false,
	})

	const attendanceTrends = createResource({
		url: "hrms.analytics.api.charts.get_attendance_trends",
		params: () => ({
			employee: selectedEmployee.value || employeeResource.data?.name,
			department: selectedDepartment.value,
			period: selectedPeriod.value,
		}),
		cache: "hrms:attendance_trends",
		auto: false,
	})

	const reloadAll = () => {
		attendanceHeatmap.reload()
		payrollTrends.reload()
		leaveUtilization.reload()
		performanceMetrics.reload()
		workforceDemographics.reload()
		costAnalysis.reload()
		engagementMetrics.reload()
		attendanceTrends.reload()
	}

	return {
		selectedPeriod,
		selectedEmployee,
		selectedDepartment,
		attendanceHeatmap,
		payrollTrends,
		leaveUtilization,
		performanceMetrics,
		workforceDemographics,
		costAnalysis,
		engagementMetrics,
		attendanceTrends,
		reloadAll,
	}
}
