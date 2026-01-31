<template>
  <div class="chart-container">
    <h3 class="text-sm font-semibold text-slate-700 mb-3">Activity This Week</h3>
    <apexchart
      v-if="chartOptions"
      type="bar"
      height="200"
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

const series = computed(() => [{
  name: 'Count',
  data: props.data.map(item => item.count || 0)
}])

const chartOptions = computed(() => {
  if (!props.data || props.data.length === 0) return null
  
  return {
    chart: {
      type: 'bar',
      height: 200,
      toolbar: { show: false }
    },
    plotOptions: {
      bar: {
        horizontal: false,
        columnWidth: '60%',
        borderRadius: 4
      }
    },
    dataLabels: {
      enabled: true,
      formatter: function (val) {
        return val.toString()
      }
    },
    colors: ['#3b82f6', '#10b981', '#f59e0b'],
    xaxis: {
      categories: props.data.map(item => item.type || 'Unknown'),
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
