<template>
  <div class="space-y-4">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <GlassCard class="glass-card">
        <h3 class="text-lg font-semibold glass-text mb-4">{{ __('Deal Performance') }}</h3>
        <div class="space-y-3">
          <div class="flex justify-between">
            <span class="text-ink-gray-5">{{ __('Days in Pipeline') }}</span>
            <span class="font-semibold">{{ daysInPipeline }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-ink-gray-5">{{ __('Last Activity') }}</span>
            <span class="font-semibold">{{ lastActivity }}</span>
          </div>
        </div>
      </GlassCard>
      <GlassCard class="glass-card">
        <h3 class="text-lg font-semibold glass-text mb-4">{{ __('Engagement Metrics') }}</h3>
        <div class="space-y-3">
          <div class="flex justify-between">
            <span class="text-ink-gray-5">{{ __('Total Activities') }}</span>
            <span class="font-semibold">{{ totalActivities }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-ink-gray-5">{{ __('Email Opens') }}</span>
            <span class="font-semibold">{{ emailOpens }}</span>
          </div>
        </div>
      </GlassCard>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { createResource } from 'frappe-ui'
import GlassCard from '@/components/UI/GlassCard.vue'

const props = defineProps({
  doc: {
    type: Object,
    default: null
  },
  doctype: {
    type: String,
    required: true
  }
})

const daysInPipeline = computed(() => {
  if (!props.doc?.creation) return 0
  const created = new Date(props.doc.creation)
  const now = new Date()
  return Math.floor((now - created) / (1000 * 60 * 60 * 24))
})

const lastActivity = computed(() => {
  if (!props.doc?.modified) return __('Never')
  const modified = new Date(props.doc.modified)
  const now = new Date()
  const days = Math.floor((now - modified) / (1000 * 60 * 60 * 24))
  if (days === 0) return __('Today')
  if (days === 1) return __('Yesterday')
  return `${days} ${__('days ago')}`
})

const totalActivities = ref(0)
const emailOpens = ref(0)

const activities = createResource({
  url: 'crm.api.collaboration.get_activity_feed',
  params: {
    doctype: props.doctype,
    docname: props.doc?.name,
    limit: 1000
  },
  auto: true,
  onSuccess: (data) => {
    totalActivities.value = data?.length || 0
    emailOpens.value = data?.filter(a => a.type === 'email').length || 0
  }
})
</script>
