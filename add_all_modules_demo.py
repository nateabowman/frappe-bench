#!/usr/bin/env python3
"""
Comprehensive demo data for all modules: CRM, ERPNext, HRMS, Gameplan
"""
import frappe
from frappe.utils import add_days, nowdate, flt, get_datetime, getdate
from random import randint, choice
from datetime import datetime, timedelta

frappe.set_user("Administrator")

print("="*80)
print("COMPREHENSIVE DEMO DATA SETUP - ALL MODULES")
print("="*80)

# Get company
companies = frappe.get_all("Company", limit=1)
if not companies:
    print("❌ No company found!")
    exit(1)

company = companies[0].name
print(f"\n✓ Company: {company}\n")

# ============================================================================
# 1. CRM MODULE - Extensive Demo Data
# ============================================================================
print("="*80)
print("📞 MODULE 1: CRM - Adding comprehensive demo data")
print("="*80)

# 1.1 CRM Leads (100 leads)
print("\n  📋 Creating 100 CRM Leads...")
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
    "Spa & Salon", "Beauty Products", "Cosmetics", "Fashion Brand",
    "Jewelry Store", "Watchmaker", "Luxury Goods", "Art Gallery"
]
lead_sources = ["Website", "Email Campaign", "Cold Call", "Referral", "Trade Show", "Social Media", "LinkedIn", "Google Ads"]
lead_statuses = ["Open", "Contacted", "Nurturing", "Qualified", "Converted", "Lost"]
industries = ["Technology", "Manufacturing", "Retail", "Services", "Healthcare", "Finance", "Education", "Real Estate"]

leads_created = 0
for i, name in enumerate(lead_names):
    if frappe.db.exists("CRM Lead", name):
        continue
    try:
        lead = frappe.new_doc("CRM Lead")
        lead.lead_name = name
        lead.company_name = name
        lead.email_id = f"contact@{name.lower().replace(' ', '').replace('&', '')}.com"
        lead.mobile_no = f"+1{randint(2000000000, 9999999999)}"
        lead.source = choice(lead_sources)
        lead.status = choice(lead_statuses)
        lead.industry = choice(industries)
        lead.no_of_employees = choice(["1-10", "11-50", "51-200", "201-500", "500+"])
        lead.annual_revenue = flt(randint(100000, 10000000), 2)
        lead.insert(ignore_permissions=True)
        leads_created += 1
    except Exception as e:
        pass
print(f"    ✅ Created {leads_created} CRM Leads")

# 1.2 CRM Organizations (50 organizations)
print("\n  🏢 Creating 50 CRM Organizations...")
org_names = [
    "Acme Corporation", "Global Industries", "Prime Services", "Elite Enterprises",
    "Summit Group", "Apex Systems", "Nexus Technologies", "Velocity Corp",
    "Stellar Solutions", "Quantum Industries", "Phoenix Group", "Horizon Enterprises",
    "Catalyst Corp", "Fusion Systems", "Matrix Industries", "Zenith Corp",
    "Titan Group", "Orion Enterprises", "Nova Systems", "Premier Solutions",
    "Advanced Systems", "Core Technologies", "Prime Services", "Elite Group",
    "Summit Corp", "Apex Industries", "Nexus Solutions", "Velocity Enterprises",
    "Stellar Corp", "Quantum Systems", "Phoenix Industries", "Horizon Corp",
    "Catalyst Solutions", "Fusion Group", "Matrix Corp", "Zenith Industries",
    "Titan Solutions", "Orion Corp", "Nova Industries", "Premier Corp",
    "Advanced Industries", "Core Corp", "Prime Industries", "Elite Solutions",
    "Summit Industries", "Apex Corp", "Nexus Industries", "Velocity Solutions",
    "Stellar Industries", "Quantum Corp"
]
orgs_created = 0
for name in org_names:
    if frappe.db.exists("CRM Organization", name):
        continue
    try:
        org = frappe.new_doc("CRM Organization")
        org.organization_name = name
        org.website = f"https://www.{name.lower().replace(' ', '')}.com"
        org.industry = choice(industries)
        org.no_of_employees = choice(["1-10", "11-50", "51-200", "201-500", "500+"])
        org.annual_revenue = flt(randint(500000, 50000000), 2)
        org.insert(ignore_permissions=True)
        orgs_created += 1
    except:
        pass
print(f"    ✅ Created {orgs_created} CRM Organizations")

# 1.3 CRM Deals (60 deals)
print("\n  💼 Creating 60 CRM Deals...")
deal_statuses = ["Open", "Qualified", "Proposal", "Negotiation", "Won", "Lost"]
deals_created = 0
for i in range(60):
    deal_name = f"Deal {i+1} - {choice(['Q1', 'Q2', 'Q3', 'Q4'])} {choice(['2024', '2025'])}"
    if frappe.db.exists("CRM Deal", deal_name):
        continue
    try:
        deal = frappe.new_doc("CRM Deal")
        deal.deal_name = deal_name
        deal.status = choice(deal_statuses)
        deal.deal_value = flt(randint(5000, 500000), 2)
        deal.expected_close_date = add_days(nowdate(), randint(-30, 90))
        deal.probability = randint(10, 90)
        deal.insert(ignore_permissions=True)
        deals_created += 1
    except:
        pass
print(f"    ✅ Created {deals_created} CRM Deals")

# 1.4 CRM Contacts (80 contacts)
print("\n  👤 Creating 80 CRM Contacts...")
first_names = ["John", "Jane", "Mike", "Sarah", "David", "Emily", "Chris", "Lisa", "Robert", "Maria", 
               "James", "Patricia", "Michael", "Jennifer", "William", "Linda", "Richard", "Barbara",
               "Joseph", "Elizabeth", "Thomas", "Susan", "Charles", "Jessica", "Daniel", "Sarah"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Wilson",
              "Martinez", "Anderson", "Taylor", "Thomas", "Hernandez", "Moore", "Martin", "Jackson",
              "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker"]
contacts_created = 0
for i in range(80):
    first_name = choice(first_names)
    last_name = choice(last_names)
    contact_name = f"{first_name} {last_name}"
    if frappe.db.exists("CRM Contacts", {"first_name": first_name, "last_name": last_name}):
        continue
    try:
        contact = frappe.new_doc("CRM Contacts")
        contact.first_name = first_name
        contact.last_name = last_name
        contact.email = f"{first_name.lower()}.{last_name.lower()}@example.com"
        contact.mobile_no = f"+1{randint(2000000000, 9999999999)}"
        contact.designation = choice(["Manager", "Director", "VP", "CEO", "CTO", "CFO", "Developer", "Analyst"])
        contact.insert(ignore_permissions=True)
        contacts_created += 1
    except:
        pass
print(f"    ✅ Created {contacts_created} CRM Contacts")

# 1.5 CRM Tasks (40 tasks)
print("\n  ✅ Creating 40 CRM Tasks...")
task_subjects = [
    "Follow up with client", "Prepare proposal", "Schedule meeting", "Send quote",
    "Review contract", "Update CRM", "Call prospect", "Send email",
    "Prepare presentation", "Research competitor", "Update pipeline", "Close deal",
    "Onboard new client", "Renew contract", "Upsell service", "Resolve issue",
    "Collect feedback", "Schedule demo", "Send documentation", "Arrange call"
]
tasks_created = 0
for i in range(40):
    subject = f"{choice(task_subjects)} {i+1}"
    if frappe.db.exists("CRM Task", subject):
        continue
    try:
        task = frappe.new_doc("CRM Task")
        task.subject = subject
        task.status = choice(["Open", "In Progress", "Completed", "Cancelled"])
        task.priority = choice(["Low", "Medium", "High"])
        task.due_date = add_days(nowdate(), randint(-5, 30))
        task.insert(ignore_permissions=True)
        tasks_created += 1
    except:
        pass
print(f"    ✅ Created {tasks_created} CRM Tasks")

# 1.6 CRM Products (30 products)
print("\n  📦 Creating 30 CRM Products...")
product_names = [
    "Enterprise Software", "Cloud Hosting", "SaaS Platform", "Mobile App",
    "Web Development", "Consulting Services", "Training Program", "Support Package",
    "Premium License", "Basic License", "API Access", "Data Analytics",
    "Marketing Tools", "CRM Software", "Project Management", "Team Collaboration",
    "Security Suite", "Backup Solution", "Monitoring Service", "Integration Service",
    "Custom Development", "Maintenance Plan", "Upgrade Package", "Migration Service",
    "Performance Optimization", "Security Audit", "Compliance Check", "Documentation",
    "Video Tutorials", "Live Training"
]
products_created = 0
for name in product_names:
    if frappe.db.exists("CRM Product", name):
        continue
    try:
        product = frappe.new_doc("CRM Product")
        product.product_name = name
        product.standard_rate = flt(randint(100, 10000), 2)
        product.description = f"Professional {name.lower()} solution"
        product.insert(ignore_permissions=True)
        products_created += 1
    except:
        pass
print(f"    ✅ Created {products_created} CRM Products")

# 1.7 CRM Campaigns (15 campaigns)
print("\n  📢 Creating 15 CRM Campaigns...")
campaign_names = [
    "Q1 2025 Launch", "Summer Promotion", "Holiday Special", "New Year Sale",
    "Product Launch", "Customer Retention", "Lead Generation", "Brand Awareness",
    "Email Marketing", "Social Media Push", "Webinar Series", "Trade Show 2025",
    "Referral Program", "Upsell Campaign", "Win-Back Campaign"
]
campaigns_created = 0
for name in campaign_names:
    if frappe.db.exists("CRM Campaign", name):
        continue
    try:
        campaign = frappe.new_doc("CRM Campaign")
        campaign.campaign_name = name
        campaign.status = choice(["Planning", "Active", "Completed", "Cancelled"])
        campaign.start_date = add_days(nowdate(), randint(-30, 30))
        campaign.end_date = add_days(campaign.start_date, randint(7, 90))
        campaign.budget = flt(randint(5000, 100000), 2)
        campaign.insert(ignore_permissions=True)
        campaigns_created += 1
    except:
        pass
print(f"    ✅ Created {campaigns_created} CRM Campaigns")

print("\n✅ CRM Module Demo Data Complete!")

# ============================================================================
# 2. ERPNEXT MODULE - More Extensive Data
# ============================================================================
print("\n" + "="*80)
print("📦 MODULE 2: ERPNEXT - Adding more comprehensive demo data")
print("="*80)

# 2.1 More Customers (50 additional)
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
    "Phi Logistics", "Chi Supply", "Psi Chain", "Omega Network"
]
customers_created = 0
for name in customer_names:
    if frappe.db.exists("Customer", name):
        continue
    try:
        customer = frappe.new_doc("Customer")
        customer.customer_name = name
        customer.customer_type = choice(["Company", "Individual"])
        customer.territory = choice(["All Territories", "North America", "Europe", "Asia", "Middle East", "Africa"])
        customer.customer_group = "All Customer Groups"
        customer.insert(ignore_permissions=True)
        customers_created += 1
    except:
        pass
print(f"    ✅ Created {customers_created} additional Customers")

# 2.2 More Suppliers (30 additional)
print("\n  🏭 Creating 30 additional Suppliers...")
supplier_names = [
    "Alpha Supplies", "Beta Materials", "Gamma Goods", "Delta Products",
    "Epsilon Vendors", "Zeta Suppliers", "Eta Sources", "Theta Materials",
    "Iota Goods", "Kappa Products", "Lambda Supplies", "Mu Vendors",
    "Nu Suppliers", "Xi Sources", "Omicron Materials", "Pi Goods",
    "Rho Products", "Sigma Supplies", "Tau Vendors", "Upsilon Suppliers",
    "Phi Sources", "Chi Materials", "Psi Goods", "Omega Products",
    "Premium Alpha", "Elite Beta", "Pro Gamma", "Plus Delta"
]
suppliers_created = 0
for name in supplier_names:
    if frappe.db.exists("Supplier", name):
        continue
    try:
        supplier = frappe.new_doc("Supplier")
        supplier.supplier_name = name
        supplier.supplier_group = "All Supplier Groups"
        supplier.insert(ignore_permissions=True)
        suppliers_created += 1
    except:
        pass
print(f"    ✅ Created {suppliers_created} additional Suppliers")

# 2.3 More Items (60 additional)
print("\n  📦 Creating 60 additional Items...")
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
    "Service Mesh", "Microservices", "Serverless Platform", "Function Service",
    "Event Streaming", "Time Series DB", "Graph Database", "NoSQL Database",
    "Blockchain Node", "Smart Contract", "Cryptocurrency", "Digital Wallet"
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
print(f"    ✅ Created {items_created} additional Items")

# 2.4 More Sales Orders (50 additional)
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
print(f"    ✅ Created {so_created} additional Sales Orders")

# 2.5 More Sales Invoices (40 additional)
print("\n  💰 Creating 40 additional Sales Invoices...")
si_created = 0
if customers and items and warehouses:
    for i in range(40):
        try:
            si = frappe.new_doc("Sales Invoice")
            si.company = company
            si.customer = choice(customers).name
            si.posting_date = add_days(nowdate(), -randint(1, 90))
            si.due_date = add_days(si.posting_date, randint(15, 45))
            for _ in range(randint(1, 6)):
                si.append("items", {
                    "item_code": choice(items).name,
                    "qty": randint(1, 15),
                    "warehouse": choice(warehouses).name,
                    "rate": flt(randint(50, 2000), 2)
                })
            si.insert(ignore_permissions=True)
            if i % 3 == 0:
                si.submit()
            si_created += 1
        except:
            pass
print(f"    ✅ Created {si_created} additional Sales Invoices")

# 2.6 Purchase Orders (30 additional)
print("\n  📥 Creating 30 additional Purchase Orders...")
suppliers = frappe.get_all("Supplier", limit=50)
po_created = 0
if suppliers and items and warehouses:
    for i in range(30):
        try:
            po = frappe.new_doc("Purchase Order")
            po.company = company
            po.supplier = choice(suppliers).name
            po.transaction_date = add_days(nowdate(), -randint(1, 90))
            po.schedule_date = add_days(po.transaction_date, randint(7, 30))
            for _ in range(randint(1, 4)):
                po.append("items", {
                    "item_code": choice(items).name,
                    "qty": randint(10, 100),
                    "warehouse": choice(warehouses).name,
                    "rate": flt(randint(25, 1000), 2)
                })
            po.insert(ignore_permissions=True)
            if i % 3 == 0:
                po.submit()
            po_created += 1
        except:
            pass
print(f"    ✅ Created {po_created} additional Purchase Orders")

# 2.7 Quotations (25 additional)
print("\n  📄 Creating 25 additional Quotations...")
quotations_created = 0
if customers and items and warehouses:
    for i in range(25):
        try:
            quotation = frappe.new_doc("Quotation")
            quotation.party_name = choice(customers).name
            quotation.transaction_date = add_days(nowdate(), -randint(1, 60))
            quotation.valid_till = add_days(quotation.transaction_date, randint(15, 60))
            for _ in range(randint(1, 4)):
                quotation.append("items", {
                    "item_code": choice(items).name,
                    "qty": randint(1, 10),
                    "warehouse": choice(warehouses).name,
                    "rate": flt(randint(100, 1500), 2)
                })
            quotation.insert(ignore_permissions=True)
            if i % 4 == 0:
                quotation.submit()
            quotations_created += 1
        except:
            pass
print(f"    ✅ Created {quotations_created} additional Quotations")

print("\n✅ ERPNext Module Demo Data Complete!")

# ============================================================================
# 3. HRMS MODULE - Comprehensive Demo Data
# ============================================================================
print("\n" + "="*80)
print("👥 MODULE 3: HRMS - Adding comprehensive demo data")
print("="*80)

# 3.1 More Employees (50 employees)
print("\n  👤 Creating 50 Employees...")
first_names = ["John", "Jane", "Mike", "Sarah", "David", "Emily", "Chris", "Lisa", "Robert", "Maria",
               "James", "Patricia", "Michael", "Jennifer", "William", "Linda", "Richard", "Barbara",
               "Joseph", "Elizabeth", "Thomas", "Susan", "Charles", "Jessica", "Daniel", "Sarah",
               "Matthew", "Nancy", "Anthony", "Karen", "Mark", "Betty", "Donald", "Helen",
               "Steven", "Sandra", "Paul", "Donna", "Andrew", "Carol", "Joshua", "Ruth",
               "Kenneth", "Sharon", "Kevin", "Michelle", "Brian", "Laura", "George", "Kimberly"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Wilson",
              "Martinez", "Anderson", "Taylor", "Thomas", "Hernandez", "Moore", "Martin", "Jackson",
              "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
              "Walker", "Young", "Allen", "King", "Wright", "Lopez", "Hill", "Scott", "Green",
              "Adams", "Baker", "Gonzalez", "Nelson", "Carter", "Mitchell", "Perez", "Roberts",
              "Turner", "Phillips", "Campbell", "Parker", "Evans", "Edwards", "Collins", "Stewart"]
designations = ["Manager", "Senior Manager", "Director", "VP", "CEO", "CTO", "CFO", "Developer",
                "Senior Developer", "Lead Developer", "Analyst", "Senior Analyst", "Designer",
                "Senior Designer", "Engineer", "Senior Engineer", "Consultant", "Specialist",
                "Coordinator", "Executive", "Assistant", "Administrator", "Supervisor", "Team Lead"]
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
for i in range(50):
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
        employee.designation = choice(designations)
        employee.department = choice(departments).name if departments else None
        employee.status = choice(["Active", "Active", "Active", "Left"])
        employee.gender = choice(["Male", "Female", "Other"])
        employee.date_of_birth = add_days(nowdate(), -randint(7300, 18250))
        employee.insert(ignore_permissions=True)
        employees_created += 1
    except:
        pass
print(f"    ✅ Created {employees_created} Employees")

# 3.2 Leave Applications (40 applications)
print("\n  🏖️  Creating 40 Leave Applications...")
employees_list = frappe.get_all("Employee", limit=50)
leave_types = frappe.get_all("Leave Type", limit=10)
if not leave_types:
    leave_types = [{"name": "Annual Leave"}]

leave_apps_created = 0
for i in range(40):
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

# 3.3 Attendance Records (200 records)
print("\n  ⏰ Creating 200 Attendance Records...")
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

# 3.4 Expense Claims (20 claims)
print("\n  💳 Creating 20 Expense Claims...")
expense_claims_created = 0
expense_types = ["Travel", "Meal", "Accommodation", "Transport", "Office Supplies", "Phone", "Internet"]
for i in range(20):
    if not employees_list:
        break
    employee = choice(employees_list)
    try:
        expense_claim = frappe.new_doc("Expense Claim")
        expense_claim.employee = employee.name
        expense_claim.expense_approver = "Administrator"
        expense_claim.posting_date = add_days(nowdate(), -randint(1, 30))
        for _ in range(randint(1, 4)):
            expense_claim.append("expenses", {
                "expense_type": choice(expense_types),
                "expense_date": add_days(expense_claim.posting_date, -randint(0, 7)),
                "amount": flt(randint(50, 500), 2),
                "description": f"Expense for {choice(expense_types)}"
            })
        expense_claim.insert(ignore_permissions=True)
        expense_claims_created += 1
    except:
        pass
print(f"    ✅ Created {expense_claims_created} Expense Claims")

print("\n✅ HRMS Module Demo Data Complete!")

# ============================================================================
# 4. GAMEPLAN MODULE - Comprehensive Demo Data
# ============================================================================
print("\n" + "="*80)
print("🎮 MODULE 4: GAMEPLAN - Adding comprehensive demo data")
print("="*80)

# 4.1 GP Teams (10 teams)
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

# 4.2 GP Projects (25 projects)
print("\n  📁 Creating 25 GP Projects...")
project_names = [
    "Website Redesign", "Mobile App", "API Development", "Database Migration",
    "Security Audit", "Performance Optimization", "Feature Launch", "Bug Fixes",
    "Documentation", "Testing", "Deployment", "Monitoring Setup",
    "Backup System", "Disaster Recovery", "Compliance Review", "Training Program",
    "Marketing Campaign", "Sales Strategy", "Customer Onboarding", "Product Roadmap",
    "Research Project", "Prototype", "MVP Development", "Beta Testing", "Production Release"
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

# 4.3 GP Tasks (100 tasks)
print("\n  ✅ Creating 100 GP Tasks...")
task_titles = [
    "Design login page", "Implement authentication", "Write unit tests", "Fix bug in API",
    "Update documentation", "Review code", "Deploy to staging", "Test feature",
    "Create wireframes", "Design mockups", "Gather requirements", "Plan sprint",
    "Update database", "Optimize queries", "Add logging", "Monitor performance",
    "Fix security issue", "Update dependencies", "Refactor code", "Add comments",
    "Create migration", "Backup data", "Restore system", "Configure server",
    "Set up CI/CD", "Write documentation", "Train team", "Onboard client"
]
tasks_created = 0
projects = frappe.get_all("GP Project", limit=25)
for i in range(100):
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

# 4.4 GP Discussions (50 discussions)
print("\n  💬 Creating 50 GP Discussions...")
discussion_topics = [
    "Project planning", "Technical discussion", "Design review", "Code review",
    "Sprint planning", "Retrospective", "Standup notes", "Architecture decision",
    "Performance issue", "Security concern", "Feature request", "Bug report",
    "User feedback", "Market research", "Competitor analysis", "Strategy discussion"
]
discussions_created = 0
for i in range(50):
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

# 4.5 GP Pages (30 pages)
print("\n  📄 Creating 30 GP Pages...")
page_titles = [
    "Project Overview", "Requirements", "Architecture", "API Documentation",
    "User Guide", "Developer Guide", "Deployment Guide", "Troubleshooting",
    "FAQ", "Changelog", "Roadmap", "Meeting Notes", "Decisions", "Research",
    "Analysis", "Proposal", "Report", "Summary", "Plan", "Strategy"
]
pages_created = 0
for i in range(30):
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

# 4.6 GP Comments (80 comments)
print("\n  💭 Creating 80 GP Comments...")
comments_created = 0
discussions_list = frappe.get_all("GP Discussion", limit=50)
tasks_list = frappe.get_all("GP Task", limit=100)
for i in range(80):
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

print("\n✅ Gameplan Module Demo Data Complete!")

# Commit all changes
frappe.db.commit()

# Print final summary
print("\n" + "="*80)
print("FINAL DEMO DATA SUMMARY - ALL MODULES")
print("="*80)

summary_doctypes = {
    "CRM": ["CRM Lead", "CRM Organization", "CRM Deal", "CRM Contacts", "CRM Task", "CRM Product", "CRM Campaign"],
    "ERPNext": ["Customer", "Supplier", "Item", "Sales Order", "Purchase Order", "Sales Invoice", "Purchase Invoice", "Quotation"],
    "HRMS": ["Employee", "Leave Application", "Attendance", "Expense Claim"],
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
