<template>
	<div class="attendance-trend-chart">
		<div v-if="loading" class="flex items-center justify-center p-8">
			<div class="text-gray-500">Loading...</div>
		</div>
		<div v-else-if="error" class="text-red-500 p-4">{{ error }}</div>
		<apexchart
			v-else
			type="line"
			height="300"
			:options="chartOptions"
			:series="series"
		></apexchart>
	</div>
</template>

<script setup>
import { computed, inject, onMounted } from "vue"
import { attendanceTrendsData } from "@/data/analytics"

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
		default: "month",
	},
})

const __ = inject("$translate")

const loading = computed(() => attendanceTrendsData.loading)
const error = computed(() => attendanceTrendsData.error)

const series = computed(() => {
	if (!attendanceTrendsData.data?.trend_data) return []
	
	const data = attendanceTrendsData.data.trend_data
	
	return [
		{
			name: __("Attendance Rate (%)"),
			data: data.map(item => item.attendance_rate || 0),
		},
		{
			name: __("Present"),
			data: data.map(item => item.present || 0),
		},
		{
			name: __("Absent"),
			data: data.map(item => item.absent || 0),
		},
	]
})

const chartOptions = computed(() => {
	if (!attendanceTrendsData.data?.trend_data) return {}
	
	const data = attendanceTrendsData.data.trend_data
	
	return {
		chart: {
			type: "line",
			height: 300,
			toolbar: {
				show: false,
			},
			zoom: {
				enabled: false,
			},
		},
		stroke: {
			curve: "smooth",
			width: 2,
		},
		xaxis: {
			categories: data.map(item => {
				const date = new Date(item.date)
				return date.toLocaleDateString("en-US", { month: "short", day: "numeric" })
			}),
			labels: {
				style: {
					fontSize: "12px",
				},
			},
		},
		yaxis: [
			{
				title: {
					text: __("Rate (%)"),
				},
				max: 100,
			},
			{
				title: {
					text: __("Count"),
				},
				opposite: true,
			},
		],
		colors: ["#3b82f6", "#10b981", "#ef4444"],
		legend: {
			position: "top",
		},
		markers: {
			size: 4,
		},
		tooltip: {
			shared: true,
			intersect: false,
		},
	}
})
</script>

<style scoped>
.attendance-trend-chart {
	@apply w-full;
}
</style>
