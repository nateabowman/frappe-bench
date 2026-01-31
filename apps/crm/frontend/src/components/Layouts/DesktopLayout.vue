<template>
  <div class="flex h-screen w-screen overflow-hidden">
    <div class="h-full glass-strong border-r border-glass-border">
      <AppSidebar />
    </div>
    <div class="flex-1 flex flex-col h-full overflow-auto bg-gradient-to-br from-surface-white via-surface-gray-1 to-surface-gray-2">
      <AppHeader />
      <div class="flex-1 overflow-auto glass-scrollbar">
        <slot />
      </div>
    </div>
    <GlobalModals />
  </div>
</template>
<script setup>
import AppSidebar from '@/components/Layouts/AppSidebar.vue'
import AppHeader from '@/components/Layouts/AppHeader.vue'
import GlobalModals from '@/components/Modals/GlobalModals.vue'
</script>
