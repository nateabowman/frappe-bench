<template>
  <div class="h-full w-full p-4">
    <div class="mb-4">
      <h3 class="text-lg font-semibold text-gray-900">{{ config.title || __('Trend Analysis') }}</h3>
      <p v-if="config.description" class="text-sm text-gray-500 mt-1">{{ config.description }}</p>
    </div>
    <div class="h-48 relative">
      <svg class="w-full h-full" viewBox="0 0 400 200" preserveAspectRatio="none">
        <!-- Grid lines -->
        <defs>
          <linearGradient id="trendGradient" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" style="stop-color:rgb(14, 165, 233);stop-opacity:0.3" />
            <stop offset="100%" style="stop-color:rgb(14, 165, 233);stop-opacity:0" />
          </linearGradient>
        </defs>
        <g v-for="(line, i) in gridLines" :key="i">
          <line
            :x1="0"
            :y1="line"
            :x2="400"
            :y2="line"
            stroke="#e5e7eb"
            stroke-width="1"
          />
        </g>
        <!-- Trend line -->
        <polyline
          :points="trendPoints"
          fill="none"
          stroke="rgb(14, 165, 233)"
          stroke-width="2"
          class="transition-all duration-500"
        />
        <!-- Area under curve -->
        <polygon
          :points="areaPoints"
          fill="url(#trendGradient)"
          class="transition-all duration-500"
        />
        <!-- Data points -->
        <circle
          v-for="(point, index) in dataPoints"
          :key="index"
          :cx="point.x"
          :cy="point.y"
          r="4"
          fill="rgb(14, 165, 233)"
          class="cursor-pointer hover:r-6 transition-all"
        />
      </svg>
    </div>
    <div class="mt-4 flex items-center justify-between text-xs text-gray-600">
      <span v-for="(label, index) in config.labels" :key="index">
        {{ label }}
      </span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  config: {
    type: Object,
    required: true,
    default: () => ({
      title: '',
      description: '',
      data: [],
      labels: [],
    }),
  },
})

const maxValue = computed(() => Math.max(...props.config.data, 1))
const minValue = computed(() => Math.min(...props.config.data, 0))

const trendPoints = computed(() => {
  const points = props.config.data.map((value, index) => {
    const x = (index / (props.config.data.length - 1 || 1)) * 400
    const y = 200 - ((value - minValue.value) / (maxValue.value - minValue.value || 1)) * 180
    return `${x},${y}`
  })
  return points.join(' ')
})

const areaPoints = computed(() => {
  const base = trendPoints.value.split(' ').map(p => p.split(','))
  const bottomLeft = `0,200`
  const bottomRight = `400,200`
  return `${bottomLeft} ${trendPoints.value} ${bottomRight}`
})

const dataPoints = computed(() => {
  return props.config.data.map((value, index) => {
    const x = (index / (props.config.data.length - 1 || 1)) * 400
    const y = 200 - ((value - minValue.value) / (maxValue.value - minValue.value || 1)) * 180
    return { x, y }
  })
})

const gridLines = computed(() => {
  return [40, 80, 120, 160]
})
</script>

