<template>
  <div
    :class="[
      'glass-card',
      variantClass,
      hoverable && 'cursor-pointer',
      interactive && 'glass-border-animate',
      className
    ]"
    @click="handleClick"
  >
    <slot />
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'default', // 'default', 'subtle', 'strong'
    validator: (value) => ['default', 'subtle', 'strong'].includes(value)
  },
  hoverable: {
    type: Boolean,
    default: false
  },
  interactive: {
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
    subtle: 'glass-subtle',
    strong: 'glass-strong'
  }
  return variants[props.variant]
})

const handleClick = (event) => {
  if (props.hoverable || props.interactive) {
    emit('click', event)
  }
}
</script>

<style scoped>
.glass-card {
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.glass-card.hoverable:hover {
  transform: translateY(-4px);
}
</style>
