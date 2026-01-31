<template>
  <div class="chart-widget p-4 bg-white rounded-lg shadow-sm border border-gray-200">
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-sm font-semibold text-gray-900">{{ widget.widget_title }}</h3>
      <div v-if="widget.chart_type" class="text-xs text-gray-500 px-2 py-1 bg-gray-100 rounded">
        {{ widget.chart_type }}
      </div>
    </div>
    
    <div v-if="loading" class="flex items-center justify-center h-48">
      <div class="animate-spin rounded-full h-8 w-8 border-2 border-primary-500 border-t-transparent"></div>
    </div>
    
    <div v-else-if="error" class="text-red-500 text-sm p-4">
      {{ error }}
    </div>
    
    <div v-else-if="chartData">
      <AxisChart
        v-if="widget.chart_type === 'bar' || widget.chart_type === 'line'"
        :config="chartConfig"
      />
      <DonutChart
        v-else-if="widget.chart_type === 'pie' || widget.chart_type === 'donut'"
        :config="chartConfig"
      />
      <div v-else class="text-gray-500 text-sm p-4 text-center">
        Chart type "{{ widget.chart_type }}" not yet supported
      </div>
    </div>
    
    <div v-else class="text-gray-500 text-sm p-4 text-center">
      No data available
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { createResource, AxisChart, DonutChart } from 'frappe-ui'

const props = defineProps({
  widget: {
    type: Object,
    required: true
  }
})

const loading = ref(false)
const error = ref(null)
const chartData = ref(null)

const chartConfig = computed(() => {
  if (!chartData.value) return null
  
  return {
    labels: chartData.value.labels || [],
    datasets: chartData.value.datasets || [{
      values: chartData.value.values || []
    }]
  }
})

onMounted(async () => {
  if (!props.widget.query_name) return
  
  loading.value = true
  error.value = null
  
  try {
    const response = await fetch(`/api/method/crm.api.analytics.get_widget_data`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        widget_name: props.widget.name,
        query_name: props.widget.query_name
      })
    })
    
    const result = await response.json()
    
    if (result.message) {
      chartData.value = result.message
    } else {
      error.value = 'Failed to load chart data'
    }
  } catch (e) {
    error.value = 'Error loading chart data'
    console.error('Chart widget error:', e)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.chart-widget {
  min-height: 200px;
}
</style>
