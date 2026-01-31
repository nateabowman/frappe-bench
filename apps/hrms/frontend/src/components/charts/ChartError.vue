<template>
	<div class="chart-error-container">
		<div class="flex flex-col items-center justify-center p-8 text-center">
			<svg
				class="w-16 h-16 text-gray-400 mb-4"
				fill="none"
				stroke="currentColor"
				viewBox="0 0 24 24"
			>
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					stroke-width="2"
					d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
				/>
			</svg>
			<h3 class="text-lg font-semibold text-gray-700 mb-2">{{ title || __("Error Loading Chart") }}</h3>
			<p class="text-sm text-gray-500 mb-4">{{ message || error }}</p>
			<Button v-if="retry" @click="retry" variant="outline" size="sm">
				{{ __("Retry") }}
			</Button>
		</div>
	</div>
</template>

<script setup>
import { inject } from "vue"
import { Button } from "frappe-ui"

const props = defineProps({
	error: {
		type: String,
		default: "",
	},
	title: {
		type: String,
		default: null,
	},
	message: {
		type: String,
		default: null,
	},
	retry: {
		type: Function,
		default: null,
	},
})

const __ = inject("$translate")
</script>

<style scoped>
.chart-error-container {
	@apply w-full min-h-[200px] flex items-center justify-center;
}
</style>
