<template>
  <div class="space-y-4">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <GlassCard class="glass-card">
        <div class="text-sm text-ink-gray-5 mb-1">{{ __('Deal Value') }}</div>
        <div class="text-2xl font-bold glass-text">
          {{ formatCurrency(doc?.deal_value || 0) }}
        </div>
      </GlassCard>
      <GlassCard class="glass-card">
        <div class="text-sm text-ink-gray-5 mb-1">{{ __('Probability') }}</div>
        <div class="text-2xl font-bold glass-text">
          {{ doc?.probability || 0 }}%
        </div>
      </GlassCard>
      <GlassCard class="glass-card">
        <div class="text-sm text-ink-gray-5 mb-1">{{ __('Expected Close Date') }}</div>
        <div class="text-2xl font-bold glass-text">
          {{ formatDate(doc?.expected_closure_date) || __('Not set') }}
        </div>
      </GlassCard>
    </div>
    <Recommendations
      :reference-type="doctype"
      :reference-name="doc?.name"
    />
  </div>
</template>

<script setup>
import { formatCurrency, formatDate } from '@/utils'
import GlassCard from '@/components/UI/GlassCard.vue'
import Recommendations from '@/components/AI/Recommendations.vue'

defineProps({
  doc: {
    type: Object,
    default: null
  },
  doctype: {
    type: String,
    required: true
  }
})
</script>
