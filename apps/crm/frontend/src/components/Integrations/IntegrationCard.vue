<template>
  <GlassCard hoverable class="glass-card">
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center gap-3">
        <div class="w-12 h-12 rounded-lg glass-subtle flex items-center justify-center">
          <FeatherIcon :name="getProviderIcon(integration.provider)" class="size-6" />
        </div>
        <div>
          <h3 class="font-semibold glass-text">{{ integration.integration_name }}</h3>
          <p class="text-sm text-ink-gray-5">{{ integration.provider }}</p>
        </div>
      </div>
      <Badge
        :label="integration.status"
        :variant="getStatusVariant(integration.status)"
      />
    </div>
    <p class="text-sm text-ink-gray-5 mb-4">{{ integration.description }}</p>
    <div class="flex gap-2">
      <Button
        v-if="integration.status === 'Disconnected'"
        size="sm"
        :label="__('Connect')"
        @click="$emit('connect', integration)"
      />
      <Button
        v-else
        variant="ghost"
        size="sm"
        :label="__('Sync')"
        @click="$emit('sync', integration)"
      />
      <Button
        variant="ghost"
        size="sm"
        :label="__('Disconnect')"
        @click="$emit('disconnect', integration)"
      />
    </div>
  </GlassCard>
</template>

<script setup>
import GlassCard from '@/components/UI/GlassCard.vue'
import { Button, FeatherIcon, Badge } from 'frappe-ui'

defineProps({
  integration: {
    type: Object,
    required: true
  }
})

defineEmits(['connect', 'disconnect', 'sync'])

const getProviderIcon = (provider) => {
  const icons = {
    'Facebook': 'facebook',
    'Twitter': 'twitter',
    'LinkedIn': 'linkedin',
    'Instagram': 'instagram',
    'Gmail': 'mail',
    'Outlook': 'mail',
    'Stripe': 'credit-card',
    'PayPal': 'credit-card',
  }
  return icons[provider] || 'plug'
}

const getStatusVariant = (status) => {
  const variants = {
    'Connected': 'success',
    'Disconnected': 'subtle',
    'Error': 'danger',
    'Pending': 'warning',
  }
  return variants[status] || 'subtle'
}
</script>
