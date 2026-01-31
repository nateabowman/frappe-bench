<template>
  <div class="space-y-4">
    <GlassInput
      v-model="widgetData.widget_name"
      label="Widget Name"
      required
    />
    <div>
      <label class="block text-sm font-medium glass-text mb-2">
        {{ __('Widget Type') }}
      </label>
      <select
        v-model="widgetData.widget_type"
        class="glass-input w-full"
      >
        <option value="Chart">Chart</option>
        <option value="Metric">Metric</option>
        <option value="Table">Table</option>
        <option value="KPI">KPI</option>
      </select>
    </div>
    <GlassInput
      v-model="widgetData.widget_title"
      label="Widget Title"
      required
    />
    <div class="flex justify-end gap-2">
      <Button
        :label="__('Cancel')"
        @click="$emit('cancel')"
      />
      <Button
        variant="solid"
        :label="__('Save')"
        @click="handleSave"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { createResource } from 'frappe-ui'
import GlassInput from '@/components/UI/GlassInput.vue'
import { Button } from 'frappe-ui'

const props = defineProps({
  widget: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['save', 'cancel'])

const widgetData = ref({
  widget_name: props.widget?.widget_name || '',
  widget_type: props.widget?.widget_type || 'Metric',
  widget_title: props.widget?.widget_title || '',
  description: props.widget?.description || '',
})

const saveWidget = createResource({
  url: props.widget
    ? 'crm.api.analytics.update_analytics_widget'
    : 'crm.api.analytics.create_analytics_widget',
  method: 'POST',
  onSuccess: () => {
    emit('save')
  }
})

const handleSave = () => {
  saveWidget.submit({
    ...widgetData.value,
    name: props.widget?.name
  })
}
</script>
