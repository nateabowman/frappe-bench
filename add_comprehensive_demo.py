#!/usr/bin/env python3
"""
Comprehensive demo data script for demo.nexelya.com
Adds extensive demo data across all modules
"""
import frappe
from frappe.utils import add_days, nowdate, flt
from random import randint, choice

frappe.set_user("Administrator")

print("="*70)
print("COMPREHENSIVE DEMO DATA SETUP FOR demo.nexelya.com")
print("="*70)

# Get company
companies = frappe.get_all("Company", limit=1)
if not companies:
    print("❌ No company found!")
    exit(1)

company = companies[0].name
print(f"\n✓ Company: {company}\n")

# 1. ERPNext Demo Data
print("📦 Step 1: Setting up ERPNext demo data...")
try:
    from erpnext.setup.demo import setup_demo_data
    setup_demo_data()
    print("  ✅ ERPNext demo data created\n")
except Exception as e:
    print(f"  ⚠️  {str(e)}\n")

# 2. Additional Customers (30 more)
print("👥 Step 2: Creating 30 additional customers...")
customer_names = [
    "Acme Corporation", "Tech Solutions Inc", "Global Industries", "Prime Services",
    "Elite Enterprises", "Summit Group", "Apex Systems", "Nexus Technologies",
    "Velocity Corp", "Stellar Solutions", "Quantum Industries", "Phoenix Group",
    "Horizon Enterprises", "Catalyst Corp", "Fusion Systems", "Matrix Industries",
    "Zenith Corp", "Titan Group", "Orion Enterprises", "Nova Systems",
    "Premier Solutions", "Advanced Systems", "Core Technologies", "Prime Services",
    "Elite Group", "Summit Corp", "Apex Industries", "Nexus Solutions",
    "Velocity Enterprises", "Stellar Corp"
]
created = 0
for name in customer_names:
    if not frappe.db.exists("Customer", name):
        try:
            c = frappe.new_doc("Customer")
            c.customer_name = name
            c.customer_type = choice(["Company", "Individual"])
            c.territory = choice(["All Territories", "North America", "Europe", "Asia"])
            c.customer_group = "All Customer Groups"
            c.insert(ignore_permissions=True)
            created += 1
        except: pass
print(f"  ✅ Created {created} customers\n")

# 3. Additional Suppliers (20 more)
print("🏭 Step 3: Creating 20 additional suppliers...")
supplier_names = [
    "Best Supplies Co", "Quality Materials Ltd", "Reliable Sources Inc",
    "Premium Goods Corp", "Trusted Vendors", "Superior Products",
    "Excellence Suppliers", "Prime Materials", "Top Quality Co",
    "First Class Supplies", "Elite Vendors", "Master Suppliers",
    "Pro Materials", "Ace Suppliers", "Champion Goods",
    "Premium Supplies", "Quality Materials", "Reliable Sources",
    "Excellence Goods", "Superior Products"
]
created = 0
for name in supplier_names:
    if not frappe.db.exists("Supplier", name):
        try:
            s = frappe.new_doc("Supplier")
            s.supplier_name = name
            s.supplier_group = "All Supplier Groups"
            s.insert(ignore_permissions=True)
            created += 1
        except: pass
print(f"  ✅ Created {created} suppliers\n")

# 4. Additional Items (40 more)
print("📦 Step 4: Creating 40 additional items...")
item_names = [
    "Laptop Computer", "Desktop Computer", "Monitor 24 inch", "Keyboard Wireless",
    "Mouse Optical", "Webcam HD", "Headphones", "USB Drive 32GB",
    "External Hard Drive", "Printer Laser", "Scanner", "Tablet",
    "Smartphone", "Smart Watch", "Bluetooth Speaker", "Router WiFi",
    "Network Switch", "Cable HDMI", "Power Adapter", "Battery Pack",
    "Office Chair", "Desk Stand", "Monitor Arm", "Laptop Stand",
    "Desk Lamp", "File Organizer", "Pen Set", "Notebook",
    "Stapler", "Paper Clips", "Wireless Mouse", "USB-C Cable",
    "Laptop Bag", "Monitor Stand", "Desk Mat", "Keyboard Wrist Rest",
    "Webcam Stand", "Microphone USB", "Speaker Bluetooth", "Headset Gaming"
]
item_groups = frappe.get_all("Item Group", limit=1)
created = 0
if item_groups:
    warehouses = frappe.get_all("Warehouse", filters={"company": company, "is_group": 0}, limit=1)
    for name in item_names:
        if not frappe.db.exists("Item", name):
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
                created += 1
            except: pass
print(f"  ✅ Created {created} items\n")

# 5. CRM Leads (50 leads)
print("📞 Step 5: Creating 50 CRM leads...")
lead_names = [
    "Tech Startup Inc", "Digital Solutions", "Cloud Services Co", "AI Innovations",
    "Data Analytics Ltd", "Software Solutions", "Web Development Co", "Mobile Apps Inc",
    "E-commerce Platform", "SaaS Provider", "IT Consulting", "Network Services",
    "Security Solutions", "DevOps Services", "Cloud Infrastructure", "Big Data Corp",
    "Machine Learning Co", "IoT Solutions", "Blockchain Services", "Fintech Startup",
    "Healthcare Tech", "EdTech Solutions", "Retail Tech", "Manufacturing Tech",
    "Logistics Tech", "Transport Tech", "Energy Solutions", "Green Tech",
    "Media Company", "Entertainment Corp", "Sports Tech", "Fitness App",
    "Food Delivery", "Travel Tech", "Real Estate Tech", "Construction Tech",
    "Agriculture Tech", "Farming Solutions", "Water Management", "Waste Management",
    "Renewable Energy", "Solar Solutions", "Wind Power", "Hydro Energy",
    "Battery Tech", "Electric Vehicles", "Autonomous Systems", "Robotics Corp",
    "3D Printing", "Virtual Reality"
]
created = 0
for i, name in enumerate(lead_names):
    if not frappe.db.exists("Lead", name):
        try:
            lead = frappe.new_doc("Lead")
            lead.lead_name = name
            lead.company_name = name
            lead.email_id = f"contact@{name.lower().replace(' ', '')}.com"
            lead.mobile_no = f"+1{randint(2000000000, 9999999999)}"
            lead.source = choice(["Website", "Email Campaign", "Cold Call", "Referral", "Trade Show", "Social Media"])
            lead.status = choice(["Open", "Contacted", "Nurturing", "Qualified"])
            lead.industry = choice(["Technology", "Manufacturing", "Retail", "Services", "Healthcare", "Finance"])
            lead.insert(ignore_permissions=True)
            created += 1
        except: pass
print(f"  ✅ Created {created} leads\n")

# 6. Opportunities (30 opportunities)
print("💼 Step 6: Creating 30 opportunities...")
leads = frappe.get_all("Lead", limit=30)
created = 0
for i, lead in enumerate(leads):
    opp_name = f"Opportunity from {lead.name}"
    if not frappe.db.exists("Opportunity", opp_name):
        try:
            opp = frappe.new_doc("Opportunity")
            opp.opportunity_from = "Lead"
            opp.party_name = lead.name
            opp.opportunity_type = choice(["Sales", "Maintenance", "Support"])
            opp.status = choice(["Open", "Quotation", "Negotiation", "Converted"])
            opp.expected_closing = add_days(nowdate(), randint(7, 90))
            opp.probability = randint(10, 90)
            opp.opportunity_amount = flt(randint(10000, 200000), 2)
            opp.insert(ignore_permissions=True)
            created += 1
        except: pass
print(f"  ✅ Created {created} opportunities\n")

# 7. Employees (25 employees)
print("👤 Step 7: Creating 25 employees...")
first_names = ["John", "Jane", "Mike", "Sarah", "David", "Emily", "Chris", "Lisa", "Robert", "Maria", "James", "Patricia", "Michael", "Jennifer", "William", "Linda"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Wilson", "Martinez", "Anderson", "Taylor", "Thomas", "Hernandez", "Moore", "Martin"]
designations = ["Manager", "Developer", "Analyst", "Designer", "Engineer", "Consultant", "Specialist", "Director", "Coordinator", "Executive"]
departments = frappe.get_all("Department", limit=5)
if not departments:
    try:
        dept = frappe.new_doc("Department")
        dept.department_name = "General"
        dept.company = company
        dept.insert(ignore_permissions=True)
        departments = [{"name": dept.name}]
    except: pass

created = 0
for i in range(25):
    first_name = choice(first_names)
    last_name = choice(last_names)
    employee_name = f"{first_name} {last_name}"
    if not frappe.db.exists("Employee", {"employee_name": employee_name}):
        try:
            emp = frappe.new_doc("Employee")
            emp.first_name = first_name
            emp.last_name = last_name
            emp.employee_name = employee_name
            emp.company = company
            emp.date_of_joining = add_days(nowdate(), -randint(30, 1095))
            emp.designation = choice(designations)
            emp.department = choice(departments).name if departments else None
            emp.status = "Active"
            emp.gender = choice(["Male", "Female", "Other"])
            emp.insert(ignore_permissions=True)
            created += 1
        except: pass
print(f"  ✅ Created {created} employees\n")

# 8. Additional Sales Orders (20)
print("📋 Step 8: Creating 20 additional sales orders...")
customers = frappe.get_all("Customer", limit=30)
items = frappe.get_all("Item", limit=40)
warehouses = frappe.get_all("Warehouse", filters={"company": company, "is_group": 0}, limit=5)
created = 0
if customers and items and warehouses:
    for i in range(20):
        try:
            so = frappe.new_doc("Sales Order")
            so.company = company
            so.customer = choice(customers).name
            so.transaction_date = add_days(nowdate(), -randint(1, 90))
            so.delivery_date = add_days(so.transaction_date, randint(7, 30))
            for _ in range(randint(1, 4)):
                so.append("items", {
                    "item_code": choice(items).name,
                    "qty": randint(1, 10),
                    "warehouse": choice(warehouses).name,
                    "rate": flt(randint(100, 1000), 2)
                })
            so.insert(ignore_permissions=True)
            if i % 3 == 0:
                so.submit()
            created += 1
        except: pass
print(f"  ✅ Created {created} sales orders\n")

# 9. Additional Sales Invoices (15)
print("💰 Step 9: Creating 15 additional sales invoices...")
created = 0
if customers and items and warehouses:
    for i in range(15):
        try:
            si = frappe.new_doc("Sales Invoice")
            si.company = company
            si.customer = choice(customers).name
            si.posting_date = add_days(nowdate(), -randint(1, 60))
            si.due_date = add_days(si.posting_date, randint(15, 30))
            for _ in range(randint(1, 5)):
                si.append("items", {
                    "item_code": choice(items).name,
                    "qty": randint(1, 10),
                    "warehouse": choice(warehouses).name,
                    "rate": flt(randint(100, 1000), 2)
                })
            si.insert(ignore_permissions=True)
            if i % 2 == 0:
                si.submit()
            created += 1
        except: pass
print(f"  ✅ Created {created} sales invoices\n")

# 10. Contacts and Addresses
print("📧 Step 10: Creating contacts and addresses...")
customers_list = frappe.get_all("Customer", limit=20)
suppliers_list = frappe.get_all("Supplier", limit=15)
first_names = ["John", "Jane", "Mike", "Sarah", "David", "Emily"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones"]

contacts_created = 0
for customer in customers_list[:15]:
    if frappe.db.count("Contact", {"link_doctype": "Customer", "link_name": customer.name}) == 0:
        try:
            contact = frappe.new_doc("Contact")
            contact.first_name = choice(first_names)
            contact.last_name = choice(last_names)
            contact.email_id = f"{contact.first_name.lower()}.{contact.last_name.lower()}@{customer.name.lower().replace(' ', '')}.com"
            contact.append("links", {"link_doctype": "Customer", "link_name": customer.name})
            contact.insert(ignore_permissions=True)
            contacts_created += 1
        except: pass

addresses_created = 0
addresses_data = [
    {"address_line1": "123 Main St", "city": "New York", "state": "NY", "country": "United States"},
    {"address_line1": "456 Oak Ave", "city": "Los Angeles", "state": "CA", "country": "United States"},
    {"address_line1": "789 Pine Rd", "city": "Chicago", "state": "IL", "country": "United States"},
]
for customer in customers_list[:10]:
    if frappe.db.count("Address", {"link_doctype": "Customer", "link_name": customer.name}) == 0:
        try:
            addr_data = choice(addresses_data)
            address = frappe.new_doc("Address")
            address.address_line1 = addr_data["address_line1"]
            address.city = addr_data["city"]
            address.state = addr_data["state"]
            address.country = addr_data["country"]
            address.pincode = str(randint(10000, 99999))
            address.append("links", {"link_doctype": "Customer", "link_name": customer.name})
            address.insert(ignore_permissions=True)
            addresses_created += 1
        except: pass
print(f"  ✅ Created {contacts_created} contacts and {addresses_created} addresses\n")

# 11. Attendance Records
print("⏰ Step 11: Creating attendance records...")
employees_list = frappe.get_all("Employee", limit=10)
attendance_created = 0
for employee in employees_list:
    for day in range(10):
        att_date = add_days(nowdate(), -day)
        if not frappe.db.exists("Attendance", {"employee": employee.name, "attendance_date": att_date}):
            try:
                att = frappe.new_doc("Attendance")
                att.employee = employee.name
                att.attendance_date = att_date
                att.status = choice(["Present", "Present", "Present", "Absent"])
                att.insert(ignore_permissions=True)
                att.submit()
                attendance_created += 1
            except: pass
print(f"  ✅ Created {attendance_created} attendance records\n")

# 12. Insights Demo Data
print("📊 Step 12: Setting up Insights demo data...")
try:
    from insights.setup.demo import DemoDataFactory
    factory = DemoDataFactory.run(force=False)
    print("  ✅ Insights demo data created\n")
except Exception as e:
    print(f"  ⚠️  Insights: {str(e)}\n")

# Commit all changes
frappe.db.commit()

# Print summary
print("="*70)
print("DEMO DATA SUMMARY")
print("="*70)
doctypes = [
    "Customer", "Supplier", "Item", "Contact", "Address",
    "Sales Order", "Purchase Order", "Sales Invoice", "Purchase Invoice",
    "Lead", "Opportunity", "Employee", "Attendance"
]
for doctype in doctypes:
    try:
        count = frappe.db.count(doctype)
        print(f"  {doctype:20} : {count}")
    except: pass
print("="*70)
print("✅ All demo data has been added successfully!")
print("="*70)
