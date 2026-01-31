<template>
  <div class="flex flex-col h-full overflow-hidden">
    <LayoutHeader>
      <template #left-header>
        <ViewBreadcrumbs routeName="Analytics" />
      </template>
      <template #right-header>
        <Button
          :label="__('Add Widget')"
          @click="showAddWidgetModal = true"
        >
          <template #prefix>
            <FeatherIcon name="plus" class="size-4" />
          </template>
        </Button>
        <Button
          :label="editing ? __('Done') : __('Edit')"
          @click="editing = !editing"
        >
          <template #prefix>
            <FeatherIcon :name="editing ? 'check' : 'edit'" class="size-4" />
          </template>
        </Button>
      </template>
    </LayoutHeader>

    <div class="flex-1 overflow-auto p-6 glass-scrollbar">
      <div v-if="widgets.loading" class="flex items-center justify-center h-64">
        <LoadingIndicator />
      </div>
      <div v-else-if="widgets.data && widgets.data.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        <GlassCard
          v-for="widget in widgets.data"
          :key="widget.name"
          :hoverable="editing"
          class="glass-card"
        >
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold glass-text">{{ widget.widget_title }}</h3>
            <div v-if="editing" class="flex gap-2">
              <Button
                variant="ghost"
                size="sm"
                @click="editWidget(widget)"
              >
                <FeatherIcon name="edit" class="size-4" />
              </Button>
              <Button
                variant="ghost"
                size="sm"
                @click="deleteWidget(widget.name)"
              >
                <FeatherIcon name="trash-2" class="size-4" />
              </Button>
            </div>
          </div>
          <div class="widget-content">
            <component
              :is="getWidgetComponent(widget.widget_type)"
              :widget="widget"
            />
          </div>
        </GlassCard>
      </div>
      <div v-else class="flex flex-col items-center justify-center h-64 glass-card">
        <FeatherIcon name="bar-chart-2" class="size-12 text-ink-gray-5 mb-4" />
        <p class="text-ink-gray-5 mb-4">{{ __('No widgets yet') }}</p>
        <Button
          :label="__('Add Your First Widget')"
          @click="showAddWidgetModal = true"
        />
      </div>
    </div>

    <GlassModal
      v-model="showAddWidgetModal"
      :title="editingWidget ? __('Edit Widget') : __('Add Widget')"
      size="lg"
    >
      <WidgetBuilder
        :widget="editingWidget"
        @save="handleWidgetSave"
        @cancel="showAddWidgetModal = false"
      />
    </GlassModal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { createResource } from 'frappe-ui'
import LayoutHeader from '@/components/LayoutHeader.vue'
import ViewBreadcrumbs from '@/components/ViewBreadcrumbs.vue'
import GlassCard from '@/components/UI/GlassCard.vue'
import GlassModal from '@/components/UI/GlassModal.vue'
import WidgetBuilder from '@/components/Analytics/WidgetBuilder.vue'
import LoadingIndicator from '@/components/Icons/LoadingIndicator.vue'
import { Button, FeatherIcon } from 'frappe-ui'

const editing = ref(false)
const showAddWidgetModal = ref(false)
const editingWidget = ref(null)

const widgets = createResource({
  url: 'crm.api.analytics.get_analytics_widgets',
  auto: true,
  transform: (data) => data || []
})

const getWidgetComponent = (widgetType) => {
  const components = {
    'Chart': () => import('@/components/Analytics/ChartWidget.vue'),
    'Metric': () => import('@/components/Analytics/MetricWidget.vue'),
    'Table': () => import('@/components/Analytics/TableWidget.vue'),
    'KPI': () => import('@/components/Analytics/KPIWidget.vue'),
  }
  return components[widgetType] || components['Metric']
}

const editWidget = (widget) => {
  editingWidget.value = widget
  showAddWidgetModal.value = true
}

const deleteWidget = async (widgetName) => {
  // Implement delete logic
  widgets.reload()
}

const handleWidgetSave = () => {
  showAddWidgetModal.value = false
  editingWidget.value = null
  widgets.reload()
}
</script>

<style scoped>
.widget-content {
  min-height: 200px;
}
</style>
