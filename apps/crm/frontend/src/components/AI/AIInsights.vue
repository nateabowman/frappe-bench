<template>
  <div class="space-y-4">
    <div v-if="insights.loading" class="flex items-center justify-center h-64">
      <LoadingIndicator />
    </div>
    <div v-else-if="insights.data && insights.data.length > 0">
      <GlassCard
        v-for="insight in insights.data"
        :key="insight.name"
        class="glass-card mb-4"
      >
        <div class="flex items-start justify-between mb-2">
          <div>
            <h4 class="font-semibold glass-text">{{ insight.insight_title }}</h4>
            <Badge :label="insight.insight_type" class="mt-1" />
          </div>
          <div class="text-right">
            <div class="text-sm text-ink-gray-5">
              {{ __('Confidence') }}: {{ Math.round(insight.confidence_score * 100) }}%
            </div>
          </div>
        </div>
        <p class="text-sm text-ink-gray-7 mb-3">{{ insight.insight_description }}</p>
        <div v-if="insight.next_best_action" class="glass-subtle rounded-lg p-3">
          <div class="text-sm font-medium glass-text mb-1">{{ __('Next Best Action') }}</div>
          <div class="text-sm text-ink-gray-7">{{ insight.next_best_action }}</div>
        </div>
        <div v-if="insight.health_score" class="mt-3">
          <div class="flex items-center justify-between mb-1">
            <span class="text-sm text-ink-gray-5">{{ __('Health Score') }}</span>
            <span class="text-sm font-medium">{{ Math.round(insight.health_score) }}%</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div
              class="h-2 rounded-full transition-all"
              :class="getHealthScoreColor(insight.health_score)"
              :style="{ width: insight.health_score + '%' }"
            />
          </div>
        </div>
      </GlassCard>
    </div>
    <div v-else class="flex flex-col items-center justify-center h-64 glass-card">
      <FeatherIcon name="brain" class="size-12 text-ink-gray-5 mb-4" />
      <p class="text-ink-gray-5 mb-4">{{ __('No insights available') }}</p>
      <Button
        :label="__('Generate Insights')"
        @click="generateInsights"
      />
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

const insights = createResource({
  url: 'crm.api.ai.get_ai_insights',
  params: {
    reference_type: props.referenceType,
    reference_name: props.referenceName
  },
  auto: true,
  transform: (data) => data || []
})

const generateInsight = createResource({
  url: 'crm.api.ai.generate_ai_insight',
  method: 'POST',
  onSuccess: () => {
    insights.reload()
  }
})

const generateInsights = () => {
  generateInsight.submit({
    reference_type: props.referenceType,
    reference_name: props.referenceName,
    insight_type: 'Predictive Analytics'
  })
}

const getHealthScoreColor = (score) => {
  if (score >= 70) return 'bg-success-500'
  if (score >= 40) return 'bg-warning-500'
  return 'bg-danger-500'
}
</script>
