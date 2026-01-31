<template>
	<BaseLayout pageTitle="Operational Dashboard">
		<template #body>
			<div class="flex flex-col mt-7 mb-7 p-4 gap-6">
				<!-- Header -->
				<div class="bg-gradient-to-r from-teal-600 to-cyan-600 rounded-lg p-6 text-white">
					<h2 class="text-2xl font-bold mb-2">{{ __("Operational Dashboard") }}</h2>
					<p class="text-teal-100">{{ __("Daily operations and team management") }}</p>
				</div>

				<!-- Quick Actions -->
				<div class="grid grid-cols-2 md:grid-cols-4 gap-4">
					<div class="stat-card bg-red-50 border-red-200">
						<div class="stat-card-icon bg-red-500 text-white">
							<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
							</svg>
						</div>
						<div class="stat-card-value text-red-900">{{ pendingApprovals || 0 }}</div>
						<div class="stat-card-label text-red-700">{{ __("Pending Approvals") }}</div>
					</div>

					<div class="stat-card bg-yellow-50 border-yellow-200">
						<div class="stat-card-icon bg-yellow-500 text-white">
							<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
							</svg>
						</div>
						<div class="stat-card-value text-yellow-900">{{ onLeaveToday || 0 }}</div>
						<div class="stat-card-label text-yellow-700">{{ __("On Leave Today") }}</div>
					</div>

					<div class="stat-card bg-blue-50 border-blue-200">
						<div class="stat-card-icon bg-blue-500 text-white">
							<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
							</svg>
						</div>
						<div class="stat-card-value text-blue-900">{{ presentToday || 0 }}</div>
						<div class="stat-card-label text-blue-700">{{ __("Present Today") }}</div>
					</div>

					<div class="stat-card bg-green-50 border-green-200">
						<div class="stat-card-icon bg-green-500 text-white">
							<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
							</svg>
						</div>
						<div class="stat-card-value text-green-900">{{ payrollStatus || __("Ready") }}</div>
						<div class="stat-card-label text-green-700">{{ __("Payroll Status") }}</div>
					</div>
				</div>

				<!-- Team Attendance Overview -->
				<div class="dashboard-card">
					<div class="dashboard-card-header">
						<h3 class="dashboard-card-title">{{ __("Team Attendance Overview") }}</h3>
					</div>
					<AttendanceTrendChart period="month" />
				</div>

				<!-- Leave Calendar View -->
				<div class="dashboard-card">
					<div class="dashboard-card-header">
						<h3 class="dashboard-card-title">{{ __("Leave Calendar") }}</h3>
					</div>
					<AttendanceHeatmap period="month" />
				</div>

				<!-- Department-wise Leave Utilization -->
				<div class="dashboard-card">
					<div class="dashboard-card-header">
						<h3 class="dashboard-card-title">{{ __("Leave Utilization by Department") }}</h3>
					</div>
					<LeaveUtilizationChart period="year" />
				</div>
			</div>
		</template>
	</BaseLayout>
</template>

<script setup>
import { inject, computed } from "vue"
import BaseLayout from "@/components/BaseLayout.vue"
import AttendanceTrendChart from "@/components/charts/AttendanceTrendChart.vue"
import AttendanceHeatmap from "@/components/charts/AttendanceHeatmap.vue"
import LeaveUtilizationChart from "@/components/charts/LeaveUtilizationChart.vue"

const __ = inject("$translate")

const pendingApprovals = computed(() => {
	// This would come from approval data
	return 0
})

const onLeaveToday = computed(() => {
	// This would come from leave data
	return 0
})

const presentToday = computed(() => {
	// This would come from attendance data
	return 0
})

const payrollStatus = computed(() => {
	// This would come from payroll data
	return __("Ready")
})
</script>

<script>
export default {
	name: "OperationalDashboard",
}
</script>
