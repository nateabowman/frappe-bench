"""External integrations for construction management"""
import frappe
from frappe import _
import json


# QuickBooks Integration
@frappe.whitelist()
def sync_to_quickbooks(job_site):
	"""Sync job site costs to QuickBooks Online"""
	settings = get_quickbooks_settings()
	if not settings.get("enabled"):
		frappe.throw(_("QuickBooks integration is not enabled"))
	
	job = frappe.get_doc("Job Site", job_site)
	
	# Get cost entries to sync
	entries = frappe.get_all(
		"Job Cost Entry",
		filters={"job_site": job_site, "docstatus": 1},
		fields=["*"]
	)
	
	synced = 0
	for entry in entries:
		try:
			# Create QuickBooks expense/bill
			qb_data = {
				"Line": [{
					"Amount": entry.total_cost,
					"Description": f"{job.job_name}: {entry.description}",
					"DetailType": "AccountBasedExpenseLineDetail",
					"AccountBasedExpenseLineDetail": {
						"AccountRef": {"value": settings.get("expense_account")}
					}
				}],
				"VendorRef": {"value": entry.supplier} if entry.supplier else None,
			}
			
			# This would call the actual QuickBooks API
			# result = quickbooks_api_call("POST", "/bill", qb_data)
			synced += 1
			
		except Exception as e:
			frappe.log_error(f"QuickBooks sync error for {entry.name}: {str(e)}")
	
	return {"synced": synced, "total": len(entries)}


@frappe.whitelist()
def sync_to_xero(job_site):
	"""Sync job site costs to Xero"""
	settings = get_xero_settings()
	if not settings.get("enabled"):
		frappe.throw(_("Xero integration is not enabled"))
	
	job = frappe.get_doc("Job Site", job_site)
	
	# Get invoices to sync
	invoices = frappe.get_all(
		"Purchase Invoice",
		filters={"job_site": job_site, "docstatus": 1},
		fields=["*"]
	)
	
	synced = 0
	for invoice in invoices:
		try:
			# Create Xero bill
			xero_data = {
				"Type": "ACCPAY",
				"Contact": {"Name": invoice.supplier_name},
				"Reference": invoice.name,
				"LineItems": []
			}
			
			# Get invoice items
			items = frappe.get_all(
				"Purchase Invoice Item",
				filters={"parent": invoice.name},
				fields=["item_name", "qty", "rate", "amount"]
			)
			
			for item in items:
				xero_data["LineItems"].append({
					"Description": f"{job.job_name}: {item.item_name}",
					"Quantity": item.qty,
					"UnitAmount": item.rate,
					"AccountCode": settings.get("expense_account")
				})
			
			# This would call the actual Xero API
			# result = xero_api_call("PUT", "/Invoices", xero_data)
			synced += 1
			
		except Exception as e:
			frappe.log_error(f"Xero sync error for {invoice.name}: {str(e)}")
	
	return {"synced": synced, "total": len(invoices)}


# MS Project Integration
@frappe.whitelist()
def import_ms_project(file_url, job_site):
	"""Import schedule from MS Project XML file"""
	from frappe.utils.file_manager import get_file
	
	try:
		file_content = get_file(file_url)[1]
		
		# Parse MS Project XML
		import xml.etree.ElementTree as ET
		root = ET.fromstring(file_content)
		
		# Create new schedule
		schedule = frappe.new_doc("Gantt Schedule")
		schedule.job_site = job_site
		schedule.schedule_name = f"Imported from MS Project"
		schedule.schedule_type = "CPM"
		schedule.use_cpm = 1
		
		# Parse tasks
		ns = {"msp": "http://schemas.microsoft.com/project"}
		tasks = root.findall(".//msp:Task", ns) or root.findall(".//Task")
		
		for task in tasks:
			name = task.find("Name", ns) or task.find("Name")
			if name is None or not name.text:
				continue
			
			uid = task.find("UID", ns) or task.find("UID")
			start = task.find("Start", ns) or task.find("Start")
			finish = task.find("Finish", ns) or task.find("Finish")
			duration = task.find("Duration", ns) or task.find("Duration")
			
			schedule.append("activities", {
				"activity_id": uid.text if uid is not None else str(len(schedule.activities) + 1),
				"activity_name": name.text,
				"start_date": parse_ms_date(start.text if start is not None else None),
				"end_date": parse_ms_date(finish.text if finish is not None else None),
				"duration": parse_ms_duration(duration.text if duration is not None else None),
			})
		
		schedule.insert()
		return {"schedule": schedule.name, "activities_imported": len(schedule.activities)}
		
	except Exception as e:
		frappe.log_error(f"MS Project import error: {str(e)}")
		frappe.throw(_("Failed to import MS Project file: {0}").format(str(e)))


@frappe.whitelist()
def export_to_ms_project(schedule_name):
	"""Export schedule to MS Project XML format"""
	schedule = frappe.get_doc("Gantt Schedule", schedule_name)
	
	# Build MS Project XML
	xml_content = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Project xmlns="http://schemas.microsoft.com/project">
	<Name>{schedule.schedule_name}</Name>
	<StartDate>{schedule.start_date}</StartDate>
	<Tasks>
'''
	
	for i, activity in enumerate(schedule.activities):
		xml_content += f'''		<Task>
			<UID>{i + 1}</UID>
			<ID>{i + 1}</ID>
			<Name>{activity.activity_name}</Name>
			<Start>{activity.start_date}T08:00:00</Start>
			<Finish>{activity.end_date}T17:00:00</Finish>
			<Duration>PT{activity.duration * 8}H0M0S</Duration>
			<PercentComplete>{activity.percent_complete or 0}</PercentComplete>
		</Task>
'''
	
	xml_content += '''	</Tasks>
</Project>'''
	
	# Save as file
	from frappe.utils.file_manager import save_file
	file_doc = save_file(
		fname=f"{schedule_name}.xml",
		content=xml_content.encode(),
		dt="Gantt Schedule",
		dn=schedule_name,
		is_private=0
	)
	
	return {"file_url": file_doc.file_url}


@frappe.whitelist()
def import_primavera(file_url, job_site):
	"""Import schedule from Primavera P6 XER file"""
	# Primavera XER is a proprietary format
	# This would require parsing the XER format
	frappe.throw(_("Primavera P6 import coming soon"))


def get_quickbooks_settings():
	"""Get QuickBooks integration settings"""
	# This would come from a settings doctype
	return {
		"enabled": False,
		"client_id": "",
		"client_secret": "",
		"expense_account": "",
	}


def get_xero_settings():
	"""Get Xero integration settings"""
	return {
		"enabled": False,
		"client_id": "",
		"client_secret": "",
		"expense_account": "",
	}


def parse_ms_date(date_str):
	"""Parse MS Project date format"""
	if not date_str:
		return None
	try:
		from datetime import datetime
		# MS Project format: 2024-01-15T08:00:00
		dt = datetime.fromisoformat(date_str.replace("Z", ""))
		return dt.date()
	except:
		return None


def parse_ms_duration(duration_str):
	"""Parse MS Project duration format (PT8H0M0S)"""
	if not duration_str:
		return 1
	try:
		# Extract hours from PT8H0M0S format
		import re
		match = re.search(r'PT(\d+)H', duration_str)
		if match:
			hours = int(match.group(1))
			return max(1, hours // 8)  # Convert to days
	except:
		pass
	return 1
