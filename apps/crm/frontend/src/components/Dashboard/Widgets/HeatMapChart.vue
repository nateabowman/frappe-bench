<template>
  <div class="h-full w-full p-4">
    <div class="mb-4">
      <h3 class="text-lg font-semibold text-gray-900">{{ config.title || __('Activity Heat Map') }}</h3>
      <p v-if="config.description" class="text-sm text-gray-500 mt-1">{{ config.description }}</p>
    </div>
    <div class="grid grid-cols-7 gap-1">
      <div
        v-for="(day, index) in config.data"
        :key="index"
        class="aspect-square rounded"
        :class="getIntensityClass(day.value)"
        :title="`${day.label}: ${day.value}`"
      />
    </div>
    <div class="mt-4 flex items-center justify-between text-xs text-gray-500">
      <span>{{ __('Less') }}</span>
      <div class="flex gap-1">
        <div class="w-3 h-3 rounded bg-gray-200"></div>
        <div class="w-3 h-3 rounded bg-gray-400"></div>
        <div class="w-3 h-3 rounded bg-primary-300"></div>
        <div class="w-3 h-3 rounded bg-primary-500"></div>
        <div class="w-3 h-3 rounded bg-primary-700"></div>
      </div>
      <span>{{ __('More') }}</span>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  config: {
    type: Object,
    required: true,
    default: () => ({
      title: '',
      description: '',
      data: [],
    }),
  },
})

function getIntensityClass(value) {
  const max = Math.max(...props.config.data.map(d => d.value))
  const intensity = value / max
  
  if (intensity === 0) return 'bg-gray-100'
  if (intensity < 0.2) return 'bg-gray-200'
  if (intensity < 0.4) return 'bg-gray-400'
  if (intensity < 0.6) return 'bg-primary-300'
  if (intensity < 0.8) return 'bg-primary-500'
  return 'bg-primary-700'
}
</script>

