#!/usr/bin/env python3
import frappe

# Initialize and connect
frappe.init(site='demo.nexelya.com')
frappe.connect()

# Now import and run
exec(open('/home/ubuntu/frappe-bench/add_demo_data.py').read())
setup_comprehensive_demo_data()

frappe.db.commit()
frappe.destroy()
