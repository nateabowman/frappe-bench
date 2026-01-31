<template>
  <div class="flex h-screen w-screen overflow-hidden">
    <MobileSidebar />
    <div class="flex h-full flex-1 flex-col overflow-auto bg-gradient-to-br from-surface-white via-surface-gray-1 to-surface-gray-2">
      <MobileAppHeader />
      <div class="flex-1 overflow-auto glass-scrollbar">
        <slot />
      </div>
    </div>
    <GlobalModals />
  </div>
</template>
<script setup>
import MobileSidebar from '@/components/Mobile/MobileSidebar.vue'
import MobileAppHeader from '@/components/Mobile/MobileAppHeader.vue'
import GlobalModals from '@/components/Modals/GlobalModals.vue'
</script>
