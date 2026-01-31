<template>
  <div class="relative w-full max-w-2xl">
    <div class="relative">
      <FeatherIcon
        name="search"
        class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400"
      />
      <TextInput
        v-model="query"
        :placeholder="__('Search leads, deals, contacts...')"
        class="w-full pl-10 pr-4 py-2 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all"
        @focus="showResults = true"
        @blur="handleBlur"
        @keydown.escape="showResults = false"
        @keydown.down.prevent="navigateResults(1)"
        @keydown.up.prevent="navigateResults(-1)"
        @keydown.enter="selectResult"
      />
      <kbd
        v-if="!query && !showResults"
        class="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none hidden sm:flex items-center gap-1 px-2 py-1 text-xs font-semibold text-gray-500 bg-gray-100 border border-gray-200 rounded"
      >
        <span>⌘</span>
        <span>K</span>
      </kbd>
    </div>

    <!-- Search Results Dropdown -->
    <Transition name="fade-slide">
      <div
        v-if="showResults && (query || recentSearches.length)"
        class="absolute z-50 w-full mt-2 bg-white border border-gray-200 rounded-lg shadow-xl max-h-96 overflow-y-auto custom-scrollbar"
      >
        <!-- Recent Searches -->
        <div v-if="!query && recentSearches.length" class="p-2">
          <div class="px-3 py-2 text-xs font-semibold text-gray-500 uppercase">
            {{ __('Recent Searches') }}
          </div>
          <div
            v-for="(search, index) in recentSearches"
            :key="index"
            class="px-3 py-2 rounded hover:bg-gray-100 cursor-pointer flex items-center gap-2"
            :class="{ 'bg-gray-100': selectedIndex === index }"
            @click="performSearch(search)"
          >
            <FeatherIcon name="clock" class="h-4 w-4 text-gray-400" />
            <span class="text-sm">{{ search }}</span>
          </div>
        </div>

        <!-- Search Results -->
        <div v-if="query && searchResults.loading" class="p-4 text-center">
          <div class="inline-block animate-spin rounded-full h-6 w-6 border-2 border-primary-500 border-t-transparent"></div>
        </div>

        <div v-else-if="query && searchResults.data?.length" class="py-2">
          <div
            v-for="(result, index) in searchResults.data"
            :key="result.name"
            class="px-3 py-2 rounded hover:bg-gray-100 cursor-pointer flex items-center gap-3"
            :class="{ 'bg-gray-100': selectedIndex === index + recentSearches.length }"
            @click="selectResult(result)"
          >
            <FeatherIcon
              :name="getResultIcon(result.doctype)"
              class="h-5 w-5 text-gray-400"
            />
            <div class="flex-1 min-w-0">
              <div class="text-sm font-medium text-gray-900 truncate">
                {{ result.title || result.name }}
              </div>
              <div class="text-xs text-gray-500">
                {{ getResultTypeLabel(result.doctype) }}
              </div>
            </div>
            <FeatherIcon name="arrow-right" class="h-4 w-4 text-gray-400" />
          </div>
        </div>

        <div
          v-else-if="query && !searchResults.loading && !searchResults.data?.length"
          class="p-4 text-center text-sm text-gray-500"
        >
          {{ __('No results found') }}
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { FeatherIcon, TextInput, createResource } from 'frappe-ui'
import { useDebounceFn } from '@vueuse/core'

const router = useRouter()
const query = ref('')
const showResults = ref(false)
const selectedIndex = ref(-1)
const recentSearches = ref([])

const searchResults = createResource({
  url: 'crm.api.search.global_search',
  makeParams() {
    return { query: query.value }
  },
  auto: false,
})

const debouncedSearch = useDebounceFn(() => {
  if (query.value.trim()) {
    searchResults.reload()
  }
}, 300)

watch(query, () => {
  selectedIndex.value = -1
  if (query.value.trim()) {
    debouncedSearch()
  }
})

function getResultIcon(doctype) {
  const icons = {
    'CRM Lead': 'user',
    'CRM Deal': 'briefcase',
    'CRM Contact': 'user',
    'CRM Organization': 'building',
  }
  return icons[doctype] || 'file'
}

function getResultTypeLabel(doctype) {
  const labels = {
    'CRM Lead': __('Lead'),
    'CRM Deal': __('Deal'),
    'CRM Contact': __('Contact'),
    'CRM Organization': __('Organization'),
  }
  return labels[doctype] || doctype
}

function handleBlur() {
  // Delay to allow click events on results
  setTimeout(() => {
    showResults.value = false
  }, 200)
}

function navigateResults(direction) {
  const totalResults = (query.value ? searchResults.data?.length || 0 : 0) + recentSearches.value.length
  if (totalResults === 0) return

  selectedIndex.value += direction
  if (selectedIndex.value < 0) selectedIndex.value = totalResults - 1
  if (selectedIndex.value >= totalResults) selectedIndex.value = 0
}

function selectResult(result = null) {
  if (result) {
    navigateToResult(result)
  } else if (selectedIndex.value >= 0) {
    const recentCount = recentSearches.value.length
    if (selectedIndex.value < recentCount) {
      performSearch(recentSearches.value[selectedIndex.value])
    } else {
      const resultIndex = selectedIndex.value - recentCount
      if (searchResults.data?.[resultIndex]) {
        navigateToResult(searchResults.data[resultIndex])
      }
    }
  }
}

function navigateToResult(result) {
  const routes = {
    'CRM Lead': `/leads/${result.name}`,
    'CRM Deal': `/deals/${result.name}`,
    'CRM Contact': `/contacts/${result.name}`,
    'CRM Organization': `/organizations/${result.name}`,
  }
  const route = routes[result.doctype]
  if (route) {
    router.push(route)
    showResults.value = false
    query.value = ''
    addToRecentSearches(result.title || result.name)
  }
}

function performSearch(searchQuery) {
  query.value = searchQuery
  showResults.value = true
  if (searchQuery.trim()) {
    searchResults.reload()
  }
}

function addToRecentSearches(search) {
  if (!recentSearches.value.includes(search)) {
    recentSearches.value.unshift(search)
    recentSearches.value = recentSearches.value.slice(0, 5)
    localStorage.setItem('crm_recent_searches', JSON.stringify(recentSearches.value))
  }
}

function handleKeyDown(event) {
  if ((event.metaKey || event.ctrlKey) && event.key === 'k') {
    event.preventDefault()
    const input = event.target.closest('.relative')?.querySelector('input')
    if (input) input.focus()
  }
}

onMounted(() => {
  const saved = localStorage.getItem('crm_recent_searches')
  if (saved) {
    try {
      recentSearches.value = JSON.parse(saved)
    } catch (e) {
      // Ignore parse errors
    }
  }
  document.addEventListener('keydown', handleKeyDown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeyDown)
})
</script>

<style scoped>
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.2s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>

