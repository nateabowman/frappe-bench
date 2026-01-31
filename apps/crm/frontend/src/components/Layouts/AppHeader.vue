<template>
  <div class="flex items-center border-b border-glass-border glass-subtle backdrop-blur-glass px-5 py-3 gap-4 sticky top-0 z-40">
    <div id="app-header" class="flex-1"></div>
    <div class="flex items-center gap-3">
      <GlobalSearch />
      <CallUI />
    </div>
  </div>
</template>

<script setup>
import CallUI from '@/components/Telephony/CallUI.vue'
import GlobalSearch from '@/components/DesignSystem/GlobalSearch.vue'
</script>
