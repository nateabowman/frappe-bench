<template>
	<BaseLayout>
		<template #body>
			<div class="flex flex-col items-center my-7 p-4 gap-7">
				<!-- Personalized Welcome Section -->
				<div class="w-full bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg p-6 text-white">
					<h2 class="text-2xl font-bold mb-2">
						{{ __("Welcome back") }}, {{ employee?.data?.employee_name || __("Employee") }}!
					</h2>
					<p class="text-blue-100">{{ __("Here's your overview for today") }}</p>
				</div>

				<!-- Quick Stats Cards -->
				<div class="w-full grid grid-cols-2 gap-4">
					<div class="stat-card bg-blue-50 border-blue-200">
						<div class="stat-card-icon bg-blue-500 text-white">
							<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
							</svg>
						</div>
						<div class="stat-card-value text-blue-900">{{ attendanceStats?.present || 0 }}</div>
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

				<CheckInPanel />
				<QuickLinks :items="quickLinks" :title="__('Quick Links')" />
				<RequestPanel />

				<!-- Analytics Quick View -->
				<div class="w-full">
					<div class="flex items-center justify-between mb-4">
						<h3 class="text-lg font-semibold text-gray-800">{{ __("Your Analytics") }}</h3>
						<router-link :to="{ name: 'PersonalDashboard' }" class="text-sm text-blue-600">
							{{ __("View All") }} →
						</router-link>
					</div>
					
					<!-- Charts Grid -->
					<div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
						<div class="dashboard-card">
							<h4 class="text-sm font-semibold text-gray-700 mb-3">{{ __("Attendance Heatmap") }}</h4>
							<AttendanceHeatmap :employee="employee?.data?.name" period="month" />
						</div>
						<div class="dashboard-card">
							<h4 class="text-sm font-semibold text-gray-700 mb-3">{{ __("Leave Utilization") }}</h4>
							<LeaveUtilizationChart :employee="employee?.data?.name" period="year" />
						</div>
					</div>
					
					<div class="dashboard-card">
						<h4 class="text-sm font-semibold text-gray-700 mb-3">{{ __("Attendance Trends") }}</h4>
						<AttendanceTrendChart :employee="employee?.data?.name" period="month" />
					</div>
				</div>
			</div>
		</template>
	</BaseLayout>
</template>

<script setup>
import { inject, markRaw, computed } from "vue"
import { attendanceHeatmapData } from "@/data/analytics"
import { leaveBalance as leaveBalanceResource } from "@/data/leaves"

import CheckInPanel from "@/components/CheckInPanel.vue"
import QuickLinks from "@/components/QuickLinks.vue"
import BaseLayout from "@/components/BaseLayout.vue"
import RequestPanel from "@/components/RequestPanel.vue"
import AttendanceHeatmap from "@/components/charts/AttendanceHeatmap.vue"
import LeaveUtilizationChart from "@/components/charts/LeaveUtilizationChart.vue"
import AttendanceTrendChart from "@/components/charts/AttendanceTrendChart.vue"
import AttendanceIcon from "@/components/icons/AttendanceIcon.vue"
import ShiftIcon from "@/components/icons/ShiftIcon.vue"
import LeaveIcon from "@/components/icons/LeaveIcon.vue"
import ExpenseIcon from "@/components/icons/ExpenseIcon.vue"
import EmployeeAdvanceIcon from "@/components/icons/EmployeeAdvanceIcon.vue"
import SalaryIcon from "@/components/icons/SalaryIcon.vue"

const __ = inject("$translate")
const employee = inject("$employee")

const attendanceStats = computed(() => {
	return attendanceHeatmapData.data?.summary || {}
})

const leaveBalance = computed(() => {
	if (!leaveBalanceResource.data) return 0
	// Sum all leave balances
	return Object.values(leaveBalanceResource.data).reduce(
		(sum, allocation) => sum + (allocation.balance_leaves || 0),
		0
	)
})

const quickLinks = [
	{
		icon: markRaw(AttendanceIcon),
		title: __("Request Attendance"),
		route: "AttendanceRequestFormView",
	},
	{
		icon: markRaw(ShiftIcon),
		title: __("Request a Shift"),
		route: "ShiftRequestFormView",
	},
	{
		icon: markRaw(LeaveIcon),
		title: __("Request Leave"),
		route: "LeaveApplicationFormView",
	},
	{
		icon: markRaw(ExpenseIcon),
		title: __("Claim an Expense"),
		route: "ExpenseClaimFormView",
	},
	{
		icon: markRaw(EmployeeAdvanceIcon),
		title: __("Request an Advance"),
		route: "EmployeeAdvanceFormView",
	},
	{
		icon: markRaw(SalaryIcon),
		title: __("View Salary Slips"),
		route: "SalarySlipsDashboard",
	},
]
</script>
