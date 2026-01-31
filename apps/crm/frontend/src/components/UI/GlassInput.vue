<template>
  <div :class="['glass-input-wrapper', fullWidth && 'w-full', className]">
    <label
      v-if="label"
      :for="inputId"
      class="mb-2 block text-sm font-medium glass-text"
    >
      {{ label }}
      <span v-if="required" class="text-danger-500">*</span>
    </label>
    <div class="relative">
      <div v-if="prefixIcon" class="absolute left-3 top-1/2 -translate-y-1/2">
        <FeatherIcon :name="prefixIcon" class="h-5 w-5 text-ink-gray-5" />
      </div>
      <input
        :id="inputId"
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :required="required"
        :class="[
          'glass-input glass-focus w-full',
          prefixIcon && 'pl-10',
          suffixIcon && 'pr-10',
          error && 'border-danger-500',
          sizeClass
        ]"
        @input="handleInput"
        @blur="handleBlur"
        @focus="handleFocus"
      />
      <div v-if="suffixIcon" class="absolute right-3 top-1/2 -translate-y-1/2">
        <FeatherIcon :name="suffixIcon" class="h-5 w-5 text-ink-gray-5" />
      </div>
    </div>
    <p v-if="error" class="mt-1 text-sm text-danger-500">{{ error }}</p>
    <p v-if="hint && !error" class="mt-1 text-sm text-ink-gray-5">{{ hint }}</p>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { FeatherIcon } from 'frappe-ui'

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: ''
  },
  type: {
    type: String,
    default: 'text'
  },
  label: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: ''
  },
  hint: {
    type: String,
    default: ''
  },
  error: {
    type: String,
    default: ''
  },
  required: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  },
  prefixIcon: {
    type: String,
    default: ''
  },
  suffixIcon: {
    type: String,
    default: ''
  },
  size: {
    type: String,
    default: 'md', // 'sm', 'md', 'lg'
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  },
  fullWidth: {
    type: Boolean,
    default: true
  },
  className: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue', 'blur', 'focus'])

const inputId = computed(() => `glass-input-${Math.random().toString(36).substr(2, 9)}`)

const sizeClass = computed(() => {
  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-5 py-3 text-lg'
  }
  return sizes[props.size]
})

const handleInput = (event) => {
  emit('update:modelValue', event.target.value)
}

const handleBlur = (event) => {
  emit('blur', event)
}

const handleFocus = (event) => {
  emit('focus', event)
}
</script>

<style scoped>
.glass-input-wrapper {
  @apply flex flex-col;
}
</style>
