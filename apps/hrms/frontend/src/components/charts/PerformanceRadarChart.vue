<template>
	<div class="performance-radar-chart">
		<div v-if="loading" class="flex items-center justify-center p-8">
			<div class="text-gray-500">Loading...</div>
		</div>
		<div v-else-if="error" class="text-red-500 p-4">{{ error }}</div>
		<apexchart
			v-else
			type="radar"
			height="350"
			:options="chartOptions"
			:series="series"
		></apexchart>
	</div>
</template>

<script setup>
import { computed, inject, onMounted } from "vue"
import { performanceMetricsData } from "@/data/analytics"

const props = defineProps({
	employee: {
		type: String,
		default: null,
	},
	department: {
		type: String,
		default: null,
	},
})

const __ = inject("$translate")

const loading = computed(() => performanceMetricsData.loading)
const error = computed(() => performanceMetricsData.error)

const series = computed(() => {
	if (!performanceMetricsData.data?.employee_scores) return []
	
	const scores = performanceMetricsData.data.employee_scores.slice(0, 5)
	
	return [
		{
			name: __("Performance Score"),
			data: scores.map(item => item.score),
		},
	]
})

const chartOptions = computed(() => {
	if (!performanceMetricsData.data?.employee_scores) return {}
	
	const scores = performanceMetricsData.data.employee_scores.slice(0, 5)
	
	return {
		chart: {
			type: "radar",
			height: 350,
			toolbar: {
				show: false,
			},
		},
		xaxis: {
			categories: scores.map(item => item.employee_name || item.employee),
		},
		yaxis: {
			max: 100,
			min: 0,
		},
		colors: ["#3b82f6"],
		fill: {
			opacity: 0.3,
		},
		stroke: {
			width: 2,
		},
		markers: {
			size: 4,
		},
		tooltip: {
			y: {
				formatter: (value) => {
					return value.toFixed(2)
				},
			},
		},
	}
})
</script>

<style scoped>
.performance-radar-chart {
	@apply w-full;
}
</style>
