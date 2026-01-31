<template>
	<div class="employee-engagement-gauge">
		<div v-if="loading" class="flex items-center justify-center p-8">
			<div class="text-gray-500">Loading...</div>
		</div>
		<div v-else-if="error" class="text-red-500 p-4">{{ error }}</div>
		<div v-else class="gauge-container">
			<apexchart
				type="radialBar"
				height="300"
				:options="chartOptions"
				:series="series"
			></apexchart>
			<div class="text-center mt-4">
				<div class="text-2xl font-bold" :class="getScoreClass()">
					{{ engagementScore }}%
				</div>
				<div class="text-sm text-gray-600 mt-1">{{ __("Engagement Score") }}</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { computed, inject, onMounted } from "vue"
import { engagementMetricsData } from "@/data/analytics"

const props = defineProps({
	department: {
		type: String,
		default: null,
	},
})

const __ = inject("$translate")

const loading = computed(() => engagementMetricsData.loading)
const error = computed(() => engagementMetricsData.error)

const engagementScore = computed(() => {
	return engagementMetricsData.data?.overall_score || 0
})

const series = computed(() => [engagementScore.value])

const chartOptions = computed(() => {
	const score = engagementScore.value
	let color = "#ef4444" // red
	if (score >= 80) {
		color = "#10b981" // green
	} else if (score >= 60) {
		color = "#f59e0b" // yellow
	}
	
	return {
		chart: {
			type: "radialBar",
			height: 300,
		},
		plotOptions: {
			radialBar: {
				hollow: {
					size: "70%",
				},
				track: {
					background: "#e5e7eb",
				},
				dataLabels: {
					show: false,
				},
			},
		},
		colors: [color],
		labels: [__("Engagement")],
	}
})

const getScoreClass = () => {
	const score = engagementScore.value
	if (score >= 80) return "text-green-600"
	if (score >= 60) return "text-yellow-600"
	return "text-red-600"
}
</script>

<style scoped>
.employee-engagement-gauge {
	@apply w-full;
}
</style>
