<template>
  <div class="space-y-4">
    <div v-if="profiles.loading" class="flex items-center justify-center h-64">
      <LoadingIndicator />
    </div>
    <div v-else-if="profiles.data && profiles.data.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <GlassCard
        v-for="profile in profiles.data"
        :key="profile.name"
        class="glass-card"
      >
        <div class="flex items-center gap-3 mb-4">
          <div class="w-12 h-12 rounded-lg glass-subtle flex items-center justify-center">
            <FeatherIcon :name="getPlatformIcon(profile.platform)" class="size-6" />
          </div>
          <div>
            <h4 class="font-semibold glass-text">{{ profile.platform }}</h4>
            <p class="text-sm text-ink-gray-5">{{ profile.username || profile.profile_url }}</p>
          </div>
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <div class="text-xs text-ink-gray-5">{{ __('Followers') }}</div>
            <div class="text-lg font-semibold">{{ formatNumber(profile.followers_count) }}</div>
          </div>
          <div>
            <div class="text-xs text-ink-gray-5">{{ __('Engagement') }}</div>
            <div class="text-lg font-semibold">{{ profile.engagement_rate || 0 }}%</div>
          </div>
        </div>
      </GlassCard>
    </div>
    <div v-else class="flex flex-col items-center justify-center h-64 glass-card">
      <FeatherIcon name="share-2" class="size-12 text-ink-gray-5 mb-4" />
      <p class="text-ink-gray-5 mb-4">{{ __('No social media profiles connected') }}</p>
      <Button
        :label="__('Add Social Profile')"
        @click="showAddProfile = true"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { createResource } from 'frappe-ui'
import GlassCard from '@/components/UI/GlassCard.vue'
import LoadingIndicator from '@/components/Icons/LoadingIndicator.vue'
import { Button, FeatherIcon } from 'frappe-ui'

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

const showAddProfile = ref(false)

const profiles = createResource({
  url: 'crm.api.integrations.get_social_profiles',
  params: {
    reference_type: props.doctype,
    reference_name: props.doc?.name
  },
  auto: true,
  transform: (data) => data || []
})

const getPlatformIcon = (platform) => {
  const icons = {
    'Facebook': 'facebook',
    'Twitter': 'twitter',
    'LinkedIn': 'linkedin',
    'Instagram': 'instagram',
  }
  return icons[platform] || 'share-2'
}

const formatNumber = (num) => {
  if (!num) return '0'
  if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M'
  if (num >= 1000) return (num / 1000).toFixed(1) + 'K'
  return num.toString()
}
</script>
