<template>
	<BaseLayout :pageTitle="title">
		<template #body>
			<div class="flex flex-col mt-7 mb-7 p-4 gap-6">
				<!-- Period Selector -->
				<div class="flex items-center gap-4 mb-4">
					<label class="text-sm font-medium text-gray-700">{{ __("Period") }}:</label>
					<select
						v-model="selectedPeriod"
						@change="onPeriodChange"
						class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
					>
						<option value="week">{{ __("Week") }}</option>
						<option value="month">{{ __("Month") }}</option>
						<option value="year">{{ __("Year") }}</option>
					</select>
				</div>

				<!-- Chart Container -->
				<div class="dashboard-card">
					<div class="dashboard-card-header">
						<h3 class="dashboard-card-title">{{ title }}</h3>
					</div>
					<component :is="chartComponent" v-bind="chartProps" />
				</div>
			</div>
		</template>
	</BaseLayout>
</template>

<script setup>
import { ref, computed } from "vue"
import { useRoute } from "vue-router"
import BaseLayout from "@/components/BaseLayout.vue"
import AttendanceHeatmap from "@/components/charts/AttendanceHeatmap.vue"
import PayrollTrendChart from "@/components/charts/PayrollTrendChart.vue"
import LeaveUtilizationChart from "@/components/charts/LeaveUtilizationChart.vue"
import AttendanceTrendChart from "@/components/charts/AttendanceTrendChart.vue"
import { useAnalytics } from "@/composables"

const route = useRoute()
const { selectedPeriod, reloadAll } = useAnalytics()

const chartType = computed(() => route.params.chartType || "attendance")
const title = computed(() => {
	const titles = {
		attendance: "Attendance Heatmap",
		payroll: "Payroll Trends",
		leaves: "Leave Utilization",
		trends: "Attendance Trends",
	}
	return titles[chartType.value] || "Chart"
})

const chartComponent = computed(() => {
	const components = {
		attendance: AttendanceHeatmap,
		payroll: PayrollTrendChart,
		leaves: LeaveUtilizationChart,
		trends: AttendanceTrendChart,
	}
	return components[chartType.value] || AttendanceHeatmap
})

const chartProps = computed(() => {
	const baseProps = {
		period: selectedPeriod.value,
	}
	
	if (chartType.value === "attendance" || chartType.value === "trends") {
		return baseProps
	}
	
	return baseProps
})

const onPeriodChange = () => {
	reloadAll()
}
</script>
