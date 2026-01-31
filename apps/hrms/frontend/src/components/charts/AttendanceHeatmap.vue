<template>
	<div class="attendance-heatmap-container">
		<div v-if="loading" class="flex items-center justify-center p-8">
			<div class="text-gray-500">Loading...</div>
		</div>
		<div v-else-if="error" class="text-red-500 p-4">{{ error }}</div>
		<div v-else class="heatmap-wrapper">
			<div class="grid grid-cols-7 gap-1 mb-4">
				<div
					v-for="(day, index) in daysOfWeek"
					:key="index"
					class="text-xs text-gray-600 text-center font-medium"
				>
					{{ day }}
				</div>
			</div>
			<div class="grid grid-cols-7 gap-1">
				<div
					v-for="(cell, index) in heatmapCells"
					:key="index"
					:class="getCellClass(cell)"
					class="aspect-square rounded text-xs flex items-center justify-center cursor-pointer hover:opacity-80 transition-opacity"
					:title="getCellTooltip(cell)"
				>
					{{ cell.day }}
				</div>
			</div>
			<div class="flex items-center justify-between mt-4 text-xs">
				<div class="flex items-center gap-4">
					<span class="text-gray-600">Less</span>
					<div class="flex gap-1">
						<div class="w-3 h-3 rounded bg-gray-200"></div>
						<div class="w-3 h-3 rounded bg-blue-200"></div>
						<div class="w-3 h-3 rounded bg-blue-400"></div>
						<div class="w-3 h-3 rounded bg-blue-600"></div>
						<div class="w-3 h-3 rounded bg-blue-800"></div>
					</div>
					<span class="text-gray-600">More</span>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { computed, inject, onMounted } from "vue"
import { attendanceHeatmapData } from "@/data/analytics"

const props = defineProps({
	employee: {
		type: String,
		default: null,
	},
	period: {
		type: String,
		default: "month",
	},
})

const dayjs = inject("$dayjs")

const loading = computed(() => attendanceHeatmapData.loading)
const error = computed(() => attendanceHeatmapData.error)

const daysOfWeek = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

const heatmapCells = computed(() => {
	if (!attendanceHeatmapData.data?.heatmap_data) return []
	
	const data = attendanceHeatmapData.data.heatmap_data
	const dataMap = new Map(data.map(item => [item.date, item]))
	
	// Get start and end dates
	const today = dayjs()
	const startDate = props.period === "month" 
		? today.startOf("month")
		: today.subtract(30, "days")
	const endDate = props.period === "month"
		? today.endOf("month")
		: today
	
	// Generate calendar cells
	const cells = []
	let currentDate = startDate.startOf("week")
	const end = endDate.endOf("week")
	
	while (currentDate.isBefore(end) || currentDate.isSame(end)) {
		const dateStr = currentDate.format("YYYY-MM-DD")
		const cellData = dataMap.get(dateStr) || { date: dateStr, present: 0, absent: 0, on_leave: 0, total: 0 }
		
		cells.push({
			date: dateStr,
			day: currentDate.date(),
			...cellData,
			isCurrentMonth: currentDate.month() === today.month(),
		})
		
		currentDate = currentDate.add(1, "day")
	}
	
	return cells
})

const getCellClass = (cell) => {
	if (!cell.isCurrentMonth) return "bg-gray-100 text-gray-400"
	
	const total = cell.total || 0
	if (total === 0) return "bg-gray-200"
	if (total < 5) return "bg-blue-200"
	if (total < 10) return "bg-blue-400"
	if (total < 20) return "bg-blue-600"
	return "bg-blue-800 text-white"
}

const getCellTooltip = (cell) => {
	if (!cell.isCurrentMonth) return ""
	return `${cell.date}: ${cell.present} present, ${cell.absent} absent, ${cell.on_leave} on leave`
}

onMounted(() => {
	if (props.employee) {
		attendanceHeatmapData.params.employee = props.employee
	}
	attendanceHeatmapData.params.period = props.period
	attendanceHeatmapData.reload()
})
</script>

<style scoped>
.attendance-heatmap-container {
	@apply w-full;
}
</style>
