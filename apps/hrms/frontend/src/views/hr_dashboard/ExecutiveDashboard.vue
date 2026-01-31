<template>
	<BaseLayout pageTitle="Executive Dashboard">
		<template #body>
			<div class="flex flex-col mt-7 mb-7 p-4 gap-6">
				<!-- Header -->
				<div class="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-lg p-6 text-white">
					<h2 class="text-2xl font-bold mb-2">{{ __("Executive Dashboard") }}</h2>
					<p class="text-indigo-100">{{ __("Real-time workforce insights and analytics") }}</p>
				</div>

				<!-- Key Metrics -->
				<div class="grid grid-cols-2 md:grid-cols-4 gap-4">
					<div class="metric-card bg-gradient-to-br from-blue-50 to-blue-100">
						<div class="metric-card-value">{{ workforceData?.total_employees || 0 }}</div>
						<div class="metric-card-label">{{ __("Total Employees") }}</div>
					</div>

					<div class="metric-card bg-gradient-to-br from-green-50 to-green-100">
						<div class="metric-card-value">{{ costData?.total_net || 0 | currency }}</div>
						<div class="metric-card-label">{{ __("Total Payroll Cost") }}</div>
					</div>

					<div class="metric-card bg-gradient-to-br from-purple-50 to-purple-100">
						<div class="metric-card-value">{{ engagementScore || 0 }}%</div>
						<div class="metric-card-label">{{ __("Engagement Score") }}</div>
					</div>

					<div class="metric-card bg-gradient-to-br from-orange-50 to-orange-100">
						<div class="metric-card-value">{{ avgPerformance || 0 }}</div>
						<div class="metric-card-label">{{ __("Avg Performance") }}</div>
					</div>
				</div>

				<!-- Workforce Demographics -->
				<div class="dashboard-card">
					<div class="dashboard-card-header">
						<h3 class="dashboard-card-title">{{ __("Workforce Demographics") }}</h3>
					</div>
					<WorkforceDemographics />
				</div>

				<!-- Cost Analysis -->
				<div class="dashboard-card">
					<div class="dashboard-card-header">
						<h3 class="dashboard-card-title">{{ __("Cost Analysis by Department") }}</h3>
					</div>
					<CostAnalysisChart period="year" />
				</div>

				<!-- Payroll Trends -->
				<div class="dashboard-card">
					<div class="dashboard-card-header">
						<h3 class="dashboard-card-title">{{ __("Payroll Trends") }}</h3>
					</div>
					<PayrollTrendChart period="year" />
				</div>

				<!-- Engagement Gauge -->
				<div class="dashboard-card">
					<div class="dashboard-card-header">
						<h3 class="dashboard-card-title">{{ __("Employee Engagement") }}</h3>
					</div>
					<EmployeeEngagementGauge />
				</div>
			</div>
		</template>
	</BaseLayout>
</template>

<script setup>
import { inject, computed } from "vue"
import BaseLayout from "@/components/BaseLayout.vue"
import WorkforceDemographics from "@/components/charts/WorkforceDemographics.vue"
import CostAnalysisChart from "@/components/charts/CostAnalysisChart.vue"
import PayrollTrendChart from "@/components/charts/PayrollTrendChart.vue"
import EmployeeEngagementGauge from "@/components/charts/EmployeeEngagementGauge.vue"
import { hrWorkforceDemographicsData, hrCostAnalysisData, hrPayrollTrendsData, engagementMetricsData } from "@/data/analytics"

const __ = inject("$translate")

const workforceData = computed(() => hrWorkforceDemographicsData.data)
const costData = computed(() => hrCostAnalysisData.data)
const engagementScore = computed(() => engagementMetricsData.data?.overall_score || 0)
const avgPerformance = computed(() => {
	// This would come from performance data
	return 0
})
</script>

<script>
export default {
	name: "ExecutiveDashboard",
}
</script>
