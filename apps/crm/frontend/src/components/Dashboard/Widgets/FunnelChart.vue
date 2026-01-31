<template>
  <div class="h-full w-full p-4">
    <div class="mb-4">
      <h3 class="text-lg font-semibold text-gray-900">{{ config.title || __('Funnel') }}</h3>
      <p v-if="config.description" class="text-sm text-gray-500 mt-1">{{ config.description }}</p>
    </div>
    <div class="flex flex-col gap-2">
      <div
        v-for="(stage, index) in config.data"
        :key="index"
        class="relative"
      >
        <div class="flex items-center justify-between mb-1">
          <span class="text-sm font-medium text-gray-700">{{ stage.label }}</span>
          <span class="text-sm text-gray-600">{{ stage.value }} ({{ stage.percentage }}%)</span>
        </div>
        <div class="relative h-8 bg-gray-200 rounded-lg overflow-hidden">
          <div
            class="absolute inset-y-0 left-0 bg-gradient-to-r from-primary-500 to-primary-600 rounded-lg transition-all duration-500 flex items-center justify-end pr-2"
            :style="{ width: `${stage.percentage}%` }"
          >
            <span v-if="stage.percentage > 10" class="text-xs font-medium text-white">
              {{ stage.percentage }}%
            </span>
          </div>
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
</script>

