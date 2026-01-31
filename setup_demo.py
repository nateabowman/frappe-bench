#!/usr/bin/env python3
"""
Setup comprehensive demo data for demo.nexelya.com
Run with: bench --site demo.nexelya.com console
Then execute: exec(open('setup_demo.py').read())
"""

import frappe
from frappe.utils import add_days, getdate, nowdate, flt
from random import randint, choice

def setup_demo():
	"""Main function to setup all demo data"""
	frappe.set_user("Administrator")
	
	print("="*60)
	print("Setting up comprehensive demo data for demo.nexelya.com")
	print("="*60)
	
	# Get company
	companies = frappe.get_all("Company", limit=1)
	if not companies:
		print("❌ No company found. Please set up a company first.")
		return
	
	company = companies[0].name
	print(f"\n✓ Using company: {company}\n")
	
	# Setup ERPNext demo data using built-in function
	try:
		print("📦 Setting up ERPNext demo data...")
		from erpnext.setup.demo import setup_demo_data
		setup_demo_data()
		print("  ✅ ERPNext demo data created\n")
	except Exception as e:
		print(f"  ⚠️  ERPNext demo data: {str(e)}\n")
	
	# Add additional data
	print("📊 Adding additional demo data...")
	
	# Additional customers
	print("  Creating additional customers...")
	create_additional_customers(15)
	
	# Additional suppliers
	print("  Creating additional suppliers...")
	create_additional_suppliers(10)
	
	# Additional items
	print("  Creating additional items...")
	create_additional_items(20, company)
	
	# CRM data
	print("  Creating CRM leads and opportunities...")
	create_crm_data(20)
	
	# HRMS data
	print("  Creating HRMS employees and records...")
	create_hrms_data(15, company)
	
	# More transactions
	print("  Creating additional transactions...")
	create_additional_transactions(company)
	
	# Insights demo data
	print("  Setting up Insights demo data...")
	try:
		from insights.setup.demo import DemoDataFactory
		factory = DemoDataFactory.run(force=False)
		print("  ✅ Insights demo data created")
	except Exception as e:
		print(f"  ⚠️  Insights demo data: {str(e)}")
	
	print("\n" + "="*60)
	print("✅ Demo data setup completed!")
	print_summary()
	print("="*60)
	
	frappe.db.commit()

def create_additional_customers(count):
	"""Create additional customers"""
	names = [
		"Premier Solutions", "Advanced Systems", "Core Technologies", "Prime Services",
		"Elite Group", "Summit Corp", "Apex Industries", "Nexus Solutions",
		"Velocity Enterprises", "Stellar Corp", "Quantum Systems", "Phoenix Industries",
		"Horizon Corp", "Catalyst Solutions", "Fusion Group"
	]
	
	for i in range(count):
		name = names[i % len(names)] + f" {i+1}"
		if frappe.db.exists("Customer", name):
			continue
		
		try:
			customer = frappe.new_doc("Customer")
			customer.customer_name = name
			customer.customer_type = choice(["Company", "Individual"])
			customer.territory = choice(["All Territories", "North America", "Europe", "Asia"])
			customer.customer_group = "All Customer Groups"
			customer.insert(ignore_permissions=True)
		except Exception as e:
			print(f"    Warning: {str(e)}")

def create_additional_suppliers(count):
	"""Create additional suppliers"""
	names = [
		"Premium Supplies", "Quality Materials", "Reliable Sources", "Excellence Goods",
		"Superior Products", "First Class Supplies", "Elite Vendors", "Master Suppliers",
		"Pro Materials", "Ace Suppliers", "Champion Goods", "Top Quality Co"
	]
	
	for i in range(count):
		name = names[i % len(names)] + f" {i+1}"
		if frappe.db.exists("Supplier", name):
			continue
		
		try:
			supplier = frappe.new_doc("Supplier")
			supplier.supplier_name = name
			supplier.supplier_group = "All Supplier Groups"
			supplier.insert(ignore_permissions=True)
		except Exception as e:
			print(f"    Warning: {str(e)}")

def create_additional_items(count, company):
	"""Create additional items"""
	names = [
		"Wireless Mouse", "USB-C Cable", "Laptop Bag", "Monitor Stand",
		"Desk Mat", "Keyboard Wrist Rest", "Webcam Stand", "Microphone USB",
		"Speaker Bluetooth", "Headset Gaming", "Mouse Pad", "Cable Organizer",
		"Desk Fan", "LED Strip", "Power Strip", "Adapter USB", "Hub USB",
		"SD Card Reader", "External SSD", "Laptop Cooler"
	]
	
	item_groups = frappe.get_all("Item Group", limit=5)
	if not item_groups:
		return
	
	for i in range(count):
		name = names[i % len(names)]
		if frappe.db.exists("Item", name):
			continue
		
		try:
			item = frappe.new_doc("Item")
			item.item_code = name
			item.item_name = name
			item.item_group = item_groups[0].name
			item.stock_uom = "Nos"
			item.is_stock_item = 1
			
			warehouses = frappe.get_all("Warehouse", filters={"company": company, "is_group": 0}, limit=1)
			if warehouses:
				item.append("item_defaults", {
					"company": company,
					"default_warehouse": warehouses[0].name
				})
			
			item.insert(ignore_permissions=True)
		except Exception as e:
			print(f"    Warning: {str(e)}")

def create_crm_data(count):
	"""Create CRM leads and opportunities"""
	lead_names = [
		"Tech Innovations", "Digital Solutions", "Cloud Services", "AI Systems",
		"Data Analytics", "Software Dev", "Web Solutions", "Mobile Apps",
		"E-commerce", "SaaS Platform", "IT Services", "Network Solutions"
	]
	
	for i in range(count):
		name = lead_names[i % len(lead_names)] + f" {i+1}"
		if frappe.db.exists("Lead", name):
			continue
		
		try:
			lead = frappe.new_doc("Lead")
			lead.lead_name = name
			lead.company_name = name
			lead.email_id = f"contact@{name.lower().replace(' ', '')}.com"
			lead.mobile_no = f"+1{randint(2000000000, 9999999999)}"
			lead.source = choice(["Website", "Email", "Cold Call", "Referral"])
			lead.status = choice(["Open", "Contacted", "Qualified"])
			lead.industry = choice(["Technology", "Manufacturing", "Retail", "Services"])
			lead.insert(ignore_permissions=True)
			
			# Create opportunity for some leads
			if i % 2 == 0:
				opp = frappe.new_doc("Opportunity")
				opp.opportunity_from = "Lead"
				opp.party_name = lead.name
				opp.status = choice(["Open", "Quotation", "Negotiation"])
				opp.expected_closing = add_days(nowdate(), randint(7, 60))
				opp.opportunity_amount = flt(randint(10000, 100000), 2)
				opp.insert(ignore_permissions=True)
		except Exception as e:
			print(f"    Warning: {str(e)}")

def create_hrms_data(count, company):
	"""Create HRMS employees and records"""
	first_names = ["John", "Jane", "Mike", "Sarah", "David", "Emily", "Chris", "Lisa"]
	last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller"]
	designations = ["Manager", "Developer", "Analyst", "Designer", "Engineer"]
	
	departments = frappe.get_all("Department", limit=5)
	if not departments:
		try:
			dept = frappe.new_doc("Department")
			dept.department_name = "General"
			dept.company = company
			dept.insert(ignore_permissions=True)
			departments = [{"name": dept.name}]
		except:
			return
	
	employees = []
	for i in range(count):
		first_name = choice(first_names)
		last_name = choice(last_names)
		employee_name = f"{first_name} {last_name} {i+1}"
		
		if frappe.db.exists("Employee", {"employee_name": employee_name}):
			continue
		
		try:
			employee = frappe.new_doc("Employee")
			employee.first_name = first_name
			employee.last_name = last_name
			employee.employee_name = employee_name
			employee.company = company
			employee.date_of_joining = add_days(nowdate(), -randint(30, 365))
			employee.designation = choice(designations)
			employee.department = choice(departments).name
			employee.status = "Active"
			employee.gender = choice(["Male", "Female"])
			employee.insert(ignore_permissions=True)
			employees.append(employee.name)
		except Exception as e:
			print(f"    Warning: {str(e)}")
	
	# Create some attendance records
	for employee in employees[:5]:
		for day in range(5):
			att_date = add_days(nowdate(), -day)
			if not frappe.db.exists("Attendance", {
				"employee": employee,
				"attendance_date": att_date
			}):
				try:
					attendance = frappe.new_doc("Attendance")
					attendance.employee = employee
					attendance.attendance_date = att_date
					attendance.status = choice(["Present", "Present", "Present", "Absent"])
					attendance.insert(ignore_permissions=True)
					attendance.submit()
				except:
					pass

def create_additional_transactions(company):
	"""Create additional transactions"""
	customers = frappe.get_all("Customer", limit=20)
	suppliers = frappe.get_all("Supplier", limit=15)
	items = frappe.get_all("Item", limit=30)
	warehouses = frappe.get_all("Warehouse", filters={"company": company, "is_group": 0}, limit=5)
	
	if not (customers and suppliers and items and warehouses):
		return
	
	# Additional Sales Orders
	for i in range(10):
		try:
			so = frappe.new_doc("Sales Order")
			so.company = company
			so.customer = choice(customers).name
			so.transaction_date = add_days(nowdate(), -randint(1, 60))
			so.delivery_date = add_days(so.transaction_date, randint(7, 30))
			
			for _ in range(randint(1, 3)):
				so.append("items", {
					"item_code": choice(items).name,
					"qty": randint(1, 10),
					"warehouse": choice(warehouses).name,
					"rate": flt(randint(100, 1000), 2)
				})
			
			so.insert(ignore_permissions=True)
			if i % 3 == 0:
				so.submit()
		except Exception as e:
			pass
	
	# Additional Sales Invoices
	for i in range(8):
		try:
			si = frappe.new_doc("Sales Invoice")
			si.company = company
			si.customer = choice(customers).name
			si.posting_date = add_days(nowdate(), -randint(1, 45))
			si.due_date = add_days(si.posting_date, randint(15, 30))
			
			for _ in range(randint(1, 4)):
				si.append("items", {
					"item_code": choice(items).name,
					"qty": randint(1, 10),
					"warehouse": choice(warehouses).name,
					"rate": flt(randint(100, 1000), 2)
				})
			
			si.insert(ignore_permissions=True)
			if i % 2 == 0:
				si.submit()
		except Exception as e:
			pass

def print_summary():
	"""Print summary"""
	doctypes = [
		"Customer", "Supplier", "Item", "Contact", "Address",
		"Sales Order", "Purchase Order", "Sales Invoice", "Purchase Invoice",
		"Lead", "Opportunity", "Employee", "Attendance"
	]
	
	print("\nData Summary:")
	for doctype in doctypes:
		try:
			count = frappe.db.count(doctype)
			print(f"  {doctype:20} : {count}")
		except:
			pass

# Auto-run when exec'd or run directly
if True:  # Always run
	setup_demo()
