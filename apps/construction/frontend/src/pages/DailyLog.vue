<template>
  <div class="p-4 space-y-4">
    <!-- New Log Button -->
    <router-link to="/daily-log/new" class="field-btn-primary w-full flex items-center justify-center gap-2">
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
      </svg>
      Create Today's Log
    </router-link>

    <!-- Job Site Filter -->
    <select v-model="selectedJobSite" class="field-input">
      <option value="">All Job Sites</option>
      <option v-for="site in jobSites" :key="site.name" :value="site.name">
        {{ site.job_name }}
      </option>
    </select>

    <!-- Logs List -->
    <div class="space-y-3">
      <div v-for="log in filteredLogs" :key="log.name" class="field-card">
        <router-link :to="`/daily-log/${log.name}`" class="block p-4">
          <div class="flex justify-between items-start mb-2">
            <div>
              <h3 class="font-medium text-slate-900">{{ log.job_site_name }}</h3>
              <p class="text-sm text-slate-500">{{ formatDate(log.report_date) }}</p>
            </div>
            <span :class="statusClass(log.status)">{{ log.status }}</span>
          </div>
          <div class="flex gap-4 text-sm text-slate-600 mt-3">
            <span>👷 {{ log.total_man_hours || 0 }} hrs</span>
            <span>{{ weatherIcon(log.weather_condition) }} {{ log.temperature }}°F</span>
          </div>
        </router-link>
      </div>

      <div v-if="filteredLogs.length === 0" class="text-center py-8 text-slate-500">
        No daily logs found
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const logs = ref([])
const jobSites = ref([])
const selectedJobSite = ref('')

const filteredLogs = computed(() => {
  if (!selectedJobSite.value) return logs.value
  return logs.value.filter(log => log.job_site === selectedJobSite.value)
})

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' })
}

const statusClass = (status) => {
  const classes = {
    'Draft': 'status-open',
    'Submitted': 'status-in-progress',
    'Approved': 'status-completed',
  }
  return classes[status] || 'status-open'
}

const weatherIcon = (condition) => {
  const icons = {
    'Clear': '☀️',
    'Partly Cloudy': '⛅',
    'Cloudy': '☁️',
    'Rain': '🌧️',
    'Snow': '❄️',
  }
  return icons[condition] || '🌤️'
}

onMounted(async () => {
  try {
    const [logsRes, sitesRes] = await Promise.all([
      fetch('/api/method/construction.api.field.get_daily_logs'),
      fetch('/api/method/construction.api.field.get_user_job_sites')
    ])
    const logsData = await logsRes.json()
    const sitesData = await sitesRes.json()
    logs.value = logsData.message || []
    jobSites.value = sitesData.message || []
  } catch (e) {
    console.log('Using offline data')
  }
})
</script>
