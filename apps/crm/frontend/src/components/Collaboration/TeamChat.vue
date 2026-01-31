<template>
  <div class="flex flex-col h-full">
    <div class="flex-1 overflow-y-auto glass-scrollbar p-4 space-y-4">
      <div
        v-for="message in messages.data"
        :key="message.name"
        class="flex"
        :class="message.sent_by === currentUser ? 'justify-end' : 'justify-start'"
      >
        <div
          class="glass-card max-w-[80%] p-3"
          :class="message.sent_by === currentUser ? 'glass-gradient-primary' : ''"
        >
          <div class="flex items-center gap-2 mb-1">
            <UserAvatar :user="message.sent_by" size="sm" />
            <span class="text-xs text-ink-gray-5">{{ formatTime(message.sent_at) }}</span>
          </div>
          <div v-html="message.message" class="text-sm"></div>
          <div v-if="message.mentioned_users && message.mentioned_users.length > 0" class="mt-2">
            <div class="text-xs text-ink-gray-5">
              {{ __('Mentioned') }}:
              <span
                v-for="(user, index) in message.mentioned_users"
                :key="user.user"
                class="font-medium"
              >
                {{ user.user }}{{ index < message.mentioned_users.length - 1 ? ', ' : '' }}
              </span>
            </div>
          </div>
        </div>
      </div>
      <div v-if="messages.loading" class="flex justify-center">
        <LoadingIndicator />
      </div>
    </div>
    <div class="border-t border-glass-border p-4">
      <MentionsInput
        v-model="newMessage"
        :reference-type="referenceType"
        :reference-name="referenceName"
        @send="sendMessage"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { createResource } from 'frappe-ui'
import { sessionStore } from '@/stores/session'
import GlassCard from '@/components/UI/GlassCard.vue'
import UserAvatar from '@/components/UserAvatar.vue'
import MentionsInput from '@/components/Collaboration/MentionsInput.vue'
import LoadingIndicator from '@/components/Icons/LoadingIndicator.vue'

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

const { user: currentUser } = sessionStore()
const newMessage = ref('')

const messages = createResource({
  url: 'crm.api.collaboration.get_team_chat_messages',
  params: {
    reference_type: props.referenceType,
    reference_name: props.referenceName,
    limit: 50
  },
  auto: true,
  transform: (data) => data || []
})

const sendChatMessage = createResource({
  url: 'crm.api.collaboration.send_team_chat_message',
  method: 'POST',
  onSuccess: () => {
    newMessage.value = ''
    messages.reload()
  }
})

const sendMessage = (message, mentionedUsers) => {
  sendChatMessage.submit({
    reference_type: props.referenceType,
    reference_name: props.referenceName,
    message: message,
    mentioned_users: mentionedUsers || []
  })
}

const formatTime = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

// Reload messages when reference changes
watch(() => [props.referenceType, props.referenceName], () => {
  messages.reload()
})
</script>
