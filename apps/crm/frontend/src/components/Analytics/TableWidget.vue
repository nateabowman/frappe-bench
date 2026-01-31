<template>
  <div class="table-widget p-4">
    <div class="text-sm text-ink-gray-5 mb-2">{{ widget.widget_title }}</div>
    <div class="text-ink-gray-7">{{ __('Table data will be displayed here') }}</div>
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
