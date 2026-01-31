<template>
  <div class="relative">
    <textarea
      v-model="message"
      :placeholder="__('Type a message... Use @ to mention someone')"
      class="glass-input w-full min-h-[80px] resize-none"
      @input="handleInput"
      @keydown.enter.exact.prevent="handleEnter"
    />
    <div v-if="showMentions" class="absolute bottom-full mb-2 w-full glass-card max-h-48 overflow-y-auto">
      <div
        v-for="user in filteredUsers"
        :key="user.name"
        class="p-2 hover:glass-subtle cursor-pointer flex items-center gap-2"
        @click="selectUser(user)"
      >
        <UserAvatar :user="user.name" size="sm" />
        <span>{{ user.full_name || user.name }}</span>
      </div>
    </div>
    <div class="flex justify-end gap-2 mt-2">
      <Button
        variant="ghost"
        size="sm"
        :label="__('Cancel')"
        @click="$emit('cancel')"
      />
      <Button
        size="sm"
        :label="__('Send')"
        :disabled="!message.trim()"
        @click="handleSend"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { createResource } from 'frappe-ui'
import UserAvatar from '@/components/UserAvatar.vue'
import { Button } from 'frappe-ui'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  referenceType: {
    type: String,
    required: true
  },
  referenceName: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['update:modelValue', 'send', 'cancel'])

const message = ref(props.modelValue)
const showMentions = ref(false)
const mentionStart = ref(-1)
const mentionedUsers = ref([])

const users = createResource({
  url: 'crm.api.user.get_users',
  auto: true,
  transform: (data) => data || []
})

const filteredUsers = computed(() => {
  if (!showMentions.value || mentionStart.value === -1) return []
  const query = message.value.substring(mentionStart.value + 1).toLowerCase()
  return users.data.filter(user => {
    const name = (user.full_name || user.name).toLowerCase()
    return name.includes(query)
  }).slice(0, 5)
})

watch(() => props.modelValue, (newValue) => {
  message.value = newValue
})

const handleInput = (event) => {
  emit('update:modelValue', message.value)
  
  const text = message.value
  const cursorPos = event.target.selectionStart
  const textBeforeCursor = text.substring(0, cursorPos)
  const lastAtIndex = textBeforeCursor.lastIndexOf('@')
  
  if (lastAtIndex !== -1) {
    const textAfterAt = textBeforeCursor.substring(lastAtIndex + 1)
    if (!textAfterAt.includes(' ') && !textAfterAt.includes('\n')) {
      showMentions.value = true
      mentionStart.value = lastAtIndex
      return
    }
  }
  
  showMentions.value = false
  mentionStart.value = -1
}

const selectUser = (user) => {
  const beforeMention = message.value.substring(0, mentionStart.value)
  const afterMention = message.value.substring(mentionStart.value).replace(/@\w*/, `@${user.name} `)
  message.value = beforeMention + afterMention
  emit('update:modelValue', message.value)
  showMentions.value = false
  mentionedUsers.value.push(user.name)
}

const handleEnter = () => {
  if (showMentions.value && filteredUsers.value.length > 0) {
    selectUser(filteredUsers.value[0])
  } else {
    handleSend()
  }
}

const handleSend = () => {
  if (message.value.trim()) {
    emit('send', message.value, mentionedUsers.value)
    message.value = ''
    mentionedUsers.value = []
    emit('update:modelValue', '')
  }
}
</script>
