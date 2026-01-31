<template>
  <div class="flex flex-col h-full overflow-hidden">
    <LayoutHeader>
      <template #left-header>
        <ViewBreadcrumbs routeName="Reports" />
      </template>
      <template #right-header>
        <Button
          v-if="!editing"
          :label="__('New Report')"
          variant="solid"
          @click="createNewReport"
        >
          <template #prefix>
            <FeatherIcon name="plus" class="h-4" />
          </template>
        </Button>
        <Button
          v-if="editing"
          :label="__('Save')"
          variant="solid"
          :loading="saving.loading"
          @click="saveReport"
        />
        <Button
          v-if="editing"
          :label="__('Cancel')"
          @click="cancelEditing"
        />
      </template>
    </LayoutHeader>

    <div class="flex-1 overflow-hidden flex">
      <!-- Reports List Sidebar -->
      <div class="w-64 border-r bg-gray-50 overflow-y-auto">
        <div class="p-4">
          <TextInput
            v-model="searchQuery"
            :placeholder="__('Search reports...')"
            class="w-full"
          >
            <template #prefix>
              <FeatherIcon name="search" class="h-4" />
            </template>
          </TextInput>
        </div>
        <div class="px-2">
          <div
            v-for="report in filteredReports"
            :key="report.name"
            class="px-3 py-2 rounded-lg cursor-pointer mb-1 transition-colors"
            :class="
              selectedReport?.name === report.name
                ? 'bg-primary-100 text-primary-700'
                : 'hover:bg-gray-100'
            "
            @click="selectReport(report)"
          >
            <div class="font-medium text-sm">{{ report.title }}</div>
            <div class="text-xs text-gray-500 mt-1">
              {{ report.doctype }}
            </div>
          </div>
        </div>
      </div>

      <!-- Report Builder/Viewer -->
      <div class="flex-1 overflow-y-auto p-6">
        <div v-if="!selectedReport && !editing" class="flex items-center justify-center h-full">
          <div class="text-center">
            <FeatherIcon name="file-text" class="h-16 w-16 text-gray-300 mx-auto mb-4" />
            <h3 class="text-lg font-semibold text-gray-700 mb-2">{{ __('No Report Selected') }}</h3>
            <p class="text-gray-500 mb-4">{{ __('Select a report from the sidebar or create a new one') }}</p>
            <Button :label="__('Create New Report')" variant="solid" @click="createNewReport" />
          </div>
        </div>

        <div v-else-if="editing">
          <ReportBuilder
            v-model="reportConfig"
            :doctypes="availableDoctypes"
            @save="saveReport"
            @cancel="cancelEditing"
          />
        </div>

        <div v-else-if="selectedReport">
          <ReportViewer :report="selectedReport" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  Button,
  TextInput,
  FeatherIcon,
  createResource,
  toast,
} from 'frappe-ui'
import LayoutHeader from '@/components/LayoutHeader.vue'
import ViewBreadcrumbs from '@/components/ViewBreadcrumbs.vue'
import ReportBuilder from '@/components/Reports/ReportBuilder.vue'
import ReportViewer from '@/components/Reports/ReportViewer.vue'
import { usePageMeta } from 'frappe-ui'

const router = useRouter()
const searchQuery = ref('')
const selectedReport = ref(null)
const editing = ref(false)
const reportConfig = ref(null)

const reports = createResource({
  url: 'crm.api.reports.get_reports',
  auto: true,
})

const availableDoctypes = [
  { value: 'CRM Lead', label: __('Lead') },
  { value: 'CRM Deal', label: __('Deal') },
  { value: 'CRM Contact', label: __('Contact') },
  { value: 'CRM Organization', label: __('Organization') },
]

const filteredReports = computed(() => {
  if (!reports.data) return []
  if (!searchQuery.value) return reports.data

  const query = searchQuery.value.toLowerCase()
  return reports.data.filter(
    (r) =>
      r.title?.toLowerCase().includes(query) ||
      r.doctype?.toLowerCase().includes(query)
  )
})

function createNewReport() {
  editing.value = true
  selectedReport.value = null
  reportConfig.value = {
    title: '',
    doctype: '',
    filters: [],
    columns: [],
    chart_type: null,
  }
}

function selectReport(report) {
  selectedReport.value = report
  editing.value = false
}

function cancelEditing() {
  editing.value = false
  reportConfig.value = null
}

const saving = createResource({
  url: 'crm.api.reports.save_report',
  method: 'POST',
  onSuccess: () => {
    toast.success(__('Report saved successfully'))
    reports.reload()
    editing.value = false
  },
})

function saveReport() {
  if (!reportConfig.value.title) {
    toast.error(__('Please enter a report title'))
    return
  }
  saving.submit({ report: reportConfig.value })
}

usePageMeta(() => {
  return { title: __('Reports') }
})
</script>

