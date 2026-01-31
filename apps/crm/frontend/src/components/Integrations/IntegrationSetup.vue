<template>
  <div class="space-y-4">
    <GlassInput
      v-model="integrationData.integration_name"
      label="Integration Name"
      required
    />
    <div>
      <label class="block text-sm font-medium glass-text mb-2">
        {{ __('Integration Type') }}
      </label>
      <select
        v-model="integrationData.integration_type"
        class="glass-input w-full"
      >
        <option value="Social Media">Social Media</option>
        <option value="Email Provider">Email Provider</option>
        <option value="Payment Gateway">Payment Gateway</option>
        <option value="Marketing Tool">Marketing Tool</option>
      </select>
    </div>
    <div>
      <label class="block text-sm font-medium glass-text mb-2">
        {{ __('Provider') }}
      </label>
      <select
        v-model="integrationData.provider"
        class="glass-input w-full"
      >
        <option value="Facebook">Facebook</option>
        <option value="Twitter">Twitter</option>
        <option value="LinkedIn">LinkedIn</option>
        <option value="Gmail">Gmail</option>
        <option value="Outlook">Outlook</option>
      </select>
    </div>
    <GlassInput
      v-model="integrationData.api_key"
      label="API Key"
      type="password"
    />
    <div class="flex justify-end gap-2">
      <Button
        :label="__('Cancel')"
        @click="$emit('cancel')"
      />
      <Button
        variant="solid"
        :label="__('Save')"
        @click="handleSave"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { createResource } from 'frappe-ui'
import GlassInput from '@/components/UI/GlassInput.vue'
import { Button } from 'frappe-ui'

const emit = defineEmits(['save', 'cancel'])

const integrationData = ref({
  integration_name: '',
  integration_type: 'Social Media',
  provider: 'Facebook',
  api_key: '',
})

const saveIntegration = createResource({
  url: 'crm.api.integrations.create_integration',
  method: 'POST',
  onSuccess: () => {
    emit('save')
  }
})

const handleSave = () => {
  saveIntegration.submit(integrationData.value)
}
</script>
