<template>
  <GlassModal
    v-model="modelValue"
    title="Workflow Builder"
    size="xl"
  >
    <div class="space-y-4">
      <GlassInput
        v-model="workflowData.template_name"
        label="Template Name"
        required
      />
      <div>
        <label class="block text-sm font-medium glass-text mb-2">
          {{ __('Workflow Type') }}
        </label>
        <select
          v-model="workflowData.workflow_type"
          class="glass-input w-full"
        >
          <option value="Automation">Automation</option>
          <option value="Process">Process</option>
          <option value="Approval">Approval</option>
          <option value="Notification">Notification</option>
        </select>
      </div>
      <GlassInput
        v-model="workflowData.description"
        label="Description"
      />
      <div class="flex justify-end gap-2">
        <Button
          :label="__('Cancel')"
          @click="$emit('update:modelValue', false)"
        />
        <Button
          variant="solid"
          :label="__('Save')"
          @click="handleSave"
        />
      </div>
    </div>
  </GlassModal>
</template>

<script setup>
import { ref, watch } from 'vue'
import { createResource } from 'frappe-ui'
import GlassModal from '@/components/UI/GlassModal.vue'
import GlassInput from '@/components/UI/GlassInput.vue'
import { Button } from 'frappe-ui'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  workflow: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['update:modelValue', 'save'])

const workflowData = ref({
  template_name: props.workflow?.template_name || '',
  workflow_type: props.workflow?.workflow_type || 'Automation',
  description: props.workflow?.description || '',
})

watch(() => props.workflow, (newWorkflow) => {
  if (newWorkflow) {
    workflowData.value = {
      template_name: newWorkflow.template_name || '',
      workflow_type: newWorkflow.workflow_type || 'Automation',
      description: newWorkflow.description || '',
    }
  }
}, { immediate: true })

const saveWorkflow = createResource({
  url: props.workflow
    ? 'crm.api.workflow.update_workflow_template'
    : 'crm.api.workflow.create_workflow_template',
  method: 'POST',
  onSuccess: () => {
    emit('save')
    emit('update:modelValue', false)
  }
})

const handleSave = () => {
  saveWorkflow.submit({
    ...workflowData.value,
    name: props.workflow?.name
  })
}
</script>
