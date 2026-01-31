<template>
  <div class="min-h-screen bg-slate-50">
    <!-- Header -->
    <header class="bg-blue-800 text-white sticky top-0 z-50 shadow-lg">
      <div class="flex items-center justify-between px-4 py-3">
        <div class="flex items-center gap-3">
          <button @click="toggleMenu" class="p-2 hover:bg-blue-700 rounded-lg">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
            </svg>
          </button>
          <h1 class="text-lg font-semibold">{{ pageTitle }}</h1>
        </div>
        <div class="flex items-center gap-2">
          <button @click="syncData" class="p-2 hover:bg-blue-700 rounded-lg" :class="{ 'animate-spin': syncing }">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
          </button>
        </div>
      </div>
    </header>

    <!-- Side Menu -->
    <div v-if="menuOpen" class="fixed inset-0 z-40" @click="toggleMenu">
      <div class="absolute inset-0 bg-black/50"></div>
      <nav class="absolute left-0 top-0 bottom-0 w-72 bg-white shadow-xl" @click.stop>
        <div class="p-4 bg-blue-800 text-white">
          <h2 class="text-xl font-bold">Construction</h2>
          <p class="text-blue-200 text-sm">Field Operations</p>
        </div>
        <ul class="py-2">
          <li v-for="item in menuItems" :key="item.path">
            <router-link 
              :to="item.path" 
              class="flex items-center gap-3 px-4 py-3 hover:bg-slate-100 text-slate-700"
              @click="toggleMenu"
            >
              <span v-html="item.icon" class="w-5 h-5"></span>
              <span>{{ item.label }}</span>
            </router-link>
          </li>
        </ul>
      </nav>
    </div>

    <!-- Main Content -->
    <main class="pb-20">
      <router-view />
    </main>

    <!-- Bottom Navigation -->
    <nav class="fixed bottom-0 left-0 right-0 bg-white border-t border-slate-200 z-30">
      <div class="flex justify-around py-2">
        <router-link 
          v-for="item in bottomNav" 
          :key="item.path"
          :to="item.path"
          class="flex flex-col items-center py-1 px-3 text-slate-500"
          active-class="text-blue-600"
        >
          <span v-html="item.icon" class="w-6 h-6"></span>
          <span class="text-xs mt-1">{{ item.label }}</span>
        </router-link>
      </div>
    </nav>

    <!-- Offline Indicator -->
    <div v-if="!online" class="fixed top-16 left-0 right-0 bg-amber-500 text-white text-center py-1 text-sm z-30">
      Offline Mode - Changes will sync when connected
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const menuOpen = ref(false)
const syncing = ref(false)
const online = ref(navigator.onLine)

const pageTitle = computed(() => {
  const titles = {
    'Home': 'Dashboard',
    'DailyLog': 'Daily Logs',
    'PunchList': 'Punch Lists',
    'Inspection': 'Inspections',
    'JobSites': 'Job Sites',
  }
  return titles[route.name] || 'Construction'
})

const menuItems = [
  { path: '/', label: 'Dashboard', icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>' },
  { path: '/job-sites', label: 'Job Sites', icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>' },
  { path: '/daily-log', label: 'Daily Logs', icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>' },
  { path: '/punch-list', label: 'Punch Lists', icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/></svg>' },
  { path: '/inspection', label: 'Inspections', icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>' },
]

const bottomNav = [
  { path: '/', label: 'Home', icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>' },
  { path: '/daily-log', label: 'Log', icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>' },
  { path: '/punch-list', label: 'Punch', icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/></svg>' },
  { path: '/inspection', label: 'Inspect', icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>' },
]

const toggleMenu = () => {
  menuOpen.value = !menuOpen.value
}

const syncData = async () => {
  syncing.value = true
  // Sync offline data
  setTimeout(() => {
    syncing.value = false
  }, 1000)
}

const updateOnlineStatus = () => {
  online.value = navigator.onLine
}

onMounted(() => {
  window.addEventListener('online', updateOnlineStatus)
  window.addEventListener('offline', updateOnlineStatus)
})

onUnmounted(() => {
  window.removeEventListener('online', updateOnlineStatus)
  window.removeEventListener('offline', updateOnlineStatus)
})
</script>
