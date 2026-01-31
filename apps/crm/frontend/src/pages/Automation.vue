<template>
  <div class="flex flex-col h-full overflow-hidden">
    <LayoutHeader>
      <template #left-header>
        <ViewBreadcrumbs routeName="Automation" />
      </template>
      <template #right-header>
        <Button
          :label="__('New Automation')"
          variant="solid"
          @click="createNewAutomation"
        >
          <template #prefix>
            <FeatherIcon name="plus" class="h-4" />
          </template>
        </Button>
      </template>
    </LayoutHeader>

    <div class="flex-1 overflow-y-auto p-6">
      <div v-if="automations.loading" class="flex items-center justify-center py-12">
        <div class="animate-spin rounded-full h-8 w-8 border-2 border-primary-500 border-t-transparent"></div>
      </div>

      <div v-else-if="automations.data?.length === 0" class="text-center py-12">
        <FeatherIcon name="zap" class="h-16 w-16 text-gray-300 mx-auto mb-4" />
        <h3 class="text-lg font-semibold text-gray-700 mb-2">{{ __('No Automations') }}</h3>
        <p class="text-gray-500 mb-4">{{ __('Create your first automation to streamline workflows') }}</p>
        <Button :label="__('Create Automation')" variant="solid" @click="createNewAutomation" />
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="automation in automations.data"
          :key="automation.name"
          class="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow cursor-pointer"
          @click="editAutomation(automation)"
        >
          <div class="flex items-start justify-between mb-4">
            <h3 class="text-lg font-semibold text-gray-900">{{ automation.title }}</h3>
            <Badge
              :label="automation.enabled ? __('Enabled') : __('Disabled')"
              :variant="automation.enabled ? 'success' : 'subtle'"
            />
          </div>
          <p class="text-sm text-gray-600 mb-4">{{ automation.description || __('No description') }}</p>
          <div class="flex items-center gap-2 text-xs text-gray-500">
            <FeatherIcon name="zap" class="h-4" />
            <span>{{ automation.trigger_type }}</span>
          </div>
        </div>
      </div>
    </div>

    <AutomationBuilderModal
      v-if="showBuilder"
      v-model="showBuilder"
      :automation="selectedAutomation"
      @saved="handleSaved"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Button, FeatherIcon, Badge, createResource, toast } from 'frappe-ui'
import LayoutHeader from '@/components/LayoutHeader.vue'
import ViewBreadcrumbs from '@/components/ViewBreadcrumbs.vue'
import AutomationBuilderModal from '@/components/Automation/AutomationBuilderModal.vue'
import { usePageMeta } from 'frappe-ui'

const showBuilder = ref(false)
const selectedAutomation = ref(null)

const automations = createResource({
  url: 'frappe.client.get_list',
  makeParams: () => ({
    doctype: 'CRM Automation Rule',
    fields: ['name', 'title', 'enabled', 'trigger_type', 'description'],
    order_by: 'modified desc',
  }),
  auto: true,
})

function createNewAutomation() {
  selectedAutomation.value = null
  showBuilder.value = true
}

function editAutomation(automation) {
  selectedAutomation.value = automation
  showBuilder.value = true
}

function handleSaved() {
  automations.reload()
  showBuilder.value = false
  toast.success(__('Automation saved successfully'))
}

usePageMeta(() => {
  return { title: __('Automation') }
})
</script>

