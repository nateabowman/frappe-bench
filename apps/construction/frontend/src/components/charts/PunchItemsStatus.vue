<template>
  <div class="chart-container">
    <h3 class="text-sm font-semibold text-slate-700 mb-3">Punch Items by Status</h3>
    <apexchart
      v-if="chartOptions"
      type="donut"
      height="250"
      :options="chartOptions"
      :series="series"
    />
    <div v-else class="flex items-center justify-center h-48 text-slate-500">
      No data available
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

const series = computed(() => props.data.map(item => item.count || 0))

const chartOptions = computed(() => {
  if (!props.data || props.data.length === 0) return null
  
  const statusColors = {
    'Open': '#ef4444',
    'In Progress': '#f59e0b',
    'Completed': '#10b981',
    'On Hold': '#6b7280'
  }
  
  return {
    chart: {
      type: 'donut',
      height: 250,
      toolbar: { show: false }
    },
    labels: props.data.map(item => item.status || 'Unknown'),
    colors: props.data.map(item => statusColors[item.status] || '#6b7280'),
    legend: {
      position: 'bottom',
      fontSize: '12px'
    },
    dataLabels: {
      enabled: true,
      formatter: function (val) {
        return val.toFixed(0) + '%'
      }
    },
    plotOptions: {
      pie: {
        donut: {
          size: '65%'
        }
      }
    },
    tooltip: {
      theme: 'light',
      y: {
        formatter: function (val) {
          return val + ' items'
        }
      }
    }
  }
})
</script>

<style scoped>
.chart-container {
  @apply p-4 bg-white rounded-lg;
}
</style>
