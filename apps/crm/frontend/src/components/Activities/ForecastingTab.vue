<template>
  <div class="space-y-4">
    <GlassCard class="glass-card">
      <h3 class="text-lg font-semibold glass-text mb-4">{{ __('Revenue Forecast') }}</h3>
      <div class="space-y-3">
        <div class="flex justify-between items-center">
          <span class="text-ink-gray-5">{{ __('Weighted Revenue') }}</span>
          <span class="text-xl font-bold glass-text">
            {{ formatCurrency(forecastData?.total_weighted_revenue || 0) }}
          </span>
        </div>
        <div class="flex justify-between items-center">
          <span class="text-ink-gray-5">{{ __('Total Deals') }}</span>
          <span class="text-lg font-semibold">{{ forecastData?.total_deals || 0 }}</span>
        </div>
      </div>
    </GlassCard>
    <GlassCard class="glass-card">
      <h3 class="text-lg font-semibold glass-text mb-4">{{ __('Monthly Breakdown') }}</h3>
      <div class="space-y-2">
        <div
          v-for="(value, month) in forecastData?.monthly_breakdown"
          :key="month"
          class="flex justify-between items-center"
        >
          <span class="text-ink-gray-5">{{ month }}</span>
          <span class="font-semibold">{{ formatCurrency(value) }}</span>
        </div>
      </div>
    </GlassCard>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { createResource } from 'frappe-ui'
import { formatCurrency } from '@/utils'
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

const forecastData = createResource({
  url: 'crm.api.analytics.get_revenue_forecast',
  params: {
    user: props.doc?.deal_owner
  },
  auto: true,
  transform: (data) => data || {}
})
</script>
