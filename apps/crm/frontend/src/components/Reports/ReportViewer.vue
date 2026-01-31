<template>
  <div class="space-y-6">
    <div>
      <h2 class="text-2xl font-bold text-gray-900">{{ report.title }}</h2>
      <p class="text-gray-500 mt-1">{{ report.doctype }}</p>
    </div>

    <div v-if="reportData.loading" class="flex items-center justify-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-2 border-primary-500 border-t-transparent"></div>
    </div>

    <div v-else-if="reportData.data">
      <!-- Chart -->
      <div v-if="reportData.data.config?.chart_type" class="bg-white rounded-lg shadow p-6 mb-6">
        <AxisChart
          v-if="reportData.data.config.chart_type === 'bar' || reportData.data.config.chart_type === 'line'"
          :config="getChartConfig(reportData.data)"
        />
        <DonutChart
          v-else-if="reportData.data.config.chart_type === 'pie'"
          :config="getChartConfig(reportData.data)"
        />
      </div>

      <!-- Data Table -->
      <div class="bg-white rounded-lg shadow overflow-hidden">
        <div class="px-6 py-4 border-b flex items-center justify-between">
          <h3 class="text-lg font-semibold">{{ __('Report Data') }}</h3>
          <div class="flex gap-2">
            <Button
              :label="__('Export CSV')"
              size="sm"
              @click="exportCSV"
            >
              <template #prefix>
                <FeatherIcon name="download" class="h-4" />
              </template>
            </Button>
            <Button
              :label="__('Export PDF')"
              size="sm"
              @click="exportPDF"
            >
              <template #prefix>
                <FeatherIcon name="file" class="h-4" />
              </template>
            </Button>
          </div>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-gray-50">
              <tr>
                <th
                  v-for="column in reportData.data.config?.columns || []"
                  :key="column"
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  {{ column }}
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr
                v-for="(row, index) in reportData.data.data"
                :key="index"
                class="hover:bg-gray-50"
              >
                <td
                  v-for="column in reportData.data.config?.columns || []"
                  :key="column"
                  class="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
                >
                  {{ row[column] || '-' }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-if="reportData.data.data.length === 0" class="text-center py-12 text-gray-500">
          {{ __('No data found') }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { createResource } from 'frappe-ui'
import { Button, FeatherIcon, AxisChart, DonutChart, toast } from 'frappe-ui'

const props = defineProps({
  report: {
    type: Object,
    required: true,
  },
})

const reportData = createResource({
  url: 'crm.api.reports.get_report_data',
  makeParams: () => ({ report_name: props.report.name }),
  auto: true,
})

function getChartConfig(data) {
  // Simplified chart config - would need proper data transformation
  return {
    labels: data.data.map((_, i) => `Item ${i + 1}`),
    datasets: [
      {
        values: data.data.map((row) => {
          const firstCol = data.config?.columns?.[0]
          return row[firstCol] || 0
        }),
      },
    ],
  }
}

function exportCSV() {
  if (!reportData.data?.data) return

  const headers = reportData.data.config?.columns || []
  const rows = reportData.data.data.map((row) =>
    headers.map((col) => row[col] || '').join(',')
  )

  const csv = [headers.join(','), ...rows].join('\n')
  const blob = new Blob([csv], { type: 'text/csv' })
  const url = window.URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${props.report.title}.csv`
  a.click()
  window.URL.revokeObjectURL(url)

  toast.success(__('CSV exported successfully'))
}

function exportPDF() {
  toast.info(__('PDF export coming soon'))
}
</script>

