<template>
  <button
    :class="[
      'glass-button',
      variantClass,
      sizeClass,
      fullWidth && 'w-full',
      disabled && 'opacity-50 cursor-not-allowed',
      className
    ]"
    :disabled="disabled || loading"
    @click="handleClick"
  >
    <span v-if="loading" class="mr-2">
      <FeatherIcon name="loader" class="h-4 w-4 animate-spin" />
    </span>
    <span v-if="icon && !loading" class="mr-2">
      <FeatherIcon :name="icon" class="h-4 w-4" />
    </span>
    <slot>{{ label }}</slot>
  </button>
</template>

<script setup>
import { computed } from 'vue'
import { FeatherIcon } from 'frappe-ui'

const props = defineProps({
  label: {
    type: String,
    default: ''
  },
  variant: {
    type: String,
    default: 'default', // 'default', 'primary', 'success', 'warning', 'danger', 'subtle'
    validator: (value) =>
      ['default', 'primary', 'success', 'warning', 'danger', 'subtle'].includes(
        value
      )
  },
  size: {
    type: String,
    default: 'md', // 'sm', 'md', 'lg'
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  },
  icon: {
    type: String,
    default: ''
  },
  loading: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  },
  fullWidth: {
    type: Boolean,
    default: false
  },
  className: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['click'])

const variantClass = computed(() => {
  const variants = {
    default: '',
    primary: 'glass-gradient-primary text-white',
    success: 'glass-gradient-success text-white',
    warning: 'glass-gradient-warning text-white',
    danger: 'glass-gradient-danger text-white',
    subtle: 'glass-subtle'
  }
  return variants[props.variant]
})

const sizeClass = computed(() => {
  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg'
  }
  return sizes[props.size]
})

const handleClick = (event) => {
  if (!props.disabled && !props.loading) {
    emit('click', event)
  }
}
</script>

<style scoped>
.glass-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 500;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.glass-button:not(:disabled):hover {
  transform: translateY(-2px);
  box-shadow: var(--glass-shadow-lg);
}

.glass-button:not(:disabled):active {
  transform: translateY(0);
}
</style>
