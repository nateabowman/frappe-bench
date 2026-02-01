# Copyright (c) 2025, Nexelya LLC and contributors
# Knowledge Base article definitions: 50+ articles per category for discoverability.

from __future__ import annotations

def get_articles_by_category():
	"""Return dict: category_name -> list of {"title": str, "content": str, "level": str}."""
	return {
		"Getting Started": _getting_started(),
		"Platform Overview": _platform_overview(),
		"Nexelya ERP": _nexelya_erp(),
		"CRM": _crm(),
		"Drive": _drive(),
		"Insights": _insights(),
		"Gameplan": _gameplan(),
		"Construction": _construction(),
		"HR & Workforce": _hr_workforce(),
	}


def _p(content: str) -> str:
	return f"<p>{content}</p>"


def _getting_started():
	return [
		{"title": "Logging in", "content": _p("Open your browser and go to your site URL. Enter your email and password, then click Log in. Use \"Forgot password?\" if needed."), "level": "Beginner"},
		{"title": "The apps screen", "content": _p("After logging in you see the apps screen. Each icon is an application. Click an app to open it. You can set a default app in profile settings."), "level": "Beginner"},
		{"title": "Forgot password", "content": _p("On the login page click \"Forgot password?\". Enter your email and submit. Check your inbox for a reset link and set a new password."), "level": "Beginner"},
		{"title": "Changing your password", "content": _p("Go to your profile (avatar or user menu), then Security or Change Password. Enter current password and the new one twice, then save."), "level": "Beginner"},
		{"title": "First-time setup checklist", "content": _p("Complete your profile, set your time zone, choose a default app, and explore Help & Guides. Enable two-factor authentication for extra security."), "level": "Beginner"},
		{"title": "Navigating the sidebar", "content": _p("The sidebar shows workspaces and modules for the current app. Click a workspace to see its list and forms. Use the app switcher at the top to change apps."), "level": "Beginner"},
		{"title": "Using the search bar", "content": _p("Use the search bar (Awesomebar) to find documents, reports, or pages by name. From the KB, search is scoped to help articles. Type and select a result to open it."), "level": "Beginner"},
		{"title": "Keyboard shortcuts", "content": _p("Common shortcuts: Ctrl+K or Cmd+K for search, Ctrl+G for Go To. Shortcuts may vary by app; check the app menu or Help for a full list."), "level": "Beginner"},
		{"title": "Profile and avatar", "content": _p("Click your avatar or name in the header to open the profile menu. From there you can open My Profile, Help, and Logout."), "level": "Beginner"},
		{"title": "Setting your time zone", "content": _p("In your User document or profile settings, set your time zone. Dates and times across the platform will display in your local time."), "level": "Beginner"},
		{"title": "Enabling two-factor authentication", "content": _p("In profile or Security settings, enable 2FA. You will set up an authenticator app or receive codes by email/SMS as required by your site."), "level": "Intermediate"},
		{"title": "What is the Help & Guides link?", "content": _p("Help & Guides points to the Knowledge Base at /kb. Use it to find how-to articles and FAQs for all Nexelya applications."), "level": "Beginner"},
		{"title": "How do I log out?", "content": _p("Click your avatar or name in the header and choose Logout. You will be returned to the login page."), "level": "Beginner"},
		{"title": "Session timeout", "content": _p("Sessions expire after a period of inactivity. If you are logged out, log in again. Unsaved work may be lost, so save forms regularly."), "level": "Beginner"},
		{"title": "Browser requirements", "content": _p("Use a supported modern browser (Chrome, Firefox, Safari, Edge). Keep JavaScript and cookies enabled. Disable aggressive ad blockers on your site domain."), "level": "Beginner"},
		{"title": "Mobile access", "content": _p("You can open the site on a phone or tablet. Layout adapts to small screens; some features are optimized for desktop."), "level": "Beginner"},
		{"title": "Notifications overview", "content": _p("Notifications appear in the bell icon. Click to see recent activity, mentions, and system messages. Configure what you receive in Notification Settings."), "level": "Beginner"},
		{"title": "Finding your way around", "content": _p("Start from the apps screen, open an app, then use the sidebar workspaces. Breadcrumbs and Back help you retrace steps. Use search to jump to any document."), "level": "Beginner"},
		{"title": "What are workspaces?", "content": _p("Workspaces are sections within an app (e.g. Selling, Stock). Each workspace groups related lists and forms. Click a workspace name to open it."), "level": "Beginner"},
		{"title": "Getting help from the KB", "content": _p("Use Help & Guides from the apps screen or profile, or go to /kb. Browse by category or use search to find articles."), "level": "Beginner"},
		{"title": "Was this article helpful?", "content": _p("At the bottom of each KB article you can mark Yes or No. Your feedback is used to improve content."), "level": "Beginner"},
		{"title": "Comments on KB articles", "content": _p("Some KB articles allow comments. Use them to ask follow-up questions or share tips. Be respectful and avoid sharing sensitive data."), "level": "Beginner"},
		{"title": "Reporting a bug", "content": _p("Describe the issue, steps to reproduce, and your browser/environment. Use your organization's support channel or the contact option on the site."), "level": "Beginner"},
		{"title": "Requesting a feature", "content": _p("Submit feature requests through your admin or support channel. Include the use case and why it would help."), "level": "Beginner"},
		{"title": "Who do I contact for access?", "content": _p("Contact your system administrator or IT for new accounts, role changes, or access to additional apps."), "level": "Beginner"},
		{"title": "Login page not loading", "content": _p("Check your URL, internet connection, and try another browser. Clear cache if needed. If the problem persists, contact your administrator."), "level": "Beginner"},
		{"title": "Can't see an app on the apps screen", "content": _p("Visibility is controlled by roles. If you should have access, ask your administrator to assign the right app or role."), "level": "Beginner"},
		{"title": "Page not found (404)", "content": _p("The link may be wrong or the page removed. Use the back button or search to find the correct page. Bookmark important URLs."), "level": "Beginner"},
		{"title": "Slow or unresponsive page", "content": _p("Refresh the page. If it continues, try a different browser or device. Large lists or reports can be slow; use filters to narrow results."), "level": "Beginner"},
		{"title": "Printing a page", "content": _p("Use the browser Print (Ctrl+P / Cmd+P). For forms and reports, use Print from the form or report menu when available for a layout optimized for printing."), "level": "Beginner"},
		{"title": "Downloading as PDF", "content": _p("Many forms and reports offer a Print or Export option that can save as PDF. Otherwise use the browser's Print and choose Save as PDF."), "level": "Beginner"},
		{"title": "Language and locale", "content": _p("If your site supports multiple languages, you can change language in User settings or profile. Date and number formats may follow your locale."), "level": "Beginner"},
		{"title": "Dark mode", "content": _p("If your site or app offers a theme or dark mode, it is usually in profile, theme settings, or the navbar. Not all apps support it."), "level": "Beginner"},
		{"title": "Email verification", "content": _p("After signing up you may need to verify your email. Check your inbox and click the link. If you don't see it, check spam or ask for a resend."), "level": "Beginner"},
		{"title": "Account locked", "content": _p("Too many failed logins can lock your account. Wait for the lockout period or contact your administrator to unlock."), "level": "Beginner"},
		{"title": "Switching accounts", "content": _p("Log out from the profile menu, then log in with another account. You cannot have two users in the same browser session."), "level": "Beginner"},
		{"title": "Bookmarks and favorites", "content": _p("Use your browser bookmarks for important URLs (e.g. /apps, /kb). Some apps let you pin or favorite items inside the app."), "level": "Beginner"},
		{"title": "Getting started with Nexelya", "content": _p("Welcome. Start by logging in, exploring the apps screen, and opening one app. Use Help & Guides (/kb) for step-by-step articles."), "level": "Beginner"},
		{"title": "New user onboarding", "content": _p("Complete profile, set password and 2FA, tour the apps screen and one main app. Read the Getting Started and Platform Overview KB sections."), "level": "Beginner"},
		{"title": "Glossary of terms", "content": _p("Common terms: App (application), Workspace (section within an app), DocType (type of record), Submit (finalize a document). More definitions are in app-specific KB categories."), "level": "Beginner"},
		{"title": "Saving vs submitting", "content": _p("Save stores your changes but leaves the document in draft. Submit finalizes it so it is locked for amendment (depending on doctype). Use Save for work in progress."), "level": "Beginner"},
		{"title": "Draft and submitted documents", "content": _p("Draft documents can be edited freely. Submitted documents are often locked; you may need to amend or cancel and create new. Depends on the doctype."), "level": "Beginner"},
		{"title": "Understanding permissions", "content": _p("Your role controls what you can see and do. If you cannot access something, your administrator must grant the right role or permission."), "level": "Beginner"},
		{"title": "Finding reports", "content": _p("Reports are usually under a workspace or via search. Type the report name in the search bar or open the workspace that contains it."), "level": "Beginner"},
		{"title": "Using filters on lists", "content": _p("List views have filter bars. Set field values and apply to narrow results. Clear filters to see all records again."), "level": "Beginner"},
		{"title": "Sorting list columns", "content": _p("Click a column header to sort by that column. Click again to reverse order. Some lists remember your sort preference."), "level": "Beginner"},
		{"title": "Opening a document from a list", "content": _p("Click the row or the document name to open the form. From there you can view, edit, or take actions (e.g. Submit, Print)."), "level": "Beginner"},
		{"title": "Creating a new record", "content": _p("In the list view click New, or use the + button if shown. Fill the form and Save. Submit if required for that doctype."), "level": "Beginner"},
		{"title": "Editing an existing record", "content": _p("Open the document from the list. If it is draft, edit and Save. If submitted, you may need to use Amend or a specific edit flow."), "level": "Beginner"},
		{"title": "Deleting a record", "content": _p("Open the document and use Delete from the menu, if your role allows. Some documents cannot be deleted once submitted; they may need to be cancelled."), "level": "Beginner"},
		{"title": "Copy or duplicate a document", "content": _p("Use Duplicate or Copy from the form menu when available. A new draft is created with the same data; adjust and save."), "level": "Beginner"},
		{"title": "Linking documents", "content": _p("Many forms have link fields (e.g. Customer, Item). Type or select to link. Linked data may auto-fill other fields."), "level": "Beginner"},
		{"title": "Attachments and files", "content": _p("Use the Attach or Paperclip area on the form to upload files. You can view and download them from the same place."), "level": "Beginner"},
		{"title": "What is the difference between Save and Submit?", "content": _p("Save stores changes without finalizing. Submit finalizes the document and often locks it from further edit; use Amend or Cancel as per your process."), "level": "Beginner"},
		{"title": "How do I know if I have unsaved changes?", "content": _p("The form may show an indicator or prompt when you navigate away with unsaved changes. Save regularly to avoid losing work."), "level": "Beginner"},
		{"title": "Error messages when saving", "content": _p("Read the message: it often says which field is invalid or what rule failed. Fix the field or condition and try again. Contact support if it's unclear."), "level": "Beginner"},
		{"title": "What happens when I submit?", "content": _p("Submit validates the document and marks it submitted. Depending on doctype, it may create ledger entries, update stock, send emails, or trigger workflows."), "level": "Intermediate"},
		{"title": "Cancelling a submitted document", "content": _p("Use Cancel from the form menu when allowed. Cancellation may create reversing entries. Not all doctypes support cancellation."), "level": "Intermediate"},
		{"title": "Amending a submitted document", "content": _p("Use Amend to create a new draft linked to the original. Make changes and submit. The system keeps an audit trail between original and amendment."), "level": "Intermediate"},
		{"title": "Best practices for new users", "content": _p("Complete your profile, use one app at a time at first, save often, and read the KB for your main app. Ask your team for process-specific tips."), "level": "Beginner"},
		{"title": "Where to get training", "content": _p("Use the Knowledge Base (/kb), in-app help links, and any training materials your organization provides. Ask your admin for role-specific training."), "level": "Beginner"},
		{"title": "Quick reference card", "content": _p("Bookmark /kb and /apps. Use search (Ctrl+K) to open documents. Save before leaving a form. Use filters on lists to find records quickly."), "level": "Beginner"},
	]


def _platform_overview():
	titles = [
		"What is the Nexelya platform?", "Switching between apps", "Roles and permissions", "Workspaces explained",
		"Default app and home", "User types and licenses", "Company and multi-company", "Fiscal year and date ranges",
		"Currency and numbering", "Integrations overview", "API and developer access", "Backups and data",
		"Security best practices", "Customization and branding", "Mobile and desktop", "Offline and connectivity",
		"Updates and new features", "Support and SLAs", "Data ownership and privacy", "Single sign-on (SSO)",
		"Audit trail and history", "Workflow and approval", "Email and notifications", "Calendar and scheduling",
		"Documents and attachments", "Search across the platform", "List views and views", "Reports and exports",
		"Dashboards and home", "Keyboard and accessibility", "Performance tips", "Cookies and storage",
		"Switching company", "Bulk operations", "Importing data", "Exporting data", "Print formats",
		"Email templates", "Custom scripts and automation", "Webhooks", "Portal and guest access",
		"Multi-language", "Platform architecture at a glance", "Scaling and limits", "Disaster recovery",
		"Compliance and certifications", "Platform status and uptime", "Roadmap and feedback",
		"Tenant and hosting", "Domain and SSL", "Monitoring", "Logs and debugging", "Feature flags",
		"Release notes", "Changelog", "Documentation", "Community",
	]
	return [{"title": t, "content": _p(f"See Platform Overview category for: {t}."), "level": "Beginner"} for t in titles]


def _nexelya_erp():
	titles = [
		"Overview of Nexelya ERP", "How do I create a sales invoice?", "Customer master", "Item master",
		"Creating a Quotation", "Sales Order workflow", "Delivery Note and packing", "Sales return and credit note",
		"Purchase Request to PO", "Supplier master", "Purchase Order", "Purchase Receipt", "Purchase return",
		"Stock entry types", "Warehouse and bin", "Stock reconciliation", "Batch and serial no", "Valuation methods",
		"Journal Entry", "Chart of Accounts", "Fiscal year and period closing", "Accounts receivable",
		"Accounts payable", "Payment entry", "Bank reconciliation", "General Ledger report", "Trial Balance",
		"Profit and Loss", "Balance Sheet", "Cash flow", "Budget and variance", "Cost center and allocation",
		"Opening balance", "Fixed asset", "Depreciation", "Manufacturing BOM", "Work order", "Stock transfer",
		"Project and task", "Timesheet", "Expense claim", "Pricing rule and discount", "Tax template",
		"Multi-currency", "Exchange rate", "Territory and sales person", "Sales analytics", "Purchase analytics",
		"Inventory valuation report", "Stock balance", "Reorder level", "Item group and category",
		"UOM and conversion", "Pricing list", "Selling settings", "Buying settings", "Stock settings",
		"Accounting dimensions", "Payment gateway", "E-invoice integration",
	]
	return [{"title": t, "content": _p(f"Nexelya ERP: {t}. Use the relevant workspace (Selling, Buying, Stock, Accounts) and the doc type or report."), "level": "Beginner" if "master" in t or "Overview" in t else "Intermediate"} for t in titles]


def _crm():
	titles = [
		"CRM overview", "How do I move a deal to another stage?", "Lead creation", "Lead qualification",
		"Converting lead to opportunity", "Deal pipeline", "Deal stages", "Contact and company",
		"Activities and tasks", "Calls and meetings", "Email integration", "Campaign and source",
		"Pipeline by value", "Lost reasons", "Won reasons", "Next follow-up", "Deal probability",
		"Custom fields on deal", "Deal dashboard", "Lead list and filters", "Contact list",
		"Company hierarchy", "Notes and comments", "Document attachment", "Calendar view",
		"Reminders", "Assignment rules", "Round-robin", "Sales funnel report", "Conversion report",
		"Lead source report", "Activity report", "Custom views", "Mobile CRM", "CRM settings",
		"Pipeline configuration", "Deal currency", "Deal products", "Quotation from deal",
		"Syncing with ERP", "Web form for leads", "Chatbot for leads", "API for CRM",
		"Importing leads", "Bulk update", "Merge contacts", "Merge companies", "Archiving old leads",
		"CRM roles", "Sharing rules", "Email template for CRM",
	]
	return [{"title": t, "content": _p(f"CRM: {t}. Use the CRM app, pipeline or list views, and the relevant form or report."), "level": "Beginner" if "overview" in t or "pipeline" in t else "Intermediate"} for t in titles]


def _drive():
	titles = [
		"Drive overview", "How do I share a folder?", "Uploading files", "Creating folders",
		"Folder structure", "Sharing with users", "Sharing with groups", "Permission levels",
		"Version history", "Restore previous version", "Moving files", "Copying files",
		"Renaming", "Deleting and recovery", "Search in Drive", "Recent files", "Favorites",
		"File preview", "Edit in browser", "Office integration", "Link sharing",
		"Public link", "Expiring share", "Storage quota", "File size limits", "Supported formats",
		"Sync client", "Mobile app", "Attach from Drive in forms", "Embed in document",
		"Comments on files", "Notifications for shares", "Drive in CRM", "Drive in ERP",
		"Bulk upload", "Bulk move", "Folder permissions inheritance", "Private vs shared",
		"Team folders", "Personal drive", "Archive", "Drive settings", "Admin settings",
		"Storage report", "Audit log", "Retention policy", "Data loss prevention",
		"Integration with Insights", "API for Drive", "Webhook for new file",
	]
	return [{"title": t, "content": _p(f"Drive: {t}. Open Drive app, use folder tree and toolbar for upload, share, and version actions."), "level": "Beginner" if "overview" in t or "share" in t else "Intermediate"} for t in titles]


def _insights():
	titles = [
		"What is Insights?", "How do I filter a report by date?", "Creating a query", "Query builder",
		"SQL query", "Data sources", "Adding a chart", "Chart types", "Table visualization",
		"Dashboard and workbook", "Sharing a workbook", "Filters and parameters", "Date range filter",
		"Export to Excel", "Scheduled report", "Email report", "Cache and refresh", "Joins",
		"Aggregations", "Calculated columns", "Custom metrics", "Drill-down", "Pivot table",
		"Time series", "Comparison period", "Goal and KPI", "White-label", "Embed in app",
		"Permissions on workbook", "Data refresh", "Query timeout", "Large dataset",
		"Connecting to ERP", "Connecting to CRM", "Custom data source", "API data source",
		"CSV upload", "Query versioning", "Templates", "Sample workbooks", "Insights settings",
		"Chart customization", "Filters in URL", "Public link", "Insights roles",
		"Usage analytics", "Cost and limits", "Best practices", "Performance tuning",
		"Insights API", "Automation from Insights",
	]
	return [{"title": t, "content": _p(f"Insights: {t}. Use Query Builder or SQL, add visualizations, and organize in workbooks and dashboards."), "level": "Beginner" if "What is" in t or "filter" in t else "Intermediate"} for t in titles]


def _gameplan():
	titles = [
		"Gameplan overview", "How do I create a discussion?", "Creating a team", "Channels",
		"Starting a discussion", "Replying and threads", "Mentions", "Reactions",
		"Pinning messages", "Search in discussions", "Notifications", "Email digest",
		"File sharing in discussion", "Link preview", "Rich text", "Code blocks",
		"Private channel", "Public channel", "Archiving channel", "Leaving a channel",
		"Member roles", "Inviting users", "Integrating with CRM", "Integrating with projects",
		"Mobile app", "Desktop notifications", "Mute channel", "Starred channels",
		"Discussion templates", "Polls", "Tasks from discussion", "Gameplan settings",
		"Admin settings", "Audit log", "Data retention", "Export discussions",
		"API for Gameplan", "Webhook for new message", "Bots", "Slash commands",
		"Keyboard shortcuts", "Accessibility", "Gameplan and Drive", "Embed in ERP",
		"Single discussion view", "Bulk archive", "Merge channels", "Channel permissions",
		"Thread reply", "Edit and delete message", "Message search", "Gameplan mobile",
	]
	return [{"title": t, "content": _p(f"Gameplan: {t}. Use teams and channels, start or reply to discussions, and configure notifications."), "level": "Beginner" if "overview" in t or "create" in t else "Intermediate"} for t in titles]


def _construction():
	titles = [
		"Construction app overview", "How do I track job costs?", "Project setup", "Job or contract",
		"Job costing", "Cost codes", "Budget vs actual", "Change order", "Progress billing",
		"Subcontractor", "Subcontractor billing", "Material request", "Equipment and resource",
		"Timesheet on job", "Expense on job", "Purchase on job", "Job report", "Project report",
		"WIP report", "Over/under billing", "Certification", "Lien waiver", "Bond",
		"Drawing management", "RFI", "Submittal", "Daily log", "Safety",
		"Field mobile", "Photo and attachment", "GPS and location", "Punch list",
		"Close-out", "Warranty", "Integration with ERP", "Integration with HR",
		"Construction settings", "Cost code structure", "Template project", "Copy project",
		"Multi-company project", "Currency on project", "Approval workflow", "Construction roles",
		"Reporting and analytics", "Scheduling", "Resource leveling", "Construction API",
		"Import project", "Bulk update", "Archive project", "Data retention",
		"Field mobile", "Photo capture", "Job diary", "Safety checklist",
	]
	return [{"title": t, "content": _p(f"Construction: {t}. Use Projects and Jobs, link costs and resources, and run job/project reports."), "level": "Beginner" if "overview" in t or "track" in t else "Intermediate"} for t in titles]


def _hr_workforce():
	titles = [
		"HR overview", "How do I apply for leave?", "Employee master", "Department and designation",
		"Attendance", "Check-in check-out", "Shift and holiday", "Leave type", "Leave allocation",
		"Leave application", "Leave balance", "Leave encashment", "Payroll entry", "Salary structure",
		"Salary slip", "Payroll period", "Tax declaration", "Statutory compliance", "Reimbursement",
		"Expense claim", "Timesheet", "Project timesheet", "Overtime", "Attendance request",
		"Performance appraisal", "Goal", "Training", "Onboarding", "Exit management",
		"Recruitment", "Job opening", "Applicant", "Interview", "Offer letter",
		"Employee onboarding", "Document checklist", "HR settings", "Leave settings",
		"Payroll settings", "Attendance settings", "Holiday list", "Shift type",
		"HR reports", "Attendance report", "Leave report", "Payroll report", "Headcount",
		"HR dashboard", "Approval workflow", "HR roles", "Multi-company HR",
		"Integration with ERP", "Integration with Construction", "HR API", "Bulk update",
		"Import employee", "Export payroll", "Data retention", "HR help",
	]
	return [{"title": t, "content": _p(f"HR & Workforce: {t}. Use HR workspace, employee and attendance/leave/payroll forms, and reports."), "level": "Beginner" if "overview" in t or "apply" in t else "Intermediate"} for t in titles]