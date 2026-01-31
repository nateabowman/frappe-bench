<template>
	<div class="stat-card" :class="cardClass">
		<div class="stat-card-icon" :class="iconClass">
			<slot name="icon">
				<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
				</svg>
			</slot>
		</div>
		<div class="stat-card-value" :class="valueClass">
			{{ value }}
		</div>
		<div class="stat-card-label" :class="labelClass">
			{{ label }}
		</div>
		<div v-if="change !== null" class="dashboard-card-change" :class="changeClass">
			{{ changeText }}
		</div>
	</div>
</template>

<script setup>
import { computed } from "vue"

const props = defineProps({
	value: {
		type: [String, Number],
		required: true,
	},
	label: {
		type: String,
		required: true,
	},
	variant: {
		type: String,
		default: "blue",
		validator: (value) => ["blue", "green", "red", "yellow", "purple", "orange"].includes(value),
	},
	change: {
		type: Number,
		default: null,
	},
	changeLabel: {
		type: String,
		default: null,
	},
})

const cardClass = computed(() => {
	const variants = {
		blue: "bg-blue-50 border-blue-200",
		green: "bg-green-50 border-green-200",
		red: "bg-red-50 border-red-200",
		yellow: "bg-yellow-50 border-yellow-200",
		purple: "bg-purple-50 border-purple-200",
		orange: "bg-orange-50 border-orange-200",
	}
	return variants[props.variant] || variants.blue
})

const iconClass = computed(() => {
	const variants = {
		blue: "bg-blue-500 text-white",
		green: "bg-green-500 text-white",
		red: "bg-red-500 text-white",
		yellow: "bg-yellow-500 text-white",
		purple: "bg-purple-500 text-white",
		orange: "bg-orange-500 text-white",
	}
	return variants[props.variant] || variants.blue
})

const valueClass = computed(() => {
	const variants = {
		blue: "text-blue-900",
		green: "text-green-900",
		red: "text-red-900",
		yellow: "text-yellow-900",
		purple: "text-purple-900",
		orange: "text-orange-900",
	}
	return variants[props.variant] || variants.blue
})

const labelClass = computed(() => {
	const variants = {
		blue: "text-blue-700",
		green: "text-green-700",
		red: "text-red-700",
		yellow: "text-yellow-700",
		purple: "text-purple-700",
		orange: "text-orange-700",
	}
	return variants[props.variant] || variants.blue
})

const changeClass = computed(() => {
	if (props.change === null) return ""
	return props.change >= 0 ? "positive" : "negative"
})

const changeText = computed(() => {
	if (props.change === null) return ""
	const sign = props.change >= 0 ? "+" : ""
	const label = props.changeLabel || ""
	return `${sign}${props.change}% ${label}`
})
</script>

<style scoped>
.stat-card {
	@apply bg-white rounded-lg shadow-sm p-4 border border-gray-200 hover:shadow-md transition-shadow;
}
</style>
