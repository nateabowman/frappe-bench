<template>
  <div class="h-full w-full p-4">
    <div class="mb-4">
      <h3 class="text-lg font-semibold text-gray-900">{{ config.title || __('Goal Progress') }}</h3>
      <p v-if="config.description" class="text-sm text-gray-500 mt-1">{{ config.description }}</p>
    </div>
    <div class="space-y-4">
      <div
        v-for="(goal, index) in config.data"
        :key="index"
        class="space-y-2"
      >
        <div class="flex items-center justify-between">
          <span class="text-sm font-medium text-gray-700">{{ goal.label }}</span>
          <span class="text-sm font-semibold" :class="getProgressColor(goal.percentage)">
            {{ goal.current }} / {{ goal.target }}
          </span>
        </div>
        <div class="relative h-3 bg-gray-200 rounded-full overflow-hidden">
          <div
            class="absolute inset-y-0 left-0 rounded-full transition-all duration-500 flex items-center justify-end pr-2"
            :class="getProgressBgColor(goal.percentage)"
            :style="{ width: `${Math.min(goal.percentage, 100)}%` }"
          >
            <span v-if="goal.percentage > 15" class="text-xs font-medium text-white">
              {{ Math.round(goal.percentage) }}%
            </span>
          </div>
        </div>
        <div v-if="goal.deadline" class="text-xs text-gray-500">
          {{ __('Deadline') }}: {{ formatDate(goal.deadline) }}
        </div>
      </div>
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

function getProgressColor(percentage) {
  if (percentage >= 100) return 'text-success-600'
  if (percentage >= 75) return 'text-primary-600'
  if (percentage >= 50) return 'text-warning-600'
  return 'text-danger-600'
}

function getProgressBgColor(percentage) {
  if (percentage >= 100) return 'bg-success-500'
  if (percentage >= 75) return 'bg-primary-500'
  if (percentage >= 50) return 'bg-warning-500'
  return 'bg-danger-500'
}

function formatDate(date) {
  if (!date) return ''
  return new Date(date).toLocaleDateString()
}
</script>

