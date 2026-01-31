<template>
  <div class="kpi-widget p-4">
    <div class="text-sm text-ink-gray-5 mb-2">{{ widget.widget_title }}</div>
    <div class="text-2xl font-bold glass-text">{{ __('KPI') }}</div>
  </div>
</template>

<script setup>
defineProps({
  widget: {
    type: Object,
    required: true
  }
})
</script>
