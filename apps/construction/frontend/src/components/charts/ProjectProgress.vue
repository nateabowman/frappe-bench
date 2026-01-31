<template>
  <div class="chart-container">
    <h3 class="text-sm font-semibold text-slate-700 mb-3">Project Progress</h3>
    <apexchart
      v-if="chartOptions"
      type="bar"
      height="220"
      :options="chartOptions"
      :series="series"
    />
    <div v-else class="flex items-center justify-center h-48 text-slate-500">
      No projects available
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import VueApexCharts from 'vue-apexcharts'

const props = defineProps({
  data: {
    type: Array,
    default: () => []
  }
})

const series = computed(() => [{
  name: 'Progress',
  data: props.data.map(item => item.progress || 0)
}])

const chartOptions = computed(() => {
  if (!props.data || props.data.length === 0) return null
  
  return {
    chart: {
      type: 'bar',
      height: 220,
      toolbar: { show: false }
    },
    plotOptions: {
      bar: {
        horizontal: true,
        barHeight: '70%',
        borderRadius: 4,
        dataLabels: {
          position: 'right'
        }
      }
    },
    dataLabels: {
      enabled: true,
      formatter: function (val) {
        return val.toFixed(0) + '%'
      },
      style: {
        fontSize: '11px',
        colors: ['#1f2937']
      }
    },
    colors: ['#10b981'],
    xaxis: {
      categories: props.data.map(item => item.name || 'Unknown'),
      max: 100,
      labels: {
        style: { fontSize: '11px' },
        formatter: function (val) {
          return val + '%'
        }
      }
    },
    yaxis: {
      labels: {
        style: { fontSize: '11px' }
      }
    },
    tooltip: {
      theme: 'light',
      y: {
        formatter: function (val) {
          return val.toFixed(1) + '%'
        }
      }
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
