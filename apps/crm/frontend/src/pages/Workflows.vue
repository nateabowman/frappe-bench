<template>
  <div class="flex flex-col h-full overflow-hidden">
    <LayoutHeader>
      <template #left-header>
        <ViewBreadcrumbs routeName="Workflows" />
      </template>
      <template #right-header>
        <Button
          :label="__('New Workflow')"
          @click="showWorkflowBuilder = true"
        >
          <template #prefix>
            <FeatherIcon name="plus" class="size-4" />
          </template>
        </Button>
      </template>
    </LayoutHeader>

    <div class="flex-1 overflow-auto p-6 glass-scrollbar">
      <div v-if="workflows.loading" class="flex items-center justify-center h-64">
        <LoadingIndicator />
      </div>
      <div v-else-if="workflows.data && workflows.data.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <GlassCard
          v-for="workflow in workflows.data"
          :key="workflow.name"
          hoverable
          class="glass-card"
        >
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold glass-text">{{ workflow.template_name }}</h3>
            <Badge :label="workflow.workflow_type" />
          </div>
          <p class="text-ink-gray-5 mb-4">{{ workflow.description }}</p>
          <div class="flex gap-2">
            <Button
              variant="ghost"
              size="sm"
              @click="editWorkflow(workflow)"
            >
              {{ __('Edit') }}
            </Button>
            <Button
              variant="ghost"
              size="sm"
              @click="executeWorkflow(workflow)"
            >
              {{ __('Execute') }}
            </Button>
          </div>
        </GlassCard>
      </div>
      <div v-else class="flex flex-col items-center justify-center h-64 glass-card">
        <FeatherIcon name="workflow" class="size-12 text-ink-gray-5 mb-4" />
        <p class="text-ink-gray-5 mb-4">{{ __('No workflows yet') }}</p>
        <Button
          :label="__('Create Your First Workflow')"
          @click="showWorkflowBuilder = true"
        />
      </div>
    </div>

    <WorkflowBuilder
      v-if="showWorkflowBuilder"
      v-model="showWorkflowBuilder"
      :workflow="editingWorkflow"
      @save="handleWorkflowSave"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { createResource } from 'frappe-ui'
import LayoutHeader from '@/components/LayoutHeader.vue'
import ViewBreadcrumbs from '@/components/ViewBreadcrumbs.vue'
import GlassCard from '@/components/UI/GlassCard.vue'
import WorkflowBuilder from '@/components/Workflow/WorkflowBuilder.vue'
import LoadingIndicator from '@/components/Icons/LoadingIndicator.vue'
import { Button, FeatherIcon, Badge } from 'frappe-ui'

const showWorkflowBuilder = ref(false)
const editingWorkflow = ref(null)

const workflows = createResource({
  url: 'crm.api.workflow.get_workflow_templates',
  auto: true,
  transform: (data) => data || []
})

const editWorkflow = (workflow) => {
  editingWorkflow.value = workflow
  showWorkflowBuilder.value = true
}

const executeWorkflow = (workflow) => {
  // Implement execute logic
}

const handleWorkflowSave = () => {
  showWorkflowBuilder.value = false
  editingWorkflow.value = null
  workflows.reload()
}
</script>
