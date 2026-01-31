<template>
  <div class="p-4 space-y-4">
    <!-- Quick Add -->
    <router-link to="/punch-list/new" class="field-btn-primary w-full flex items-center justify-center gap-2">
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
      </svg>
      New Punch Item
    </router-link>

    <!-- Filters -->
    <div class="flex gap-2">
      <select v-model="selectedStatus" class="field-input flex-1">
        <option value="">All Status</option>
        <option value="Open">Open</option>
        <option value="In Progress">In Progress</option>
        <option value="Completed">Completed</option>
      </select>
      <select v-model="selectedPriority" class="field-input flex-1">
        <option value="">All Priority</option>
        <option value="Urgent">Urgent</option>
        <option value="High">High</option>
        <option value="Medium">Medium</option>
        <option value="Low">Low</option>
      </select>
    </div>

    <!-- Stats -->
    <div class="flex gap-2 text-sm">
      <span class="px-3 py-1 bg-red-100 text-red-700 rounded-full">{{ urgentCount }} Urgent</span>
      <span class="px-3 py-1 bg-amber-100 text-amber-700 rounded-full">{{ openCount }} Open</span>
      <span class="px-3 py-1 bg-green-100 text-green-700 rounded-full">{{ completedCount }} Done</span>
    </div>

    <!-- Punch Items -->
    <div class="space-y-3">
      <div v-for="item in filteredItems" :key="item.name" 
           class="field-card p-4"
           :class="{ 'border-l-4 border-l-red-500': item.priority === 'Urgent' }">
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <p class="font-medium text-slate-900">{{ item.description }}</p>
            <p class="text-sm text-slate-500 mt-1">{{ item.location }} · {{ item.trade }}</p>
          </div>
          <span :class="priorityClass(item.priority)" class="ml-2">{{ item.priority }}</span>
        </div>
        <div class="flex items-center justify-between mt-3">
          <span :class="statusClass(item.status)" class="text-xs">{{ item.status }}</span>
          <button 
            v-if="item.status !== 'Completed'"
            @click="markComplete(item)"
            class="text-green-600 text-sm font-medium"
          >
            Mark Complete
          </button>
        </div>
      </div>

      <div v-if="filteredItems.length === 0" class="text-center py-8 text-slate-500">
        No punch items found
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const items = ref([])
const selectedStatus = ref('')
const selectedPriority = ref('')

const filteredItems = computed(() => {
  return items.value.filter(item => {
    if (selectedStatus.value && item.status !== selectedStatus.value) return false
    if (selectedPriority.value && item.priority !== selectedPriority.value) return false
    return true
  })
})

const urgentCount = computed(() => items.value.filter(i => i.priority === 'Urgent' && i.status !== 'Completed').length)
const openCount = computed(() => items.value.filter(i => i.status === 'Open').length)
const completedCount = computed(() => items.value.filter(i => i.status === 'Completed').length)

const priorityClass = (priority) => {
  const classes = {
    'Urgent': 'status-urgent',
    'High': 'status-badge bg-orange-100 text-orange-800',
    'Medium': 'status-badge bg-blue-100 text-blue-800',
    'Low': 'status-badge bg-slate-100 text-slate-600',
  }
  return classes[priority]
}

const statusClass = (status) => {
  const classes = {
    'Open': 'status-open',
    'In Progress': 'status-in-progress',
    'Completed': 'status-completed',
  }
  return classes[status]
}

const markComplete = async (item) => {
  try {
    await fetch('/api/method/construction.api.field.complete_punch_item', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ item_name: item.name })
    })
    item.status = 'Completed'
  } catch (e) {
    console.error('Error completing item:', e)
  }
}

onMounted(async () => {
  try {
    const response = await fetch('/api/method/construction.api.field.get_punch_items')
    const data = await response.json()
    items.value = data.message || []
  } catch (e) {
    console.log('Using offline data')
  }
})
</script>
