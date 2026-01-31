<template>
  <div class="chart-container">
    <h3 class="text-sm font-semibold text-slate-700 mb-3">Daily Logs Trend (Last 30 Days)</h3>
    <apexchart
      v-if="chartOptions"
      type="area"
      height="200"
      :options="chartOptions"
      :series="series"
    />
    <div v-else class="flex items-center justify-center h-48 text-slate-500">
      Loading chart data...
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import VueApexCharts from 'vue-apexcharts'

const props = defineProps({
  data: {
    type: Array,
    default: () => []
  }
})

const series = computed(() => [{
  name: 'Daily Logs',
  data: props.data.map(item => item.count || 0)
}])

const chartOptions = computed(() => {
  if (!props.data || props.data.length === 0) return null
  
  return {
    chart: {
      type: 'area',
      height: 200,
      toolbar: { show: false },
      zoom: { enabled: false }
    },
    dataLabels: { enabled: false },
    stroke: {
      curve: 'smooth',
      width: 2
    },
    fill: {
      type: 'gradient',
      gradient: {
        shadeIntensity: 1,
        opacityFrom: 0.7,
        opacityTo: 0.3,
        stops: [0, 90, 100]
      }
    },
    colors: ['#3b82f6'],
    xaxis: {
      categories: props.data.map(item => {
        const date = new Date(item.date)
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
      }),
      labels: {
        style: { fontSize: '11px' }
      }
    },
    yaxis: {
      labels: {
        style: { fontSize: '11px' }
      }
    },
    tooltip: {
      theme: 'light'
    },
    grid: {
      borderColor: '#e5e7eb',
      strokeDashArray: 3
    }
  }
})
</script>

<style scoped>
.chart-container {
  @apply p-4 bg-white rounded-lg;
}
</style>
