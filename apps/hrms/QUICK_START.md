# Quick Start Guide - HRMS Analytics & UI Redesign

## 🚀 Quick Setup (5 minutes)

### 1. Install Dependencies
```bash
cd /home/ubuntu/frappe-bench/apps/hrms/frontend
yarn install
```

### 2. Build Frontend
```bash
yarn build
```

### 3. Migrate Database
```bash
cd /home/ubuntu/frappe-bench
bench migrate
```

### 4. Restart Services
```bash
bench restart
```

## 📊 Accessing the New Features

### For Employees
1. Login to HRMS app
2. Navigate to **Home** - See enhanced dashboard with analytics preview
3. Click **"View All"** in Analytics section or go to `/dashboard/analytics`
4. Explore:
   - Attendance Heatmap
   - Leave Utilization
   - Salary History
   - Performance Metrics

### For HR Managers
1. Login as HR Manager
2. Access **Executive Dashboard** at `/dashboard/hr/executive`
   - Workforce Demographics
   - Cost Analysis
   - Engagement Metrics
3. Access **Operational Dashboard** at `/dashboard/hr/operational`
   - Pending Approvals
   - Team Attendance
   - Leave Calendar

## 🎨 Chart Types Available

| Chart Component | Use Case | Location |
|----------------|----------|----------|
| AttendanceHeatmap | Calendar view of attendance | `components/charts/AttendanceHeatmap.vue` |
| PayrollTrendChart | Salary trends over time | `components/charts/PayrollTrendChart.vue` |
| LeaveUtilizationChart | Leave usage breakdown | `components/charts/LeaveUtilizationChart.vue` |
| PerformanceRadarChart | Multi-dimensional performance | `components/charts/PerformanceRadarChart.vue` |
| WorkforceDemographics | Age, gender, department stats | `components/charts/WorkforceDemographics.vue` |
| CostAnalysisChart | Payroll cost breakdown | `components/charts/CostAnalysisChart.vue` |
| AttendanceTrendChart | Time series attendance | `components/charts/AttendanceTrendChart.vue` |
| EmployeeEngagementGauge | Engagement score | `components/charts/EmployeeEngagementGauge.vue` |

## 🔧 API Endpoints

### Analytics
```python
# Get attendance heatmap
GET /api/method/hrms.analytics.api.charts.get_attendance_heatmap_data
Params: employee, department, period

# Get payroll trends
GET /api/method/hrms.analytics.api.charts.get_payroll_trends
Params: employee, department, period

# Get leave utilization
GET /api/method/hrms.analytics.api.charts.get_leave_utilization
Params: employee, department, period
```

### Automation
```python
# Get leave predictions
GET /api/method/hrms.automation.leave_predictor.get_leave_predictions
Params: employee

# Get approval workload
GET /api/method/hrms.automation.approval_engine.get_approval_workload_status
Params: approver

# Chat with assistant
POST /api/method/hrms.automation.chatbot.assistant.chat_with_assistant
Params: query, employee
```

## 💡 Usage Examples

### Using Chart Components
```vue
<template>
  <AttendanceHeatmap 
    :employee="employeeName" 
    period="month" 
  />
</template>

<script setup>
import AttendanceHeatmap from "@/components/charts/AttendanceHeatmap.vue"
</script>
```

### Using Analytics Composable
```vue
<script setup>
import { useAnalytics } from "@/composables"

const {
  attendanceHeatmap,
  payrollTrends,
  selectedPeriod,
  reloadAll
} = useAnalytics()

// Load data
attendanceHeatmap.reload()
</script>
```

### Using Stat Cards
```vue
<template>
  <StatCard
    :value="100"
    label="Total Employees"
    variant="blue"
    :change="5"
    change-label="this month"
  />
</template>
```

## 🎯 Key Features

✅ **8 Chart Types** - Comprehensive visualization options
✅ **3 Dashboard Views** - Personal, Executive, Operational
✅ **Role-Based Access** - Secure data access
✅ **Caching** - 30-minute cache for performance
✅ **Responsive Design** - Works on all devices
✅ **Dark Mode Ready** - Theme support included

## 📝 Next Steps

1. **Customize Colors**: Edit `frontend/src/theme/colors.css`
2. **Add More Charts**: Create new components in `components/charts/`
3. **Extend Analytics**: Add functions to `hrms/analytics/utils/data_aggregator.py`
4. **Configure Permissions**: Modify `hrms/analytics/utils/permissions.py`

## 🐛 Troubleshooting

**Charts not showing?**
- Check browser console for errors
- Verify API endpoints are accessible
- Check user permissions

**Data not loading?**
- Check Frappe logs
- Verify database has data
- Clear cache: `bench clear-cache`

**Build errors?**
- Run `yarn install` again
- Check Node.js version (requires 16+)
- Clear node_modules and reinstall

## 📚 Documentation

- **Full Features**: See `ANALYTICS_FEATURES.md`
- **Implementation**: See `IMPLEMENTATION_NOTES.md`
- **Changes**: See `CHANGELOG.md`

## 🎉 You're All Set!

The HRMS app now has comprehensive analytics and a modern UI. Start exploring the dashboards and charts!
