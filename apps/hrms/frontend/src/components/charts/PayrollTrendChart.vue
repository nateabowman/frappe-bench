<template>
	<div class="payroll-trend-chart">
		<div v-if="loading" class="flex items-center justify-center p-8">
			<div class="text-gray-500">Loading...</div>
		</div>
		<div v-else-if="error" class="text-red-500 p-4">{{ error }}</div>
		<apexchart
			v-else
			type="area"
			height="300"
			:options="chartOptions"
			:series="series"
		></apexchart>
	</div>
</template>

<script setup>
import { computed, inject, onMounted } from "vue"
import { payrollTrendsData } from "@/data/analytics"

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

const loading = computed(() => payrollTrendsData.loading)
const error = computed(() => payrollTrendsData.error)

const series = computed(() => {
	if (!payrollTrendsData.data?.trend_data) return []
	
	const data = payrollTrendsData.data.trend_data
	
	return [
		{
			name: __("Gross Pay"),
			data: data.map(item => item.gross_pay || 0),
		},
		{
			name: __("Net Pay"),
			data: data.map(item => item.net_pay || 0),
		},
	]
})

const chartOptions = computed(() => {
	if (!payrollTrendsData.data?.trend_data) return {}
	
	const data = payrollTrendsData.data.trend_data
	
	return {
		chart: {
			type: "area",
			height: 300,
			toolbar: {
				show: false,
			},
			zoom: {
				enabled: false,
			},
		},
		dataLabels: {
			enabled: false,
		},
		stroke: {
			curve: "smooth",
			width: 2,
		},
		xaxis: {
			categories: data.map(item => item.month),
			labels: {
				style: {
					fontSize: "12px",
				},
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
		fill: {
			type: "gradient",
			gradient: {
				shadeIntensity: 1,
				opacityFrom: 0.7,
				opacityTo: 0.3,
				stops: [0, 90, 100],
			},
		},
		colors: ["#3b82f6", "#10b981"],
		legend: {
			position: "top",
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

<script>
export default {
	components: {
		apexchart: VueApexCharts,
	},
}
</script>

<style scoped>
.payroll-trend-chart {
	@apply w-full;
}
</style>
