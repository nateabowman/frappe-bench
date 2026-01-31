<template>
  <div class="space-y-6">
    <div>
      <h2 class="text-2xl font-bold text-gray-900 mb-2">{{ __('Build Custom Report') }}</h2>
      <p class="text-gray-600">{{ __('Create a custom report with filters, columns, and charts') }}</p>
    </div>

    <!-- Basic Info -->
    <div class="bg-white rounded-lg shadow p-6">
      <h3 class="text-lg font-semibold mb-4">{{ __('Basic Information') }}</h3>
      <div class="space-y-4">
        <FormControl
          v-model="config.title"
          :label="__('Report Title')"
          type="text"
          required
        />
        <FormControl
          v-model="config.doctype"
          :label="__('Document Type')"
          type="select"
          :options="doctypes"
          required
        />
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-lg shadow p-6">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-semibold">{{ __('Filters') }}</h3>
        <Button
          :label="__('Add Filter')"
          size="sm"
          @click="addFilter"
        >
          <template #prefix>
            <FeatherIcon name="plus" class="h-4" />
          </template>
        </Button>
      </div>
      <div v-if="config.filters.length === 0" class="text-gray-500 text-center py-4">
        {{ __('No filters added. Click "Add Filter" to add one.') }}
      </div>
      <div v-else class="space-y-3">
        <div
          v-for="(filter, index) in config.filters"
          :key="index"
          class="flex items-center gap-3 p-3 bg-gray-50 rounded-lg"
        >
          <FormControl
            v-model="filter.field"
            :label="__('Field')"
            type="select"
            :options="getFieldsForDoctype(config.doctype)"
            class="flex-1"
          />
          <FormControl
            v-model="filter.operator"
            :label="__('Operator')"
            type="select"
            :options="operators"
            class="flex-1"
          />
          <FormControl
            v-model="filter.value"
            :label="__('Value')"
            type="text"
            class="flex-1"
          />
          <Button
            :label="__('Remove')"
            variant="ghost"
            size="sm"
            @click="removeFilter(index)"
          >
            <template #prefix>
              <FeatherIcon name="x" class="h-4" />
            </template>
          </Button>
        </div>
      </div>
    </div>

    <!-- Columns -->
    <div class="bg-white rounded-lg shadow p-6">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-semibold">{{ __('Columns') }}</h3>
        <Button
          :label="__('Add Column')"
          size="sm"
          @click="addColumn"
        >
          <template #prefix>
            <FeatherIcon name="plus" class="h-4" />
          </template>
        </Button>
      </div>
      <div v-if="config.columns.length === 0" class="text-gray-500 text-center py-4">
        {{ __('No columns selected. Click "Add Column" to add one.') }}
      </div>
      <div v-else class="space-y-2">
        <div
          v-for="(column, index) in config.columns"
          :key="index"
          class="flex items-center gap-3 p-2 bg-gray-50 rounded"
        >
          <FormControl
            v-model="config.columns[index]"
            :label="__('Column')"
            type="select"
            :options="getFieldsForDoctype(config.doctype)"
            class="flex-1"
          />
          <Button
            :label="__('Remove')"
            variant="ghost"
            size="sm"
            @click="removeColumn(index)"
          >
            <template #prefix>
              <FeatherIcon name="x" class="h-4" />
            </template>
          </Button>
        </div>
      </div>
    </div>

    <!-- Chart Options -->
    <div class="bg-white rounded-lg shadow p-6">
      <h3 class="text-lg font-semibold mb-4">{{ __('Chart Options') }}</h3>
      <FormControl
        v-model="config.chart_type"
        :label="__('Chart Type')"
        type="select"
        :options="chartTypes"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { Button, FormControl, FeatherIcon, createResource } from 'frappe-ui'

const props = defineProps({
  modelValue: {
    type: Object,
    required: true,
  },
  doctypes: {
    type: Array,
    required: true,
  },
})

const emit = defineEmits(['update:modelValue', 'save', 'cancel'])

const config = ref({ ...props.modelValue })

watch(
  () => props.modelValue,
  (newVal) => {
    config.value = { ...newVal }
  },
  { deep: true }
)

watch(config, (newVal) => {
  emit('update:modelValue', newVal)
}, { deep: true })

const operators = [
  { label: __('Equals'), value: '=' },
  { label: __('Not Equals'), value: '!=' },
  { label: __('Greater Than'), value: '>' },
  { label: __('Less Than'), value: '<' },
  { label: __('Contains'), value: 'like' },
  { label: __('In'), value: 'in' },
]

const chartTypes = [
  { label: __('None'), value: null },
  { label: __('Bar Chart'), value: 'bar' },
  { label: __('Line Chart'), value: 'line' },
  { label: __('Pie Chart'), value: 'pie' },
]

const fieldsCache = {}

function getFieldsForDoctype(doctype) {
  if (!doctype) return []
  
  if (!fieldsCache[doctype]) {
    fieldsCache[doctype] = createResource({
      url: 'crm.api.reports.get_fields',
      makeParams: () => ({ doctype }),
      auto: true,
    })
  }
  
  return fieldsCache[doctype].data || []
}

function addFilter() {
  if (!config.value.filters) {
    config.value.filters = []
  }
  config.value.filters.push({
    field: '',
    operator: '=',
    value: '',
  })
}

function removeFilter(index) {
  config.value.filters.splice(index, 1)
}

function addColumn() {
  if (!config.value.columns) {
    config.value.columns = []
  }
  config.value.columns.push('')
}

function removeColumn(index) {
  config.value.columns.splice(index, 1)
}
</script>

