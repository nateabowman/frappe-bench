<template>
  <div class="space-y-4">
    <div v-if="recommendations.loading" class="flex items-center justify-center h-64">
      <LoadingIndicator />
    </div>
    <div v-else-if="recommendations.data && recommendations.data.length > 0">
      <GlassCard
        v-for="(rec, index) in recommendations.data"
        :key="index"
        class="glass-card mb-4"
      >
        <div class="flex items-start gap-3">
          <div class="flex-shrink-0">
            <div
              class="w-8 h-8 rounded-full flex items-center justify-center glass-gradient-primary"
            >
              <FeatherIcon name="lightbulb" class="size-4 text-white" />
            </div>
          </div>
          <div class="flex-1">
            <h4 class="font-semibold glass-text mb-1">{{ rec.title }}</h4>
            <p class="text-sm text-ink-gray-7 mb-2">{{ rec.description }}</p>
            <div class="flex items-center gap-2">
              <Badge
                :label="rec.priority"
                :variant="getPriorityVariant(rec.priority)"
              />
              <Button
                v-if="rec.action"
                size="sm"
                :label="rec.action"
                @click="executeAction(rec)"
              />
            </div>
          </div>
        </div>
      </GlassCard>
    </div>
    <div v-else class="flex flex-col items-center justify-center h-64 glass-card">
      <FeatherIcon name="sparkles" class="size-12 text-ink-gray-5 mb-4" />
      <p class="text-ink-gray-5">{{ __('No recommendations available') }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { createResource } from 'frappe-ui'
import GlassCard from '@/components/UI/GlassCard.vue'
import LoadingIndicator from '@/components/Icons/LoadingIndicator.vue'
import { Button, FeatherIcon, Badge } from 'frappe-ui'

const props = defineProps({
  referenceType: {
    type: String,
    required: true
  },
  referenceName: {
    type: String,
    required: true
  }
})

const recommendations = createResource({
  url: 'crm.api.ai.get_recommendations',
  params: {
    reference_type: props.referenceType,
    reference_name: props.referenceName
  },
  auto: true,
  transform: (data) => data.recommendations || []
})

const getPriorityVariant = (priority) => {
  const variants = {
    'high': 'danger',
    'medium': 'warning',
    'low': 'subtle'
  }
  return variants[priority] || 'subtle'
}

const executeAction = (rec) => {
  // Implement action execution
  console.log('Executing action:', rec.action)
}
</script>
