<template>
	<div class="workforce-demographics">
		<div v-if="loading" class="flex items-center justify-center p-8">
			<div class="text-gray-500">Loading...</div>
		</div>
		<div v-else-if="error" class="text-red-500 p-4">{{ error }}</div>
		<div v-else class="space-y-6">
			<!-- Age Distribution -->
			<div v-if="ageData.length > 0">
				<h3 class="text-sm font-semibold mb-2">{{ __("Age Distribution") }}</h3>
				<apexchart
					type="bar"
					height="200"
					:options="ageChartOptions"
					:series="ageSeries"
				></apexchart>
			</div>
			
			<!-- Gender Distribution -->
			<div v-if="genderData.length > 0">
				<h3 class="text-sm font-semibold mb-2">{{ __("Gender Distribution") }}</h3>
				<apexchart
					type="pie"
					height="250"
					:options="genderChartOptions"
					:series="genderSeries"
				></apexchart>
			</div>
			
			<!-- Department Distribution -->
			<div v-if="deptData.length > 0">
				<h3 class="text-sm font-semibold mb-2">{{ __("Department Distribution") }}</h3>
				<apexchart
					type="bar"
					height="250"
					:options="deptChartOptions"
					:series="deptSeries"
				></apexchart>
			</div>
		</div>
	</div>
</template>

<script setup>
import { computed, inject, onMounted } from "vue"
import { workforceDemographicsData } from "@/data/analytics"

const props = defineProps({
	department: {
		type: String,
		default: null,
	},
})

const __ = inject("$translate")

const loading = computed(() => workforceDemographicsData.loading)
const error = computed(() => workforceDemographicsData.error)

const ageData = computed(() => workforceDemographicsData.data?.age_distribution || [])
const genderData = computed(() => workforceDemographicsData.data?.gender_distribution || [])
const deptData = computed(() => workforceDemographicsData.data?.department_distribution || [])

const ageSeries = computed(() => [
	{
		name: __("Employees"),
		data: ageData.value.map(item => item.value),
	},
])

const ageChartOptions = computed(() => ({
	chart: {
		type: "bar",
		height: 200,
		toolbar: { show: false },
	},
	xaxis: {
		categories: ageData.value.map(item => item.label),
	},
	colors: ["#3b82f6"],
	dataLabels: {
		enabled: true,
	},
}))

const genderSeries = computed(() => genderData.value.map(item => item.value))

const genderChartOptions = computed(() => ({
	chart: {
		type: "pie",
		height: 250,
	},
	labels: genderData.value.map(item => item.label),
	colors: ["#3b82f6", "#10b981", "#f59e0b"],
	legend: {
		position: "bottom",
	},
}))

const deptSeries = computed(() => [
	{
		name: __("Employees"),
		data: deptData.value.map(item => item.value),
	},
])

const deptChartOptions = computed(() => ({
	chart: {
		type: "bar",
		height: 250,
		toolbar: { show: false },
		horizontal: true,
	},
	xaxis: {
		categories: deptData.value.map(item => item.label),
	},
	colors: ["#8b5cf6"],
	dataLabels: {
		enabled: true,
	},
}))
</script>

<style scoped>
.workforce-demographics {
	@apply w-full;
}
</style>
