<template>
  <div class="metric-widget">
    <div class="text-3xl font-bold glass-text">{{ value }}</div>
    <div class="text-sm text-ink-gray-5 mt-2">{{ label }}</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { createResource } from 'frappe-ui'

const props = defineProps({
  widget: {
    type: Object,
    required: true
  }
})

const value = ref(0)
const label = ref(props.widget.widget_title)

const widgetData = createResource({
  url: 'crm.api.analytics.get_widget_data',
  params: { widget_name: props.widget.name },
  auto: true,
  onSuccess: (data) => {
    if (data.data && data.data.length > 0) {
      value.value = data.data[0].value || 0
    }
  }
})
</script>

<style scoped>
.metric-widget {
  @apply p-4;
}
</style>
