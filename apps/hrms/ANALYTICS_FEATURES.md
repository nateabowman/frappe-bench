# HRMS Analytics and UI Redesign - Feature Documentation

## Overview
This document describes the new analytics features and UI redesign implemented for the Frappe HRMS app.

## New Features

### 1. Analytics & Reporting Module

#### Backend Components
- **Location**: `hrms/analytics/`
- **API Endpoints**: `hrms/analytics/api/charts.py`
- **Data Aggregation**: `hrms/analytics/utils/data_aggregator.py`
- **Permissions**: `hrms/analytics/utils/permissions.py`

#### Available Analytics
- Attendance Heatmap - Calendar-based attendance visualization
- Payroll Trends - Salary history and trends
- Leave Utilization - Leave pattern analysis
- Performance Metrics - Performance scorecards
- Workforce Demographics - Age, gender, department, tenure distributions
- Cost Analysis - Payroll cost breakdown by department
- Engagement Metrics - Employee engagement scores
- Attendance Trends - Time series attendance data

### 2. Visual Chart Components

#### Frontend Components
- **Location**: `frontend/src/components/charts/`
- **Libraries Used**: ApexCharts (vue-apexcharts)

#### Chart Types
- `AttendanceHeatmap.vue` - Calendar heatmap
- `PayrollTrendChart.vue` - Area/line charts
- `LeaveUtilizationChart.vue` - Donut/pie charts
- `PerformanceRadarChart.vue` - Radar charts
- `WorkforceDemographics.vue` - Multiple chart types
- `CostAnalysisChart.vue` - Stacked bar charts
- `AttendanceTrendChart.vue` - Time series line charts
- `EmployeeEngagementGauge.vue` - Radial gauge charts

### 3. Dashboard Views

#### Employee Portal
- **Personal Dashboard**: `frontend/src/views/analytics/PersonalDashboard.vue`
  - Personalized welcome section
  - Quick stats cards
  - Attendance heatmap
  - Leave utilization
  - Salary history
  - Performance scorecard

#### HR Manager Dashboards
- **Executive Dashboard**: `frontend/src/views/hr_dashboard/ExecutiveDashboard.vue`
  - Real-time workforce metrics
  - Department comparisons
  - Cost center analytics
  - Engagement scores

- **Operational Dashboard**: `frontend/src/views/hr_dashboard/OperationalDashboard.vue`
  - Pending approvals queue
  - Team attendance overview
  - Leave calendar view
  - Payroll processing status

### 4. Workflow Automation

#### Features
- **Leave Predictor**: `hrms/automation/leave_predictor.py`
  - ML-based leave pattern analysis
  - Predictive leave requests
  - Workload balancing suggestions

- **Approval Engine**: `hrms/automation/approval_engine.py`
  - Intelligent routing based on hierarchy
  - Workload-based delegation
  - Auto-escalation rules

- **Chatbot**: `hrms/automation/chatbot/assistant.py`
  - Employee self-service queries
  - Leave balance inquiries
  - Policy information retrieval

### 5. Employee Engagement

#### Features
- **Employee Pulse Surveys**: `hrms/engagement/doctype/employee_pulse/`
  - Regular sentiment tracking
  - Anonymous feedback collection
  - Engagement score calculation

- **Recognition & Rewards**: `hrms/engagement/doctype/employee_recognition/`
  - Peer recognition system
  - Achievement badges
  - Reward points integration

- **Announcements**: API endpoints for company-wide announcements

### 6. Performance Management

#### Features
- **360-Degree Feedback**: `hrms/performance/api/performance.py`
  - Multi-source feedback collection
  - Peer, manager, and self-assessments

- **Goal Tracking**: `hrms/performance/api/performance.py`
  - OKR/KPI tracking
  - Progress visualization

- **Skills Matrix**: `hrms/performance/api/performance.py`
  - Skill gap analysis
  - Training recommendations

## Design System

### Color Palette
- **Location**: `frontend/src/theme/colors.css`
- Modern gradient schemes
- Dark mode support
- Accessibility-compliant contrast

### Chart Styling
- **Location**: `frontend/src/theme/charts.css`
- Consistent chart styling
- Responsive layouts
- Dashboard grid system

## API Endpoints

### Analytics
- `hrms.analytics.api.charts.get_attendance_heatmap_data`
- `hrms.analytics.api.charts.get_payroll_trends`
- `hrms.analytics.api.charts.get_leave_utilization`
- `hrms.analytics.api.charts.get_performance_metrics`
- `hrms.analytics.api.charts.get_workforce_demographics`
- `hrms.analytics.api.charts.get_cost_analysis`
- `hrms.analytics.api.charts.get_engagement_metrics`
- `hrms.analytics.api.charts.get_attendance_trends`

### Automation
- `hrms.automation.leave_predictor.get_leave_predictions`
- `hrms.automation.leave_predictor.get_workload_suggestions`
- `hrms.automation.approval_engine.get_approval_workload_status`
- `hrms.automation.approval_engine.get_delegation_suggestion`
- `hrms.automation.chatbot.assistant.chat_with_assistant`

### Engagement
- `hrms.engagement.api.engagement.get_engagement_score`
- `hrms.engagement.api.engagement.get_recognition_summary`
- `hrms.engagement.api.engagement.get_announcements`

### Performance
- `hrms.performance.api.performance.get_360_feedback`
- `hrms.performance.api.performance.get_goal_progress`
- `hrms.performance.api.performance.get_skills_matrix`

## Permissions & Security

- Role-based access control for analytics
- Data filtering based on user permissions
- Department-level data isolation
- Employee can only view their own data
- HR Managers can view department/company data
- System Managers have full access

## Testing

### Unit Tests
- Data aggregation functions
- Permission checks
- API endpoint validation

### Integration Tests
- Chart data retrieval
- Dashboard rendering
- Permission enforcement

## Usage Examples

### Accessing Analytics in Frontend
```javascript
import { attendanceHeatmapData } from "@/data/analytics"

// Load data
attendanceHeatmapData.reload()

// Use in component
const data = computed(() => attendanceHeatmapData.data)
```

### Using Chart Components
```vue
<template>
  <AttendanceHeatmap :employee="employee" period="month" />
</template>

<script setup>
import AttendanceHeatmap from "@/components/charts/AttendanceHeatmap.vue"
</script>
```

## Future Enhancements

- Real-time data updates
- Export functionality for charts
- Custom dashboard builder
- Advanced ML predictions
- Integration with external analytics tools
