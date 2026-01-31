<template>
  <div class="h-full w-full">
    <div
      v-if="item.type == 'number_chart'"
      class="flex h-full w-full glass-card overflow-hidden cursor-pointer"
    >
      <Tooltip :text="__(item.data?.tooltip)">
        <NumberChart v-if="item.data" :key="index" :config="item.data" />
      </Tooltip>
    </div>
    <div
      v-else-if="item.type == 'spacer'"
      class="glass-subtle rounded-lg h-full overflow-hidden text-ink-gray-5 flex items-center justify-center border-2 border-dashed border-glass-border"
      :class="editing ? 'border-glass-border-hover' : ''"
    >
      {{ editing ? __('Spacer') : '' }}
    </div>
    <div
      v-else-if="item.type == 'axis_chart'"
      class="h-full w-full glass-card"
    >
      <AxisChart v-if="item.data" :config="item.data" />
    </div>
    <div
      v-else-if="item.type == 'donut_chart'"
      class="h-full w-full glass-card overflow-hidden"
    >
      <DonutChart v-if="item.data" :config="item.data" />
    </div>
    <div
      v-else-if="item.type == 'funnel_chart'"
      class="h-full w-full glass-card overflow-hidden"
    >
      <FunnelChart v-if="item.data" :config="item.data" />
    </div>
    <div
      v-else-if="item.type == 'heatmap_chart'"
      class="h-full w-full glass-card overflow-hidden"
    >
      <HeatMapChart v-if="item.data" :config="item.data" />
    </div>
    <div
      v-else-if="item.type == 'trend_analysis'"
      class="h-full w-full glass-card overflow-hidden"
    >
      <TrendAnalysis v-if="item.data" :config="item.data" />
    </div>
    <div
      v-else-if="item.type == 'goal_tracker'"
      class="h-full w-full glass-card overflow-hidden"
    >
      <GoalTracker v-if="item.data" :config="item.data" />
    </div>
  </div>
</template>
<script setup>
import { AxisChart, DonutChart, NumberChart, Tooltip } from 'frappe-ui'
import FunnelChart from './Widgets/FunnelChart.vue'
import HeatMapChart from './Widgets/HeatMapChart.vue'
import TrendAnalysis from './Widgets/TrendAnalysis.vue'
import GoalTracker from './Widgets/GoalTracker.vue'

const props = defineProps({
  index: {
    type: Number,
    required: true,
  },
  item: {
    type: Object,
    required: true,
  },
  editing: {
    type: Boolean,
    default: false,
  },
})
</script>
