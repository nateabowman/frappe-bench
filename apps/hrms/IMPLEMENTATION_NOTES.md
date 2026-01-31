# HRMS Analytics & UI Redesign - Implementation Notes

## Installation Steps

### 1. Install Frontend Dependencies
```bash
cd frontend
yarn install
```

This will install:
- apexcharts
- vue-apexcharts
- chart.js
- vue-chartjs

### 2. Build Frontend
```bash
yarn build
```

### 3. Migrate Database
```bash
bench migrate
```

This will create the new doctypes:
- Employee Pulse
- Employee Recognition

### 4. Restart Bench
```bash
bench restart
```

## API Endpoints

All analytics endpoints are whitelisted and accessible via:
- `/api/method/hrms.analytics.api.charts.<method_name>`
- `/api/method/hrms.automation.<module>.<method_name>`
- `/api/method/hrms.engagement.api.engagement.<method_name>`
- `/api/method/hrms.performance.api.performance.<method_name>`

## Frontend Routes

New routes added:
- `/dashboard/analytics` - Personal Analytics Dashboard
- `/dashboard/hr/executive` - Executive Dashboard (HR Managers)
- `/dashboard/hr/operational` - Operational Dashboard (HR Managers)

## Component Usage

### Chart Components
All chart components are in `frontend/src/components/charts/`:
- Use `<AttendanceHeatmap>` for calendar-based attendance
- Use `<PayrollTrendChart>` for salary trends
- Use `<LeaveUtilizationChart>` for leave analysis
- Use `<PerformanceRadarChart>` for performance metrics
- Use `<WorkforceDemographics>` for demographics
- Use `<CostAnalysisChart>` for cost breakdowns
- Use `<AttendanceTrendChart>` for time series
- Use `<EmployeeEngagementGauge>` for engagement scores

### Utility Components
- `<StatCard>` - Reusable stat card with variants
- `<MetricCard>` - Metric display with gradients

### Composable
Use `useAnalytics()` composable for managing analytics data:
```javascript
import { useAnalytics } from "@/composables"

const {
  attendanceHeatmap,
  payrollTrends,
  selectedPeriod,
  reloadAll
} = useAnalytics()
```

## Permissions

### Employee Role
- Can view own analytics data
- Can create Employee Pulse surveys
- Can create Employee Recognition

### HR Manager Role
- Can view department analytics
- Can view all employee data
- Can manage engagement features

### System Manager Role
- Full access to all analytics
- Can view company-wide data

## Caching

Analytics data is cached for 30 minutes by default. Cache keys follow pattern:
- `hrms:analytics:<chart_type>:emp:<employee>:period:<period>`
- `hrms:analytics:<chart_type>:dept:<department>:period:<period>`

To invalidate cache:
```python
from hrms.analytics.utils.cache import invalidate_analytics_cache
invalidate_analytics_cache()  # All analytics
invalidate_analytics_cache("attendance*")  # Specific pattern
```

## Scheduled Jobs

New scheduled jobs:
- `auto_escalate_pending_approvals` - Runs daily, escalates approvals > 3 days old
- `send_engagement_reminders` - Runs weekly, sends pulse survey reminders

## Customization

### Chart Colors
Edit `frontend/src/theme/colors.css` to customize chart color schemes.

### Dashboard Layouts
Modify dashboard Vue files in:
- `frontend/src/views/analytics/PersonalDashboard.vue`
- `frontend/src/views/hr_dashboard/ExecutiveDashboard.vue`
- `frontend/src/views/hr_dashboard/OperationalDashboard.vue`

### Data Aggregation
Modify aggregation functions in:
- `hrms/analytics/utils/data_aggregator.py`

## Troubleshooting

### Charts Not Rendering
1. Check browser console for errors
2. Verify ApexCharts is installed: `yarn list apexcharts`
3. Check API endpoints are accessible
4. Verify permissions for user role

### Data Not Loading
1. Check Frappe logs for API errors
2. Verify database has required data
3. Check cache isn't stale
4. Verify user has proper permissions

### Performance Issues
1. Enable caching (default: 30 minutes)
2. Reduce date range for large datasets
3. Add database indexes on date fields
4. Use pagination for large result sets

## Testing

### Manual Testing
1. Access `/dashboard/analytics` as employee
2. Access `/dashboard/hr/executive` as HR Manager
3. Test chart interactions
4. Verify data accuracy
5. Test permissions

### API Testing
```bash
# Test attendance heatmap
curl -X POST http://localhost:8000/api/method/hrms.analytics.api.charts.get_attendance_heatmap_data \
  -H "Authorization: token <api_key>:<api_secret>" \
  -d '{"employee": "EMP-00001", "period": "month"}'
```

## Future Enhancements

1. Real-time data updates via websockets
2. Export charts as PDF/PNG
3. Custom dashboard builder
4. Advanced ML predictions
5. Integration with external BI tools
6. Mobile app support
7. Offline data caching
