<template>
  <div class="flex flex-col h-full">
    <div class="flex-1 overflow-y-auto glass-scrollbar p-4 space-y-4">
      <div
        v-for="message in messages"
        :key="message.id"
        class="flex"
        :class="message.role === 'user' ? 'justify-end' : 'justify-start'"
      >
        <div
          class="glass-card max-w-[80%] p-3"
          :class="message.role === 'user' ? 'glass-gradient-primary' : ''"
        >
          <p class="text-sm">{{ message.content }}</p>
          <div class="text-xs text-ink-gray-5 mt-1">
            {{ formatTime(message.timestamp) }}
          </div>
        </div>
      </div>
      <div v-if="loading" class="flex justify-start">
        <div class="glass-card p-3">
          <LoadingIndicator />
        </div>
      </div>
    </div>
    <div class="border-t border-glass-border p-4">
      <form @submit.prevent="sendMessage" class="flex gap-2">
        <GlassInput
          v-model="inputMessage"
          :placeholder="__('Ask a question about this record...')"
          class="flex-1"
        />
        <GlassButton
          type="submit"
          :loading="loading"
          :disabled="!inputMessage.trim()"
        >
          <FeatherIcon name="send" class="size-4" />
        </GlassButton>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { createResource } from 'frappe-ui'
import GlassCard from '@/components/UI/GlassCard.vue'
import GlassInput from '@/components/UI/GlassInput.vue'
import GlassButton from '@/components/UI/GlassButton.vue'
import LoadingIndicator from '@/components/Icons/LoadingIndicator.vue'
import { FeatherIcon } from 'frappe-ui'

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

const messages = ref([])
const inputMessage = ref('')
const loading = ref(false)

const sendMessageToAI = createResource({
  url: 'crm.api.ai.chat_with_ai',
  method: 'POST',
  onSuccess: (response) => {
    messages.value.push({
      id: Date.now() + 1,
      role: 'assistant',
      content: response.message || 'I received your message.',
      timestamp: new Date()
    })
    loading.value = false
  },
  onError: () => {
    loading.value = false
  }
})

const sendMessage = () => {
  if (!inputMessage.value.trim()) return

  messages.value.push({
    id: Date.now(),
    role: 'user',
    content: inputMessage.value,
    timestamp: new Date()
  })

  const userMessage = inputMessage.value
  inputMessage.value = ''
  loading.value = true

  sendMessageToAI.submit({
    reference_type: props.referenceType,
    reference_name: props.referenceName,
    message: userMessage
  })
}

const formatTime = (date) => {
  return new Date(date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}
</script>
