<template>
	<div class="leave-utilization-chart">
		<div v-if="loading" class="flex items-center justify-center p-8">
			<div class="text-gray-500">Loading...</div>
		</div>
		<div v-else-if="error" class="text-red-500 p-4">{{ error }}</div>
		<apexchart
			v-else
			type="donut"
			height="300"
			:options="chartOptions"
			:series="series"
		></apexchart>
	</div>
</template>

<script setup>
import { computed, inject, onMounted } from "vue"
import { leaveUtilizationData } from "@/data/analytics"

const props = defineProps({
	employee: {
		type: String,
		default: null,
	},
	department: {
		type: String,
		default: null,
	},
	period: {
		type: String,
		default: "year",
	},
})

const __ = inject("$translate")

const loading = computed(() => leaveUtilizationData.loading)
const error = computed(() => leaveUtilizationData.error)

const series = computed(() => {
	if (!leaveUtilizationData.data?.chart_data) return []
	return leaveUtilizationData.data.chart_data.map(item => item.value)
})

const chartOptions = computed(() => {
	if (!leaveUtilizationData.data?.chart_data) return {}
	
	const data = leaveUtilizationData.data.chart_data
	const colors = [
		"#3b82f6",
		"#10b981",
		"#f59e0b",
		"#ef4444",
		"#8b5cf6",
		"#ec4899",
		"#06b6d4",
		"#84cc16",
	]
	
	return {
		chart: {
			type: "donut",
			height: 300,
		},
		labels: data.map(item => item.label),
		colors: colors.slice(0, data.length),
		legend: {
			position: "bottom",
		},
		dataLabels: {
			enabled: true,
			formatter: (val) => {
				return val.toFixed(1) + "%"
			},
		},
		tooltip: {
			y: {
				formatter: (value) => {
					return `${value} ${__("days")}`
				},
			},
		},
		plotOptions: {
			pie: {
				donut: {
					labels: {
						show: true,
						total: {
							show: true,
							label: __("Total Days"),
							formatter: () => {
								return leaveUtilizationData.data?.total_days || 0
							},
						},
					},
				},
			},
		},
	}
})
</script>

<style scoped>
.leave-utilization-chart {
	@apply w-full;
}
</style>
