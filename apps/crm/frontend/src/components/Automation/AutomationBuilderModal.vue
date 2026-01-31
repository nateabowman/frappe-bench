<template>
  <Dialog v-model="show" :options="{ size: '4xl' }">
    <template #body>
      <div class="space-y-6">
        <div>
          <h2 class="text-2xl font-bold text-gray-900">
            {{ automation ? __('Edit Automation') : __('Create Automation') }}
          </h2>
        </div>

        <FormControl
          v-model="formData.title"
          :label="__('Title')"
          type="text"
          required
        />

        <FormControl
          v-model="formData.enabled"
          :label="__('Enabled')"
          type="checkbox"
        />

        <FormControl
          v-model="formData.trigger_type"
          :label="__('Trigger Type')"
          type="select"
          :options="triggerTypes"
          required
        />

        <FormControl
          v-model="formData.trigger_doctype"
          :label="__('Document Type')"
          type="select"
          :options="doctypes"
        />

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            {{ __('Actions') }}
          </label>
          <div class="space-y-2">
            <div
              v-for="(action, index) in formData.actions"
              :key="index"
              class="flex items-center gap-2 p-3 bg-gray-50 rounded"
            >
              <FormControl
                v-model="action.type"
                type="select"
                :options="actionTypes"
                class="flex-1"
              />
              <Button
                :label="__('Remove')"
                variant="ghost"
                size="sm"
                @click="removeAction(index)"
              >
                <template #prefix>
                  <FeatherIcon name="x" class="h-4" />
                </template>
              </Button>
            </div>
            <Button
              :label="__('Add Action')"
              size="sm"
              @click="addAction"
            >
              <template #prefix>
                <FeatherIcon name="plus" class="h-4" />
              </template>
            </Button>
          </div>
        </div>
      </div>
    </template>
    <template #actions>
      <Button :label="__('Cancel')" @click="show = false" />
      <Button
        :label="__('Save')"
        variant="solid"
        :loading="saving.loading"
        @click="save"
      />
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { Dialog, Button, FormControl, FeatherIcon, createResource, toast } from 'frappe-ui'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  automation: {
    type: Object,
    default: null,
  },
})

const emit = defineEmits(['update:modelValue', 'saved'])

const show = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val),
})

const formData = ref({
  title: '',
  enabled: true,
  trigger_type: 'On Create',
  trigger_doctype: '',
  actions: [],
})

const triggerTypes = [
  { label: __('On Create'), value: 'On Create' },
  { label: __('On Update'), value: 'On Update' },
  { label: __('Scheduled'), value: 'Scheduled' },
  { label: __('Webhook'), value: 'Webhook' },
]

const actionTypes = [
  { label: __('Update Field'), value: 'Update Field' },
  { label: __('Create Task'), value: 'Create Task' },
  { label: __('Send Email'), value: 'Send Email' },
  { label: __('Assign To'), value: 'Assign To' },
  { label: __('Change Status'), value: 'Change Status' },
  { label: __('Create Note'), value: 'Create Note' },
]

const doctypes = [
  { label: __('Lead'), value: 'CRM Lead' },
  { label: __('Deal'), value: 'CRM Deal' },
  { label: __('Contact'), value: 'CRM Contact' },
  { label: __('Organization'), value: 'CRM Organization' },
]

watch(() => props.automation, (newVal) => {
  if (newVal) {
    formData.value = { ...newVal }
  } else {
    formData.value = {
      title: '',
      enabled: true,
      trigger_type: 'On Create',
      trigger_doctype: '',
      actions: [],
    }
  }
}, { immediate: true })

function addAction() {
  formData.value.actions.push({
    type: 'Update Field',
    config: {},
  })
}

function removeAction(index) {
  formData.value.actions.splice(index, 1)
}

const saving = createResource({
  url: 'frappe.client.save',
  method: 'POST',
  onSuccess: () => {
    emit('saved')
    show.value = false
  },
})

function save() {
  if (!formData.value.title) {
    toast.error(__('Please enter a title'))
    return
  }

  const doc = {
    doctype: 'CRM Automation Rule',
    ...formData.value,
  }

  if (props.automation?.name) {
    doc.name = props.automation.name
  }

  saving.submit({ doc })
}
</script>

