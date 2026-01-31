<template>
  <div class="p-4 space-y-4">
    <!-- Quick Stats -->
    <div class="grid grid-cols-2 gap-3">
      <div class="field-card p-4">
        <p class="text-sm text-slate-500">Active Jobs</p>
        <p class="text-2xl font-bold text-slate-900">{{ stats.activeJobs }}</p>
      </div>
      <div class="field-card p-4">
        <p class="text-sm text-slate-500">Today's Logs</p>
        <p class="text-2xl font-bold text-slate-900">{{ stats.todayLogs }}</p>
      </div>
      <div class="field-card p-4">
        <p class="text-sm text-slate-500">Open Punch Items</p>
        <p class="text-2xl font-bold text-amber-600">{{ stats.openPunchItems }}</p>
      </div>
      <div class="field-card p-4">
        <p class="text-sm text-slate-500">Pending RFIs</p>
        <p class="text-2xl font-bold text-blue-600">{{ stats.pendingRfis }}</p>
      </div>
    </div>

    <!-- Charts Section -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <DailyLogsTrend :data="chartData.dailyLogsTrend || []" />
      <PunchItemsStatus :data="chartData.punchByStatus || []" />
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <ActivityByType :data="chartData.activityByType || []" />
      <ProjectProgress :data="chartData.projectProgress || []" />
    </div>

    <!-- Quick Actions -->
    <div class="field-card">
      <div class="p-4 border-b border-slate-100">
        <h2 class="font-semibold text-slate-900">Quick Actions</h2>
      </div>
      <div class="p-3 space-y-2">
        <router-link to="/daily-log/new" class="flex items-center gap-3 p-3 rounded-lg hover:bg-slate-50">
          <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
            <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
          </div>
          <div>
            <p class="font-medium text-slate-900">New Daily Log</p>
            <p class="text-sm text-slate-500">Create today's field report</p>
          </div>
        </router-link>
        <router-link to="/punch-list/new" class="flex items-center gap-3 p-3 rounded-lg hover:bg-slate-50">
          <div class="w-10 h-10 bg-amber-100 rounded-lg flex items-center justify-center">
            <svg class="w-5 h-5 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/>
            </svg>
          </div>
          <div>
            <p class="font-medium text-slate-900">New Punch Item</p>
            <p class="text-sm text-slate-500">Add punch list item</p>
          </div>
        </router-link>
        <router-link to="/inspection/new" class="flex items-center gap-3 p-3 rounded-lg hover:bg-slate-50">
          <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
            <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <div>
            <p class="font-medium text-slate-900">New Inspection</p>
            <p class="text-sm text-slate-500">Start site inspection</p>
          </div>
        </router-link>
      </div>
    </div>

    <!-- Recent Activity -->
    <div class="field-card">
      <div class="p-4 border-b border-slate-100">
        <h2 class="font-semibold text-slate-900">Recent Activity</h2>
      </div>
      <div class="divide-y divide-slate-100">
        <div v-for="activity in recentActivity" :key="activity.id" class="p-4">
          <div class="flex items-start gap-3">
            <div class="w-8 h-8 bg-slate-100 rounded-full flex items-center justify-center flex-shrink-0">
              <span class="text-xs">{{ activity.initials }}</span>
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm text-slate-900">{{ activity.description }}</p>
              <p class="text-xs text-slate-500 mt-1">{{ activity.time }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import DailyLogsTrend from '@/components/charts/DailyLogsTrend.vue'
import PunchItemsStatus from '@/components/charts/PunchItemsStatus.vue'
import ActivityByType from '@/components/charts/ActivityByType.vue'
import ProjectProgress from '@/components/charts/ProjectProgress.vue'

const stats = ref({
  activeJobs: 0,
  todayLogs: 0,
  openPunchItems: 0,
  pendingRfis: 0,
})

const chartData = ref({
  dailyLogsTrend: [],
  punchByStatus: [],
  activityByType: [],
  projectProgress: [],
})

const recentActivity = ref([
  { id: 1, initials: 'JD', description: 'Daily log submitted for Main Street Project', time: '2 hours ago' },
  { id: 2, initials: 'SM', description: 'Punch item completed: Drywall repair in Room 201', time: '3 hours ago' },
  { id: 3, initials: 'RB', description: 'Inspection passed for electrical rough-in', time: '5 hours ago' },
])

onMounted(async () => {
  // Fetch stats from API
  try {
    const response = await fetch('/api/method/construction.api.dashboard.get_field_stats')
    const data = await response.json()
    if (data.message) {
      stats.value = data.message
    }
  } catch (e) {
    console.log('Using offline data')
  }
  
  // Fetch chart data
  try {
    const chartResponse = await fetch('/api/method/construction.api.dashboard.get_field_chart_data')
    const chartResult = await chartResponse.json()
    if (chartResult.message) {
      chartData.value = chartResult.message
    }
  } catch (e) {
    console.log('Error loading chart data:', e)
  }
})
</script>
