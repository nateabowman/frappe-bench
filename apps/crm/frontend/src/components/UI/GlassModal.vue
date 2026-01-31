<template>
  <Teleport to="body">
    <Transition name="modal">
      <div
        v-if="modelValue"
        class="fixed inset-0 z-[1050] flex items-center justify-center p-4"
        @click.self="handleBackdropClick"
      >
        <div class="glass-overlay-dark fixed inset-0" />
        <div
          :class="[
            'glass-modal relative z-10 max-h-[90vh] w-full max-w-lg overflow-y-auto glass-scrollbar',
            sizeClass,
            className
          ]"
        >
          <div v-if="showHeader" class="mb-4 flex items-center justify-between">
            <h3 v-if="title" class="text-xl font-semibold glass-text">
              {{ title }}
            </h3>
            <slot name="header" />
            <button
              v-if="showClose"
              class="glass-button ml-auto rounded-full p-2"
              @click="handleClose"
            >
              <FeatherIcon name="x" class="h-5 w-5" />
            </button>
          </div>
          <div class="glass-content">
            <slot />
          </div>
          <div v-if="showFooter" class="mt-4 flex items-center justify-end gap-2">
            <slot name="footer" />
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { computed } from 'vue'
import { FeatherIcon } from 'frappe-ui'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: ''
  },
  size: {
    type: String,
    default: 'md', // 'sm', 'md', 'lg', 'xl', 'full'
    validator: (value) => ['sm', 'md', 'lg', 'xl', 'full'].includes(value)
  },
  showClose: {
    type: Boolean,
    default: true
  },
  showHeader: {
    type: Boolean,
    default: true
  },
  showFooter: {
    type: Boolean,
    default: false
  },
  closeOnBackdrop: {
    type: Boolean,
    default: true
  },
  className: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue', 'close'])

const sizeClass = computed(() => {
  const sizes = {
    sm: 'max-w-sm',
    md: 'max-w-lg',
    lg: 'max-w-2xl',
    xl: 'max-w-4xl',
    full: 'max-w-full'
  }
  return sizes[props.size]
})

const handleClose = () => {
  emit('update:modelValue', false)
  emit('close')
}

const handleBackdropClick = () => {
  if (props.closeOnBackdrop) {
    handleClose()
  }
}
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.25s ease;
}

.modal-enter-active .glass-modal,
.modal-leave-active .glass-modal {
  transition: transform 0.25s ease, opacity 0.25s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .glass-modal,
.modal-leave-to .glass-modal {
  transform: scale(0.95);
  opacity: 0;
}

.glass-content {
  @apply text-ink-gray-9;
}
</style>
