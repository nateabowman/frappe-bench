<template>
  <div class="flex flex-col h-full overflow-hidden">
    <LayoutHeader>
      <template #left-header>
        <ViewBreadcrumbs routeName="Integrations" />
      </template>
      <template #right-header>
        <Button
          :label="__('Add Integration')"
          @click="showAddIntegrationModal = true"
        >
          <template #prefix>
            <FeatherIcon name="plus" class="size-4" />
          </template>
        </Button>
      </template>
    </LayoutHeader>

    <div class="flex-1 overflow-auto p-6 glass-scrollbar">
      <div v-if="integrations.loading" class="flex items-center justify-center h-64">
        <LoadingIndicator />
      </div>
      <div v-else-if="integrations.data && integrations.data.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <IntegrationCard
          v-for="integration in integrations.data"
          :key="integration.name"
          :integration="integration"
          @connect="handleConnect"
          @disconnect="handleDisconnect"
          @sync="handleSync"
        />
      </div>
      <div v-else class="flex flex-col items-center justify-center h-64 glass-card">
        <FeatherIcon name="plug" class="size-12 text-ink-gray-5 mb-4" />
        <p class="text-ink-gray-5 mb-4">{{ __('No integrations yet') }}</p>
        <Button
          :label="__('Add Your First Integration')"
          @click="showAddIntegrationModal = true"
        />
      </div>
    </div>

    <GlassModal
      v-model="showAddIntegrationModal"
      title="Add Integration"
      size="lg"
    >
      <IntegrationSetup
        @save="handleIntegrationSave"
        @cancel="showAddIntegrationModal = false"
      />
    </GlassModal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { createResource } from 'frappe-ui'
import LayoutHeader from '@/components/LayoutHeader.vue'
import ViewBreadcrumbs from '@/components/ViewBreadcrumbs.vue'
import IntegrationCard from '@/components/Integrations/IntegrationCard.vue'
import IntegrationSetup from '@/components/Integrations/IntegrationSetup.vue'
import GlassModal from '@/components/UI/GlassModal.vue'
import LoadingIndicator from '@/components/Icons/LoadingIndicator.vue'
import { Button, FeatherIcon } from 'frappe-ui'

const showAddIntegrationModal = ref(false)

const integrations = createResource({
  url: 'crm.api.integrations.get_integrations',
  auto: true,
  transform: (data) => data || []
})

const handleConnect = (integration) => {
  // Implement connect logic
  integrations.reload()
}

const handleDisconnect = (integration) => {
  // Implement disconnect logic
  integrations.reload()
}

const handleSync = (integration) => {
  // Implement sync logic
}

const handleIntegrationSave = () => {
  showAddIntegrationModal.value = false
  integrations.reload()
}
</script>
