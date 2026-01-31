<template>
  <div class="space-y-4">
    <div v-if="activities.loading" class="flex items-center justify-center h-64">
      <LoadingIndicator />
    </div>
    <div v-else-if="activities.data && activities.data.length > 0">
      <div
        v-for="activity in activities.data"
        :key="activity.id"
        class="glass-card p-4 mb-4"
      >
        <div class="flex items-start gap-3">
          <UserAvatar :user="activity.owner" size="sm" />
          <div class="flex-1">
            <div class="flex items-center gap-2 mb-1">
              <span class="font-medium glass-text">{{ activity.owner }}</span>
              <Badge :label="activity.type" />
              <span class="text-xs text-ink-gray-5">{{ formatTime(activity.creation) }}</span>
            </div>
            <div v-if="activity.type === 'comment'" class="text-sm text-ink-gray-7">
              {{ activity.content }}
            </div>
            <div v-else-if="activity.type === 'task'" class="text-sm text-ink-gray-7">
              {{ activity.title }} - {{ activity.status }}
            </div>
            <div v-else-if="activity.type === 'note'" class="text-sm text-ink-gray-7">
              {{ activity.title }}
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="flex flex-col items-center justify-center h-64 glass-card">
      <FeatherIcon name="activity" class="size-12 text-ink-gray-5 mb-4" />
      <p class="text-ink-gray-5">{{ __('No activities yet') }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { createResource } from 'frappe-ui'
import GlassCard from '@/components/UI/GlassCard.vue'
import UserAvatar from '@/components/UserAvatar.vue'
import LoadingIndicator from '@/components/Icons/LoadingIndicator.vue'
import { FeatherIcon, Badge } from 'frappe-ui'

const props = defineProps({
  referenceType: {
    type: String,
    default: null
  },
  referenceName: {
    type: String,
    default: null
  }
})

const activities = createResource({
  url: 'crm.api.collaboration.get_activity_feed',
  params: {
    doctype: props.referenceType,
    docname: props.referenceName,
    limit: 50
  },
  auto: true,
  transform: (data) => data || []
})

const formatTime = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diff = now - date
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)
  
  if (days > 0) return `${days}d ago`
  if (hours > 0) return `${hours}h ago`
  if (minutes > 0) return `${minutes}m ago`
  return 'Just now'
}

watch(() => [props.referenceType, props.referenceName], () => {
  activities.reload()
})
</script>
