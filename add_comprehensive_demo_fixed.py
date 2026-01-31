#!/usr/bin/env python3
"""
Comprehensive demo data for all modules - FIXED VERSION
Uses correct doctype names and field structures
"""
import frappe
from frappe.utils import add_days, nowdate, flt
from random import randint, choice

frappe.set_user("Administrator")

print("="*80)
print("COMPREHENSIVE DEMO DATA - ALL MODULES (FIXED)")
print("="*80)

companies = frappe.get_all("Company", limit=1)
if not companies:
    print("❌ No company found!")
    exit(1)

company = companies[0].name
print(f"\n✓ Company: {company}\n")

# ============================================================================
# 1. CRM MODULE
# ============================================================================
print("="*80)
print("📞 MODULE 1: CRM")
print("="*80)

# 1.1 Leads (using "Lead" doctype, not "CRM Lead")
print("\n  📋 Creating 100 Leads...")
lead_names = [
    "TechCorp Solutions", "Digital Dynamics", "Cloud Innovations", "AI Systems Inc",
    "Data Analytics Pro", "Software Masters", "Web Dev Experts", "Mobile Apps Plus",
    "E-commerce Hub", "SaaS Platform Pro", "IT Consulting Group", "Network Solutions",
    "Security Experts", "DevOps Masters", "Cloud Infrastructure", "Big Data Corp",
    "Machine Learning Co", "IoT Solutions", "Blockchain Tech", "Fintech Innovations",
    "Healthcare Tech", "EdTech Solutions", "Retail Tech", "Manufacturing Tech",
    "Logistics Pro", "Transport Solutions", "Energy Systems", "Green Tech",
    "Media Company", "Entertainment Corp", "Sports Tech", "Fitness App",
    "Food Delivery Pro", "Travel Tech", "Real Estate Tech", "Construction Tech",
    "Agriculture Tech", "Farming Solutions", "Water Management", "Waste Solutions",
    "Renewable Energy", "Solar Systems", "Wind Power", "Hydro Energy",
    "Battery Tech", "Electric Vehicles", "Autonomous Systems", "Robotics Corp",
    "3D Printing", "Virtual Reality", "Augmented Reality", "Gaming Studio",
    "Streaming Service", "Social Media Platform", "Content Creator", "Influencer Agency",
    "Marketing Agency", "Advertising Firm", "PR Company", "Design Studio",
    "Architecture Firm", "Engineering Co", "Consulting Group", "Legal Services",
    "Accounting Firm", "Financial Services", "Insurance Co", "Banking Tech",
    "Payment Gateway", "Cryptocurrency", "Trading Platform", "Investment Firm",
    "Venture Capital", "Private Equity", "Real Estate Fund", "Property Management",
    "Facilities Management", "Cleaning Services", "Security Services", "Event Management",
    "Catering Services", "Restaurant Chain", "Hotel Group", "Travel Agency",
    "Tourism Board", "Museum", "Theater", "Concert Hall",
    "Sports Club", "Fitness Center", "Yoga Studio", "Wellness Center",
    "Spa & Salon", "Beauty Products", "Cosmetics", "Fashion Brand"
]
first_names = ["John", "Jane", "Mike", "Sarah", "David", "Emily", "Chris", "Lisa"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller"]
lead_sources = frappe.get_all("Lead Source", limit=10) or [{"name": "Website"}]
lead_statuses = frappe.get_all("CRM Lead Status", limit=10) or [{"name": "New"}]

leads_created = 0
for i, org_name in enumerate(lead_names):
    if frappe.db.exists("Lead", {"lead_name": org_name}):
        continue
    try:
        lead = frappe.new_doc("Lead")
        lead.first_name = choice(first_names)
        lead.last_name = choice(last_names)
        lead.lead_name = org_name
        lead.email = f"contact@{org_name.lower().replace(' ', '').replace('&', '')}.com"
        lead.mobile_no = f"+1{randint(2000000000, 9999999999)}"
        lead.source = choice(lead_sources).name if lead_sources else "Website"
        lead.status = choice(lead_statuses).name if lead_statuses else "New"
        lead.no_of_employees = choice(["1-10", "11-50", "51-200", "201-500", "501-1000", "1000+"])
        lead.annual_revenue = flt(randint(100000, 10000000), 2)
        lead.insert(ignore_permissions=True)
        leads_created += 1
    except Exception as e:
        pass
print(f"    ✅ Created {leads_created} Leads")

# 1.2 Opportunities
print("\n  💼 Creating 50 Opportunities...")
leads_list = frappe.get_all("Lead", limit=50)
opportunities_created = 0
for i, lead in enumerate(leads_list[:50]):
    opp_name = f"Opportunity from {lead.name}"
    if frappe.db.exists("Opportunity", opp_name):
        continue
    try:
        opp = frappe.new_doc("Opportunity")
        opp.opportunity_from = "Lead"
        opp.party_name = lead.name
        opp.status = choice(["Open", "Quotation", "Negotiation", "Converted", "Lost"])
        opp.expected_closing = add_days(nowdate(), randint(7, 90))
        opp.probability = randint(10, 90)
        opp.opportunity_amount = flt(randint(10000, 200000), 2)
        opp.insert(ignore_permissions=True)
        opportunities_created += 1
    except:
        pass
print(f"    ✅ Created {opportunities_created} Opportunities")

print("\n✅ CRM Module Complete!")

# ============================================================================
# 2. ERPNEXT - More Data
# ============================================================================
print("\n" + "="*80)
print("📦 MODULE 2: ERPNEXT")
print("="*80)

# 2.1 More Customers
print("\n  👥 Creating 50 additional Customers...")
customer_names = [
    "Alpha Industries", "Beta Corporation", "Gamma Solutions", "Delta Enterprises",
    "Epsilon Group", "Zeta Corp", "Eta Systems", "Theta Technologies",
    "Iota Services", "Kappa Industries", "Lambda Corp", "Mu Solutions",
    "Nu Enterprises", "Xi Group", "Omicron Corp", "Pi Systems",
    "Rho Technologies", "Sigma Services", "Tau Industries", "Upsilon Corp",
    "Phi Solutions", "Chi Enterprises", "Psi Group", "Omega Corp",
    "Apex Alpha", "Beta Prime", "Gamma Plus", "Delta Pro",
    "Epsilon Elite", "Zeta Premium", "Eta Standard", "Theta Basic",
    "Iota Enterprise", "Kappa Business", "Lambda Professional", "Mu Corporate",
    "Nu Commercial", "Xi Industrial", "Omicron Retail", "Pi Wholesale",
    "Rho Distribution", "Sigma Manufacturing", "Tau Production", "Upsilon Operations",
    "Phi Logistics", "Chi Supply", "Psi Chain", "Omega Network", "Prime Corp", "Elite Inc", "Summit Ltd"
]
customers_created = 0
for name in customer_names:
    if frappe.db.exists("Customer", name):
        continue
    try:
        customer = frappe.new_doc("Customer")
        customer.customer_name = name
        customer.customer_type = choice(["Company", "Individual"])
        customer.territory = choice(["All Territories", "North America", "Europe", "Asia"])
        customer.customer_group = "All Customer Groups"
        customer.insert(ignore_permissions=True)
        customers_created += 1
    except:
        pass
print(f"    ✅ Created {customers_created} Customers")

# 2.2 More Items
print("\n  📦 Creating 50 additional Items...")
item_names = [
    "Server Rack", "Network Cable", "Ethernet Switch", "Firewall Device",
    "VPN Router", "Access Point", "Network Card", "Fiber Optic Cable",
    "Patch Panel", "Cable Tester", "Network Tool", "Crimping Tool",
    "Server Blade", "Storage Array", "Backup System", "Disaster Recovery",
    "Load Balancer", "Proxy Server", "DNS Server", "Mail Server",
    "Database Server", "Web Server", "Application Server", "File Server",
    "Print Server", "Media Server", "Streaming Server", "Gaming Server",
    "Cloud Storage", "CDN Service", "Monitoring Tool", "Analytics Platform",
    "BI Dashboard", "Reporting Tool", "Data Warehouse", "ETL Tool",
    "API Gateway", "Message Queue", "Cache System", "Search Engine",
    "Documentation Tool", "Wiki System", "Issue Tracker", "Project Management",
    "Version Control", "CI/CD Tool", "Container Platform", "Orchestration Tool",
    "Service Mesh", "Microservices"
]
item_groups = frappe.get_all("Item Group", limit=1)
items_created = 0
if item_groups:
    warehouses = frappe.get_all("Warehouse", filters={"company": company, "is_group": 0}, limit=1)
    for name in item_names:
        if frappe.db.exists("Item", name):
            continue
        try:
            item = frappe.new_doc("Item")
            item.item_code = name
            item.item_name = name
            item.item_group = item_groups[0].name
            item.stock_uom = "Nos"
            item.is_stock_item = 1
            if warehouses:
                item.append("item_defaults", {
                    "company": company,
                    "default_warehouse": warehouses[0].name
                })
            item.insert(ignore_permissions=True)
            items_created += 1
        except:
            pass
print(f"    ✅ Created {items_created} Items")

# 2.3 More Sales Orders
print("\n  📋 Creating 50 additional Sales Orders...")
customers = frappe.get_all("Customer", limit=100)
items = frappe.get_all("Item", limit=100)
warehouses = frappe.get_all("Warehouse", filters={"company": company, "is_group": 0}, limit=5)
so_created = 0
if customers and items and warehouses:
    for i in range(50):
        try:
            so = frappe.new_doc("Sales Order")
            so.company = company
            so.customer = choice(customers).name
            so.transaction_date = add_days(nowdate(), -randint(1, 120))
            so.delivery_date = add_days(so.transaction_date, randint(7, 45))
            for _ in range(randint(1, 5)):
                so.append("items", {
                    "item_code": choice(items).name,
                    "qty": randint(1, 20),
                    "warehouse": choice(warehouses).name,
                    "rate": flt(randint(50, 2000), 2)
                })
            so.insert(ignore_permissions=True)
            if i % 4 == 0:
                so.submit()
            so_created += 1
        except:
            pass
print(f"    ✅ Created {so_created} Sales Orders")

print("\n✅ ERPNext Module Complete!")

# ============================================================================
# 3. HRMS MODULE
# ============================================================================
print("\n" + "="*80)
print("👥 MODULE 3: HRMS")
print("="*80)

# 3.1 More Employees
print("\n  👤 Creating 40 Employees...")
first_names = ["John", "Jane", "Mike", "Sarah", "David", "Emily", "Chris", "Lisa", "Robert", "Maria",
               "James", "Patricia", "Michael", "Jennifer", "William", "Linda", "Richard", "Barbara",
               "Joseph", "Elizabeth", "Thomas", "Susan", "Charles", "Jessica", "Daniel", "Sarah",
               "Matthew", "Nancy", "Anthony", "Karen", "Mark", "Betty", "Donald", "Helen",
               "Steven", "Sandra", "Paul", "Donna", "Andrew", "Carol"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Wilson",
              "Martinez", "Anderson", "Taylor", "Thomas", "Hernandez", "Moore", "Martin", "Jackson",
              "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
              "Walker", "Young", "Allen", "King", "Wright", "Lopez", "Hill", "Scott", "Green",
              "Adams", "Baker", "Gonzalez", "Nelson", "Carter", "Mitchell"]
designations = frappe.get_all("Designation", limit=20) or [{"name": "Manager"}]
departments = frappe.get_all("Department", limit=10)
if not departments:
    try:
        dept = frappe.new_doc("Department")
        dept.department_name = "General"
        dept.company = company
        dept.insert(ignore_permissions=True)
        departments = [{"name": dept.name}]
    except:
        pass

employees_created = 0
for i in range(40):
    first_name = choice(first_names)
    last_name = choice(last_names)
    employee_name = f"{first_name} {last_name}"
    if frappe.db.exists("Employee", {"employee_name": employee_name}):
        continue
    try:
        employee = frappe.new_doc("Employee")
        employee.first_name = first_name
        employee.last_name = last_name
        employee.employee_name = employee_name
        employee.company = company
        employee.date_of_joining = add_days(nowdate(), -randint(30, 1825))
        employee.designation = choice(designations).name if designations else "Manager"
        employee.department = choice(departments).name if departments else None
        employee.status = choice(["Active", "Active", "Active", "Left"])
        employee.gender = choice(["Male", "Female", "Other"])
        employee.date_of_birth = add_days(nowdate(), -randint(7300, 18250))
        employee.insert(ignore_permissions=True)
        employees_created += 1
    except:
        pass
print(f"    ✅ Created {employees_created} Employees")

# 3.2 More Attendance
print("\n  ⏰ Creating 150 Attendance Records...")
employees_list = frappe.get_all("Employee", limit=50)
attendance_created = 0
for employee in employees_list[:30]:
    for day in range(randint(5, 10)):
        att_date = add_days(nowdate(), -day)
        if not frappe.db.exists("Attendance", {"employee": employee.name, "attendance_date": att_date}):
            try:
                att = frappe.new_doc("Attendance")
                att.employee = employee.name
                att.attendance_date = att_date
                att.status = choice(["Present", "Present", "Present", "Present", "Absent", "Half Day"])
                att.insert(ignore_permissions=True)
                try:
                    att.submit()
                except:
                    pass
                attendance_created += 1
            except:
                pass
print(f"    ✅ Created {attendance_created} Attendance Records")

# 3.3 Leave Applications
print("\n  🏖️  Creating 30 Leave Applications...")
leave_types = frappe.get_all("Leave Type", limit=10)
if not leave_types:
    leave_types = [{"name": "Annual Leave"}]

leave_apps_created = 0
for i in range(30):
    if not employees_list:
        break
    employee = choice(employees_list)
    leave_type = choice(leave_types).name
    try:
        leave_app = frappe.new_doc("Leave Application")
        leave_app.employee = employee.name
        leave_app.leave_type = leave_type
        leave_app.from_date = add_days(nowdate(), randint(-60, 60))
        leave_app.to_date = add_days(leave_app.from_date, randint(1, 7))
        leave_app.half_day = choice([0, 1])
        leave_app.status = choice(["Open", "Approved", "Rejected", "Cancelled"])
        leave_app.insert(ignore_permissions=True)
        if leave_app.status == "Approved":
            try:
                leave_app.submit()
            except:
                pass
        leave_apps_created += 1
    except:
        pass
print(f"    ✅ Created {leave_apps_created} Leave Applications")

print("\n✅ HRMS Module Complete!")

# ============================================================================
# 4. GAMEPLAN MODULE
# ============================================================================
print("\n" + "="*80)
print("🎮 MODULE 4: GAMEPLAN")
print("="*80)

# 4.1 GP Teams
print("\n  👥 Creating 10 GP Teams...")
team_names = [
    "Engineering", "Product", "Design", "Marketing", "Sales",
    "Support", "Operations", "Finance", "HR", "Executive"
]
teams_created = 0
for name in team_names:
    if frappe.db.exists("GP Team", name):
        continue
    try:
        team = frappe.new_doc("GP Team")
        team.title = name
        team.description = f"The {name} team"
        team.insert(ignore_permissions=True)
        teams_created += 1
    except:
        pass
print(f"    ✅ Created {teams_created} GP Teams")

# 4.2 GP Projects
print("\n  📁 Creating 30 GP Projects...")
project_names = [
    "Website Redesign", "Mobile App", "API Development", "Database Migration",
    "Security Audit", "Performance Optimization", "Feature Launch", "Bug Fixes",
    "Documentation", "Testing", "Deployment", "Monitoring Setup",
    "Backup System", "Disaster Recovery", "Compliance Review", "Training Program",
    "Marketing Campaign", "Sales Strategy", "Customer Onboarding", "Product Roadmap",
    "Research Project", "Prototype", "MVP Development", "Beta Testing", "Production Release",
    "Q1 Initiative", "Q2 Project", "Q3 Launch", "Q4 Enhancement", "Annual Review"
]
projects_created = 0
teams = frappe.get_all("GP Team", limit=10)
for name in project_names:
    if frappe.db.exists("GP Project", name):
        continue
    try:
        project = frappe.new_doc("GP Project")
        project.title = name
        project.team = choice(teams).name if teams else None
        project.status = choice(["Planning", "Active", "On Hold", "Completed", "Cancelled"])
        project.start_date = add_days(nowdate(), -randint(0, 60))
        project.end_date = add_days(project.start_date, randint(30, 180))
        project.insert(ignore_permissions=True)
        projects_created += 1
    except:
        pass
print(f"    ✅ Created {projects_created} GP Projects")

# 4.3 GP Tasks
print("\n  ✅ Creating 80 GP Tasks...")
task_titles = [
    "Design login page", "Implement authentication", "Write unit tests", "Fix bug in API",
    "Update documentation", "Review code", "Deploy to staging", "Test feature",
    "Create wireframes", "Design mockups", "Gather requirements", "Plan sprint",
    "Update database", "Optimize queries", "Add logging", "Monitor performance",
    "Fix security issue", "Update dependencies", "Refactor code", "Add comments"
]
tasks_created = 0
projects = frappe.get_all("GP Project", limit=30)
for i in range(80):
    title = f"{choice(task_titles)} {i+1}"
    if frappe.db.exists("GP Task", title):
        continue
    try:
        task = frappe.new_doc("GP Task")
        task.title = title
        task.project = choice(projects).name if projects else None
        task.status = choice(["Backlog", "To Do", "In Progress", "In Review", "Done", "Cancelled"])
        task.priority = choice(["Low", "Medium", "High", "Urgent"])
        task.due_date = add_days(nowdate(), randint(-10, 30))
        task.insert(ignore_permissions=True)
        tasks_created += 1
    except:
        pass
print(f"    ✅ Created {tasks_created} GP Tasks")

# 4.4 GP Discussions
print("\n  💬 Creating 60 GP Discussions...")
discussion_topics = [
    "Project planning", "Technical discussion", "Design review", "Code review",
    "Sprint planning", "Retrospective", "Standup notes", "Architecture decision",
    "Performance issue", "Security concern", "Feature request", "Bug report"
]
discussions_created = 0
for i in range(60):
    topic = f"{choice(discussion_topics)} {i+1}"
    if frappe.db.exists("GP Discussion", topic):
        continue
    try:
        discussion = frappe.new_doc("GP Discussion")
        discussion.title = topic
        discussion.project = choice(projects).name if projects else None
        discussion.team = choice(teams).name if teams else None
        discussion.content = f"Discussion about {topic.lower()}"
        discussion.insert(ignore_permissions=True)
        discussions_created += 1
    except:
        pass
print(f"    ✅ Created {discussions_created} GP Discussions")

# 4.5 GP Pages
print("\n  📄 Creating 40 GP Pages...")
page_titles = [
    "Project Overview", "Requirements", "Architecture", "API Documentation",
    "User Guide", "Developer Guide", "Deployment Guide", "Troubleshooting",
    "FAQ", "Changelog", "Roadmap", "Meeting Notes", "Decisions", "Research"
]
pages_created = 0
for i in range(40):
    title = f"{choice(page_titles)} {i+1}"
    if frappe.db.exists("GP Page", title):
        continue
    try:
        page = frappe.new_doc("GP Page")
        page.title = title
        page.project = choice(projects).name if projects else None
        page.team = choice(teams).name if teams else None
        page.content = f"Content for {title.lower()}"
        page.insert(ignore_permissions=True)
        pages_created += 1
    except:
        pass
print(f"    ✅ Created {pages_created} GP Pages")

# 4.6 GP Comments
print("\n  💭 Creating 100 GP Comments...")
comments_created = 0
discussions_list = frappe.get_all("GP Discussion", limit=60)
tasks_list = frappe.get_all("GP Task", limit=80)
for i in range(100):
    try:
        comment = frappe.new_doc("GP Comment")
        if discussions_list and i % 2 == 0:
            comment.reference_doctype = "GP Discussion"
            comment.reference_name = choice(discussions_list).name
        elif tasks_list:
            comment.reference_doctype = "GP Task"
            comment.reference_name = choice(tasks_list).name
        else:
            continue
        comment.content = f"Comment {i+1}: This is a sample comment for discussion."
        comment.insert(ignore_permissions=True)
        comments_created += 1
    except:
        pass
print(f"    ✅ Created {comments_created} GP Comments")

print("\n✅ Gameplan Module Complete!")

# Commit all changes
frappe.db.commit()

# Print final summary
print("\n" + "="*80)
print("FINAL DEMO DATA SUMMARY - ALL MODULES")
print("="*80)

summary_doctypes = {
    "CRM": ["Lead", "Opportunity"],
    "ERPNext": ["Customer", "Supplier", "Item", "Sales Order", "Purchase Order", "Sales Invoice", "Quotation"],
    "HRMS": ["Employee", "Leave Application", "Attendance"],
    "Gameplan": ["GP Team", "GP Project", "GP Task", "GP Discussion", "GP Page", "GP Comment"]
}

for module, doctypes in summary_doctypes.items():
    print(f"\n{module}:")
    for doctype in doctypes:
        try:
            count = frappe.db.count(doctype)
            print(f"  {doctype:30} : {count}")
        except:
            pass

print("\n" + "="*80)
print("✅ ALL DEMO DATA HAS BEEN SUCCESSFULLY ADDED!")
print("="*80)
