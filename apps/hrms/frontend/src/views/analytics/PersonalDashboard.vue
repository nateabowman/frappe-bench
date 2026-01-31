<template>
	<BaseLayout pageTitle="Analytics">
		<template #body>
			<div class="flex flex-col mt-7 mb-7 p-4 gap-6">
				<!-- Welcome Section -->
				<div class="bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg p-6 text-white">
					<h2 class="text-2xl font-bold mb-2">
						{{ __("Welcome back") }}, {{ employee?.data?.employee_name || __("Employee") }}!
					</h2>
					<p class="text-blue-100">{{ __("Here's your personal analytics dashboard") }}</p>
				</div>

				<!-- Quick Stats -->
				<div class="grid grid-cols-2 gap-4">
					<div class="stat-card bg-blue-50 border-blue-200">
						<div class="stat-card-icon bg-blue-500 text-white">
							<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
							</svg>
						</div>
						<div class="stat-card-value text-blue-900">{{ attendanceSummary?.present || 0 }}</div>
						<div class="stat-card-label text-blue-700">{{ __("Days Present") }}</div>
					</div>

					<div class="stat-card bg-green-50 border-green-200">
						<div class="stat-card-icon bg-green-500 text-white">
							<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
							</svg>
						</div>
						<div class="stat-card-value text-green-900">{{ leaveBalance || 0 }}</div>
						<div class="stat-card-label text-green-700">{{ __("Leave Balance") }}</div>
					</div>
				</div>

				<!-- Attendance Heatmap -->
				<div class="dashboard-card">
					<div class="dashboard-card-header">
						<h3 class="dashboard-card-title">{{ __("Attendance Heatmap") }}</h3>
					</div>
					<AttendanceHeatmap :employee="employee?.data?.name" period="month" />
				</div>

				<!-- Attendance Trends -->
				<div class="dashboard-card">
					<div class="dashboard-card-header">
						<h3 class="dashboard-card-title">{{ __("Attendance Trends") }}</h3>
					</div>
					<AttendanceTrendChart :employee="employee?.data?.name" period="month" />
				</div>

				<!-- Leave Utilization -->
				<div class="dashboard-card">
					<div class="dashboard-card-header">
						<h3 class="dashboard-card-title">{{ __("Leave Utilization") }}</h3>
					</div>
					<LeaveUtilizationChart :employee="employee?.data?.name" period="year" />
				</div>

				<!-- Salary History -->
				<div class="dashboard-card">
					<div class="dashboard-card-header">
						<h3 class="dashboard-card-title">{{ __("Salary History") }}</h3>
					</div>
					<PayrollTrendChart :employee="employee?.data?.name" period="year" />
				</div>

				<!-- Performance Scorecard -->
				<div class="dashboard-card">
					<div class="dashboard-card-header">
						<h3 class="dashboard-card-title">{{ __("Performance Overview") }}</h3>
					</div>
					<PerformanceRadarChart :employee="employee?.data?.name" />
				</div>
			</div>
		</template>
	</BaseLayout>
</template>

<script setup>
import { inject, computed } from "vue"
import BaseLayout from "@/components/BaseLayout.vue"
import AttendanceHeatmap from "@/components/charts/AttendanceHeatmap.vue"
import AttendanceTrendChart from "@/components/charts/AttendanceTrendChart.vue"
import LeaveUtilizationChart from "@/components/charts/LeaveUtilizationChart.vue"
import PayrollTrendChart from "@/components/charts/PayrollTrendChart.vue"
import PerformanceRadarChart from "@/components/charts/PerformanceRadarChart.vue"
import { attendanceHeatmapData } from "@/data/analytics"

const __ = inject("$translate")
const employee = inject("$employee")

const attendanceSummary = computed(() => {
	return attendanceHeatmapData.data?.summary || {}
})

const leaveBalance = computed(() => {
	// This would come from leave balance data
	return 0
})
</script>

<script>
export default {
	name: "PersonalDashboard",
}
</script>
