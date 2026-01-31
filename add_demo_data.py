#!/usr/bin/env python3
"""
Comprehensive Demo Data Script for demo.nexelya.com
Adds demo data for ERPNext, CRM, HRMS, and other apps
"""

import frappe
from frappe.utils import add_days, getdate, nowdate, random_string, flt
from random import randint, choice
import json

def setup_comprehensive_demo_data():
	"""Add comprehensive demo data to the site"""
	frappe.set_user("Administrator")
	
	print("Starting comprehensive demo data setup...")
	
	# Check if company exists
	companies = frappe.get_all("Company", limit=1)
	if not companies:
		print("No company found. Please set up a company first.")
		return
	
	company = companies[0].name
	print(f"Using company: {company}")
	
	# Setup demo data for different modules
	setup_erpnext_demo_data(company)
	setup_crm_demo_data()
	setup_hrms_demo_data(company)
	setup_insights_demo_data()
	
	print("\n✅ Demo data setup completed!")
	print_summary()

def setup_erpnext_demo_data(company):
	"""Setup ERPNext demo data"""
	print("\n📦 Setting up ERPNext demo data...")
	
	# Customers
	print("  Creating customers...")
	customers = create_customers(20)
	
	# Suppliers
	print("  Creating suppliers...")
	suppliers = create_suppliers(15)
	
	# Items
	print("  Creating items...")
	items = create_items(30, company)
	
	# Contacts
	print("  Creating contacts...")
	create_contacts_for_parties(customers, suppliers)
	
	# Addresses
	print("  Creating addresses...")
	create_addresses_for_parties(customers, suppliers)
	
	# Sales Orders
	print("  Creating sales orders...")
	create_sales_orders(15, company, customers, items)
	
	# Purchase Orders
	print("  Creating purchase orders...")
	create_purchase_orders(10, company, suppliers, items)
	
	# Sales Invoices
	print("  Creating sales invoices...")
	create_sales_invoices(12, company, customers, items)
	
	# Purchase Invoices
	print("  Creating purchase invoices...")
	create_purchase_invoices(8, company, suppliers, items)
	
	# Quotations
	print("  Creating quotations...")
	create_quotations(10, company, customers, items)
	
	print("  ✅ ERPNext demo data created")

def setup_crm_demo_data():
	"""Setup CRM demo data"""
	print("\n📞 Setting up CRM demo data...")
	
	# Leads
	print("  Creating leads...")
	leads = create_leads(25)
	
	# Opportunities
	print("  Creating opportunities...")
	create_opportunities(15, leads)
	
	# Deals
	print("  Creating deals...")
	create_deals(10)
	
	print("  ✅ CRM demo data created")

def setup_hrms_demo_data(company):
	"""Setup HRMS demo data"""
	print("\n👥 Setting up HRMS demo data...")
	
	# Employees
	print("  Creating employees...")
	employees = create_employees(12, company)
	
	# Leave Applications
	print("  Creating leave applications...")
	create_leave_applications(8, employees)
	
	# Attendance
	print("  Creating attendance records...")
	create_attendance_records(50, employees)
	
	print("  ✅ HRMS demo data created")

def setup_insights_demo_data():
	"""Setup Insights demo data"""
	print("\n📊 Setting up Insights demo data...")
	try:
		from insights.setup.demo import DemoDataFactory
		factory = DemoDataFactory.run(force=False)
		print("  ✅ Insights demo data created")
	except Exception as e:
		print(f"  ⚠️  Insights demo data setup skipped: {str(e)}")

# ERPNext Functions

def create_customers(count):
	"""Create demo customers"""
	customers = []
	customer_names = [
		"Acme Corporation", "Tech Solutions Inc", "Global Industries", "Prime Services",
		"Elite Enterprises", "Summit Group", "Apex Systems", "Nexus Technologies",
		"Velocity Corp", "Stellar Solutions", "Quantum Industries", "Phoenix Group",
		"Horizon Enterprises", "Catalyst Corp", "Fusion Systems", "Matrix Industries",
		"Zenith Corp", "Titan Group", "Orion Enterprises", "Nova Systems"
	]
	
	for i in range(count):
		name = customer_names[i % len(customer_names)]
		if frappe.db.exists("Customer", name):
			customers.append(name)
			continue
			
		customer = frappe.new_doc("Customer")
		customer.customer_name = name
		customer.customer_type = choice(["Company", "Individual"])
		customer.territory = choice(["All Territories", "North America", "Europe", "Asia"])
		customer.customer_group = "All Customer Groups"
		customer.insert(ignore_permissions=True)
		customers.append(customer.name)
	
	return customers

def create_suppliers(count):
	"""Create demo suppliers"""
	suppliers = []
	supplier_names = [
		"Best Supplies Co", "Quality Materials Ltd", "Reliable Sources Inc",
		"Premium Goods Corp", "Trusted Vendors", "Superior Products",
		"Excellence Suppliers", "Prime Materials", "Top Quality Co",
		"First Class Supplies", "Elite Vendors", "Master Suppliers",
		"Pro Materials", "Ace Suppliers", "Champion Goods"
	]
	
	for i in range(count):
		name = supplier_names[i % len(supplier_names)]
		if frappe.db.exists("Supplier", name):
			suppliers.append(name)
			continue
			
		supplier = frappe.new_doc("Supplier")
		supplier.supplier_name = name
		supplier.supplier_group = "All Supplier Groups"
		supplier.insert(ignore_permissions=True)
		suppliers.append(supplier.name)
	
	return suppliers

def create_items(count, company):
	"""Create demo items"""
	items = []
	item_names = [
		"Laptop Computer", "Desktop Computer", "Monitor 24 inch", "Keyboard Wireless",
		"Mouse Optical", "Webcam HD", "Headphones", "USB Drive 32GB",
		"External Hard Drive", "Printer Laser", "Scanner", "Tablet",
		"Smartphone", "Smart Watch", "Bluetooth Speaker", "Router WiFi",
		"Network Switch", "Cable HDMI", "Power Adapter", "Battery Pack",
		"Office Chair", "Desk Stand", "Monitor Arm", "Laptop Stand",
		"Desk Lamp", "File Organizer", "Pen Set", "Notebook",
		"Stapler", "Paper Clips"
	]
	
	item_groups = frappe.get_all("Item Group", limit=5)
	if not item_groups:
		# Create default item group
		item_group = frappe.new_doc("Item Group")
		item_group.item_group_name = "Products"
		item_group.parent_item_group = "All Item Groups"
		item_group.insert(ignore_permissions=True)
		item_groups = [{"name": item_group.name}]
	
	for i in range(count):
		name = item_names[i % len(item_names)]
		if frappe.db.exists("Item", name):
			items.append(name)
			continue
			
		item = frappe.new_doc("Item")
		item.item_code = name
		item.item_name = name
		item.item_group = item_groups[0].name
		item.stock_uom = "Nos"
		item.is_stock_item = 1
		item.include_item_in_manufacturing = 0
		
		# Add default warehouse
		warehouses = frappe.get_all("Warehouse", filters={"company": company, "is_group": 0}, limit=1)
		if warehouses:
			item.append("item_defaults", {
				"company": company,
				"default_warehouse": warehouses[0].name
			})
		
		item.insert(ignore_permissions=True)
		items.append(item.name)
	
	return items

def create_contacts_for_parties(customers, suppliers):
	"""Create contacts for customers and suppliers"""
	first_names = ["John", "Jane", "Mike", "Sarah", "David", "Emily", "Chris", "Lisa"]
	last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]
	
	# Customer contacts
	for customer in customers[:10]:
		if frappe.db.count("Contact", {"link_doctype": "Customer", "link_name": customer}) > 0:
			continue
			
		contact = frappe.new_doc("Contact")
		contact.first_name = choice(first_names)
		contact.last_name = choice(last_names)
		contact.email_id = f"{contact.first_name.lower()}.{contact.last_name.lower()}@{customer.lower().replace(' ', '')}.com"
		contact.append("links", {
			"link_doctype": "Customer",
			"link_name": customer
		})
		contact.insert(ignore_permissions=True)
	
	# Supplier contacts
	for supplier in suppliers[:8]:
		if frappe.db.count("Contact", {"link_doctype": "Supplier", "link_name": supplier}) > 0:
			continue
			
		contact = frappe.new_doc("Contact")
		contact.first_name = choice(first_names)
		contact.last_name = choice(last_names)
		contact.email_id = f"{contact.first_name.lower()}.{contact.last_name.lower()}@{supplier.lower().replace(' ', '')}.com"
		contact.append("links", {
			"link_doctype": "Supplier",
			"link_name": supplier
		})
		contact.insert(ignore_permissions=True)

def create_addresses_for_parties(customers, suppliers):
	"""Create addresses for customers and suppliers"""
	addresses_data = [
		{"address_line1": "123 Main St", "city": "New York", "state": "NY", "country": "United States"},
		{"address_line1": "456 Oak Ave", "city": "Los Angeles", "state": "CA", "country": "United States"},
		{"address_line1": "789 Pine Rd", "city": "Chicago", "state": "IL", "country": "United States"},
		{"address_line1": "321 Elm St", "city": "Houston", "state": "TX", "country": "United States"},
	]
	
	# Customer addresses
	for customer in customers[:8]:
		if frappe.db.count("Address", {"link_doctype": "Customer", "link_name": customer}) > 0:
			continue
			
		addr_data = choice(addresses_data)
		address = frappe.new_doc("Address")
		address.address_line1 = addr_data["address_line1"]
		address.city = addr_data["city"]
		address.state = addr_data["state"]
		address.country = addr_data["country"]
		address.pincode = str(randint(10000, 99999))
		address.append("links", {
			"link_doctype": "Customer",
			"link_name": customer
		})
		address.insert(ignore_permissions=True)
	
	# Supplier addresses
	for supplier in suppliers[:6]:
		if frappe.db.count("Address", {"link_doctype": "Supplier", "link_name": supplier}) > 0:
			continue
			
		addr_data = choice(addresses_data)
		address = frappe.new_doc("Address")
		address.address_line1 = addr_data["address_line1"]
		address.city = addr_data["city"]
		address.state = addr_data["state"]
		address.country = addr_data["country"]
		address.pincode = str(randint(10000, 99999))
		address.append("links", {
			"link_doctype": "Supplier",
			"link_name": supplier
		})
		address.insert(ignore_permissions=True)

def create_sales_orders(count, company, customers, items):
	"""Create sales orders"""
	warehouses = frappe.get_all("Warehouse", filters={"company": company, "is_group": 0}, limit=5)
	if not warehouses:
		return
	
	for i in range(count):
		so = frappe.new_doc("Sales Order")
		so.company = company
		so.customer = choice(customers)
		so.transaction_date = add_days(nowdate(), -randint(1, 90))
		so.delivery_date = add_days(so.transaction_date, randint(7, 30))
		
		# Add items
		for _ in range(randint(1, 4)):
			so.append("items", {
				"item_code": choice(items),
				"qty": randint(1, 10),
				"warehouse": choice(warehouses).name,
				"rate": flt(randint(100, 1000), 2)
			})
		
		try:
			so.insert(ignore_permissions=True)
			if i % 3 == 0:  # Submit some orders
				so.submit()
		except Exception as e:
			print(f"    Warning: Could not create sales order: {str(e)}")

def create_purchase_orders(count, company, suppliers, items):
	"""Create purchase orders"""
	warehouses = frappe.get_all("Warehouse", filters={"company": company, "is_group": 0}, limit=5)
	if not warehouses:
		return
	
	for i in range(count):
		po = frappe.new_doc("Purchase Order")
		po.company = company
		po.supplier = choice(suppliers)
		po.transaction_date = add_days(nowdate(), -randint(1, 60))
		po.schedule_date = add_days(po.transaction_date, randint(7, 21))
		
		# Add items
		for _ in range(randint(1, 3)):
			po.append("items", {
				"item_code": choice(items),
				"qty": randint(5, 50),
				"warehouse": choice(warehouses).name,
				"rate": flt(randint(50, 500), 2)
			})
		
		try:
			po.insert(ignore_permissions=True)
			if i % 2 == 0:  # Submit some orders
				po.submit()
		except Exception as e:
			print(f"    Warning: Could not create purchase order: {str(e)}")

def create_sales_invoices(count, company, customers, items):
	"""Create sales invoices"""
	warehouses = frappe.get_all("Warehouse", filters={"company": company, "is_group": 0}, limit=5)
	if not warehouses:
		return
	
	for i in range(count):
		si = frappe.new_doc("Sales Invoice")
		si.company = company
		si.customer = choice(customers)
		si.posting_date = add_days(nowdate(), -randint(1, 60))
		si.due_date = add_days(si.posting_date, randint(15, 30))
		
		# Add items
		for _ in range(randint(1, 5)):
			si.append("items", {
				"item_code": choice(items),
				"qty": randint(1, 10),
				"warehouse": choice(warehouses).name,
				"rate": flt(randint(100, 1000), 2)
			})
		
		try:
			si.insert(ignore_permissions=True)
			if i % 2 == 0:  # Submit some invoices
				si.submit()
		except Exception as e:
			print(f"    Warning: Could not create sales invoice: {str(e)}")

def create_purchase_invoices(count, company, suppliers, items):
	"""Create purchase invoices"""
	warehouses = frappe.get_all("Warehouse", filters={"company": company, "is_group": 0}, limit=5)
	if not warehouses:
		return
	
	for i in range(count):
		pi = frappe.new_doc("Purchase Invoice")
		pi.company = company
		pi.supplier = choice(suppliers)
		pi.posting_date = add_days(nowdate(), -randint(1, 45))
		pi.due_date = add_days(pi.posting_date, randint(15, 30))
		pi.bill_date = pi.posting_date
		
		# Add items
		for _ in range(randint(1, 4)):
			pi.append("items", {
				"item_code": choice(items),
				"qty": randint(5, 50),
				"warehouse": choice(warehouses).name,
				"rate": flt(randint(50, 500), 2)
			})
		
		try:
			pi.insert(ignore_permissions=True)
			if i % 2 == 0:  # Submit some invoices
				pi.submit()
		except Exception as e:
			print(f"    Warning: Could not create purchase invoice: {str(e)}")

def create_quotations(count, company, customers, items):
	"""Create quotations"""
	warehouses = frappe.get_all("Warehouse", filters={"company": company, "is_group": 0}, limit=5)
	if not warehouses:
		return
	
	for i in range(count):
		quotation = frappe.new_doc("Quotation")
		quotation.party_name = choice(customers)
		quotation.transaction_date = add_days(nowdate(), -randint(1, 30))
		quotation.valid_till = add_days(quotation.transaction_date, randint(15, 30))
		
		# Add items
		for _ in range(randint(1, 4)):
			quotation.append("items", {
				"item_code": choice(items),
				"qty": randint(1, 10),
				"warehouse": choice(warehouses).name,
				"rate": flt(randint(100, 1000), 2)
			})
		
		try:
			quotation.insert(ignore_permissions=True)
			if i % 3 == 0:  # Submit some quotations
				quotation.submit()
		except Exception as e:
			print(f"    Warning: Could not create quotation: {str(e)}")

# CRM Functions

def create_leads(count):
	"""Create demo leads"""
	leads = []
	lead_names = [
		"Tech Startup Inc", "Digital Solutions", "Cloud Services Co", "AI Innovations",
		"Data Analytics Ltd", "Software Solutions", "Web Development Co", "Mobile Apps Inc",
		"E-commerce Platform", "SaaS Provider", "IT Consulting", "Network Services",
		"Security Solutions", "DevOps Services", "Cloud Infrastructure", "Big Data Corp",
		"Machine Learning Co", "IoT Solutions", "Blockchain Services", "Fintech Startup",
		"Healthcare Tech", "EdTech Solutions", "Retail Tech", "Manufacturing Tech", "Logistics Tech"
	]
	
	lead_sources = ["Website", "Email Campaign", "Cold Call", "Referral", "Trade Show", "Social Media"]
	
	for i in range(count):
		name = lead_names[i % len(lead_names)]
		if frappe.db.exists("Lead", name):
			leads.append(name)
			continue
			
		lead = frappe.new_doc("Lead")
		lead.lead_name = name
		lead.company_name = name
		lead.email_id = f"contact@{name.lower().replace(' ', '')}.com"
		lead.mobile_no = f"+1{randint(2000000000, 9999999999)}"
		lead.source = choice(lead_sources)
		lead.status = choice(["Open", "Contacted", "Nurturing", "Qualified"])
		lead.industry = choice(["Technology", "Manufacturing", "Retail", "Services", "Healthcare"])
		lead.insert(ignore_permissions=True)
		leads.append(lead.name)
	
	return leads

def create_opportunities(count, leads):
	"""Create opportunities from leads"""
	opportunities = []
	
	for i in range(count):
		if not leads:
			break
			
		lead = choice(leads)
		opp_name = f"Opportunity from {lead}"
		
		if frappe.db.exists("Opportunity", opp_name):
			continue
			
		opportunity = frappe.new_doc("Opportunity")
		opportunity.opportunity_from = "Lead"
		opportunity.party_name = lead
		opportunity.opportunity_type = choice(["Sales", "Maintenance", "Support"])
		opportunity.status = choice(["Open", "Quotation", "Negotiation", "Converted"])
		opportunity.expected_closing = add_days(nowdate(), randint(7, 60))
		opportunity.probability = randint(10, 90)
		opportunity.opportunity_amount = flt(randint(10000, 100000), 2)
		
		try:
			opportunity.insert(ignore_permissions=True)
			opportunities.append(opportunity.name)
		except Exception as e:
			print(f"    Warning: Could not create opportunity: {str(e)}")
	
	return opportunities

def create_deals(count):
	"""Create deals"""
	deals = []
	
	for i in range(count):
		deal_name = f"Deal {i+1} - {choice(['Q1', 'Q2', 'Q3', 'Q4'])} {choice(['2024', '2025'])}"
		
		if frappe.db.exists("CRM Deal", deal_name):
			continue
			
		try:
			deal = frappe.new_doc("CRM Deal")
			deal.deal_name = deal_name
			deal.status = choice(["Open", "Qualified", "Proposal", "Negotiation", "Won", "Lost"])
			deal.deal_value = flt(randint(5000, 50000), 2)
			deal.expected_close_date = add_days(nowdate(), randint(7, 90))
			deal.insert(ignore_permissions=True)
			deals.append(deal.name)
		except Exception as e:
			# Deal doctype might not exist in all CRM versions
			print(f"    Warning: Could not create deal: {str(e)}")
	
	return deals

# HRMS Functions

def create_employees(count, company):
	"""Create demo employees"""
	employees = []
	first_names = ["John", "Jane", "Mike", "Sarah", "David", "Emily", "Chris", "Lisa", "Robert", "Maria"]
	last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Wilson", "Martinez"]
	designations = ["Manager", "Developer", "Analyst", "Designer", "Engineer", "Consultant", "Specialist"]
	
	departments = frappe.get_all("Department", limit=5)
	if not departments:
		# Create default department
		dept = frappe.new_doc("Department")
		dept.department_name = "General"
		dept.company = company
		dept.insert(ignore_permissions=True)
		departments = [{"name": dept.name}]
	
	for i in range(count):
		first_name = choice(first_names)
		last_name = choice(last_names)
		employee_name = f"{first_name} {last_name}"
		
		if frappe.db.exists("Employee", {"employee_name": employee_name}):
			emp = frappe.get_doc("Employee", {"employee_name": employee_name})
			employees.append(emp.name)
			continue
			
		employee = frappe.new_doc("Employee")
		employee.first_name = first_name
		employee.last_name = last_name
		employee.employee_name = employee_name
		employee.company = company
		employee.date_of_joining = add_days(nowdate(), -randint(30, 365))
		employee.designation = choice(designations)
		employee.department = choice(departments).name
		employee.status = "Active"
		employee.gender = choice(["Male", "Female", "Other"])
		employee.date_of_birth = add_days(nowdate(), -randint(7300, 14600))  # 20-40 years ago
		employee.insert(ignore_permissions=True)
		employees.append(employee.name)
	
	return employees

def create_leave_applications(count, employees):
	"""Create leave applications"""
	leave_types = frappe.get_all("Leave Type", limit=5)
	if not leave_types:
		return
	
	for i in range(count):
		if not employees:
			break
			
		employee = choice(employees)
		leave_type = choice(leave_types).name
		
		leave_app = frappe.new_doc("Leave Application")
		leave_app.employee = employee
		leave_app.leave_type = leave_type
		leave_app.from_date = add_days(nowdate(), randint(-30, 30))
		leave_app.to_date = add_days(leave_app.from_date, randint(1, 5))
		leave_app.half_day = choice([0, 1])
		leave_app.status = choice(["Open", "Approved", "Rejected"])
		
		try:
			leave_app.insert(ignore_permissions=True)
			if leave_app.status == "Approved":
				leave_app.submit()
		except Exception as e:
			print(f"    Warning: Could not create leave application: {str(e)}")

def create_attendance_records(count, employees):
	"""Create attendance records"""
	for i in range(count):
		if not employees:
			break
			
		employee = choice(employees)
		attendance_date = add_days(nowdate(), -randint(0, 30))
		
		# Check if attendance already exists
		if frappe.db.exists("Attendance", {
			"employee": employee,
			"attendance_date": attendance_date
		}):
			continue
		
		attendance = frappe.new_doc("Attendance")
		attendance.employee = employee
		attendance.attendance_date = attendance_date
		attendance.status = choice(["Present", "Absent", "Half Day"])
		attendance.work_type = choice(["Work From Home", "Work From Office", None])
		
		try:
			attendance.insert(ignore_permissions=True)
			attendance.submit()
		except Exception as e:
			print(f"    Warning: Could not create attendance: {str(e)}")

def print_summary():
	"""Print summary of created data"""
	print("\n" + "="*50)
	print("DEMO DATA SUMMARY")
	print("="*50)
	
	doctypes = [
		"Customer", "Supplier", "Item", "Contact", "Address",
		"Sales Order", "Purchase Order", "Sales Invoice", "Purchase Invoice", "Quotation",
		"Lead", "Opportunity", "Employee", "Leave Application", "Attendance"
	]
	
	for doctype in doctypes:
		count = frappe.db.count(doctype)
		print(f"  {doctype:25} : {count}")
	
	print("="*50)

if __name__ == "__main__":
	# This script should be run via bench console
	# bench --site demo.nexelya.com console
	# Then: exec(open('/home/ubuntu/frappe-bench/add_demo_data.py').read())
	# Or: from add_demo_data import setup_comprehensive_demo_data; setup_comprehensive_demo_data()
	pass
