# Nexelya Construction

A comprehensive construction management platform built on Frappe/ERPNext.

## Features

### Core Construction Management
- **Job Site Management** - Enhanced project tracking with construction-specific fields
- **Job Costing** - Real-time budget tracking with CSI MasterFormat cost codes
- **Change Order Management** - PCO, COR, and approved change order workflows

### Field Operations
- **Daily Field Reports** - Mobile-friendly daily logs with weather integration
- **Punch Lists** - Track and manage punch items with photo documentation
- **Site Inspections** - Configurable checklists and inspection workflows

### Scheduling
- **Gantt Charts** - Visual project scheduling with drag-and-drop
- **CPM Scheduling** - Critical Path Method with float calculations
- **Resource Management** - Crew and equipment scheduling

### Document Control
- **Drawing Management** - Integration with Frappe Drive for blueprints
- **Version Control** - Track drawing revisions and markups
- **RFI Management** - Request for Information workflow
- **Submittals** - Submittal register and approval workflow

### Dashboards & Reporting
- **Project Dashboard** - Real-time project health metrics
- **Executive Dashboard** - Portfolio-wide visibility
- **Cost Reports** - Budget vs. actual analysis

## Installation

```bash
bench get-app construction
bench --site [site-name] install-app construction
```

## Requirements

- Frappe Framework v15+
- ERPNext v15+
- Python 3.10+

## License

AGPLv3

## Support

For support, please contact support@nexelya.io
