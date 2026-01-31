<template>
	<div class="chart-loading-container">
		<div class="flex flex-col items-center justify-center p-8">
			<div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
			<p class="text-sm text-gray-600">{{ message || __("Loading chart data...") }}</p>
		</div>
	</div>
</template>

<script setup>
import { inject } from "vue"

const props = defineProps({
	message: {
		type: String,
		default: null,
	},
})

const __ = inject("$translate")
</script>

<style scoped>
.chart-loading-container {
	@apply w-full min-h-[200px] flex items-center justify-center;
}
</style>
