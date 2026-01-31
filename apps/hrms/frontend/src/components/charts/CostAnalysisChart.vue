<template>
	<div class="cost-analysis-chart">
		<div v-if="loading" class="flex items-center justify-center p-8">
			<div class="text-gray-500">Loading...</div>
		</div>
		<div v-else-if="error" class="text-red-500 p-4">{{ error }}</div>
		<apexchart
			v-else
			type="bar"
			height="350"
			:options="chartOptions"
			:series="series"
		></apexchart>
	</div>
</template>

<script setup>
import { computed, inject, onMounted } from "vue"
import { costAnalysisData } from "@/data/analytics"

const props = defineProps({
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

const loading = computed(() => costAnalysisData.loading)
const error = computed(() => costAnalysisData.error)

const series = computed(() => {
	if (!costAnalysisData.data?.by_department) return []
	
	const deptData = costAnalysisData.data.by_department
	
	return [
		{
			name: __("Gross Pay"),
			data: deptData.map(item => item.gross_pay || 0),
		},
		{
			name: __("Deductions"),
			data: deptData.map(item => item.deductions || 0),
		},
		{
			name: __("Net Pay"),
			data: deptData.map(item => item.net_pay || 0),
		},
	]
})

const chartOptions = computed(() => {
	if (!costAnalysisData.data?.by_department) return {}
	
	const deptData = costAnalysisData.data.by_department
	
	return {
		chart: {
			type: "bar",
			height: 350,
			stacked: true,
			toolbar: {
				show: false,
			},
		},
		xaxis: {
			categories: deptData.map(item => item.department),
			labels: {
				style: {
					fontSize: "12px",
				},
				rotate: -45,
			},
		},
		yaxis: {
			labels: {
				formatter: (value) => {
					return new Intl.NumberFormat("en-US", {
						style: "currency",
						currency: "USD",
						minimumFractionDigits: 0,
					}).format(value)
				},
			},
		},
		colors: ["#3b82f6", "#ef4444", "#10b981"],
		legend: {
			position: "top",
		},
		dataLabels: {
			enabled: false,
		},
		tooltip: {
			y: {
				formatter: (value) => {
					return new Intl.NumberFormat("en-US", {
						style: "currency",
						currency: "USD",
					}).format(value)
				},
			},
		},
	}
})
</script>

<style scoped>
.cost-analysis-chart {
	@apply w-full;
}
</style>
