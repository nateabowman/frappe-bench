<template>
	<div class="metric-card" :class="gradientClass">
		<div class="metric-card-value" :class="valueClass">
			{{ formattedValue }}
		</div>
		<div class="metric-card-label" :class="labelClass">
			{{ label }}
		</div>
		<div v-if="subtitle" class="metric-card-subtitle text-sm mt-1 opacity-75">
			{{ subtitle }}
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
	subtitle: {
		type: String,
		default: null,
	},
	variant: {
		type: String,
		default: "blue",
		validator: (value) => ["blue", "green", "purple", "orange", "indigo"].includes(value),
	},
	format: {
		type: String,
		default: "number",
		validator: (value) => ["number", "currency", "percentage"].includes(value),
	},
})

const gradientClass = computed(() => {
	const variants = {
		blue: "bg-gradient-to-br from-blue-50 to-blue-100",
		green: "bg-gradient-to-br from-green-50 to-green-100",
		purple: "bg-gradient-to-br from-purple-50 to-purple-100",
		orange: "bg-gradient-to-br from-orange-50 to-orange-100",
		indigo: "bg-gradient-to-br from-indigo-50 to-indigo-100",
	}
	return variants[props.variant] || variants.blue
})

const valueClass = computed(() => {
	const variants = {
		blue: "text-blue-900",
		green: "text-green-900",
		purple: "text-purple-900",
		orange: "text-orange-900",
		indigo: "text-indigo-900",
	}
	return variants[props.variant] || variants.blue
})

const labelClass = computed(() => {
	const variants = {
		blue: "text-blue-700",
		green: "text-green-700",
		purple: "text-purple-700",
		orange: "text-orange-700",
		indigo: "text-indigo-700",
	}
	return variants[props.variant] || variants.blue
})

const formattedValue = computed(() => {
	if (props.format === "currency") {
		return new Intl.NumberFormat("en-US", {
			style: "currency",
			currency: "USD",
			minimumFractionDigits: 0,
		}).format(props.value)
	} else if (props.format === "percentage") {
		return `${props.value}%`
	}
	return props.value
})
</script>

<style scoped>
.metric-card {
	@apply bg-gradient-to-br rounded-lg p-6 border border-blue-200;
}
</style>
