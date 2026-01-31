# Copyright (c) 2024, Nexelya and Contributors
# License: GNU General Public License v3. See license.txt

"""
Advanced Mobile App API - Real-time sync endpoints
"""

import frappe
from frappe import _
from frappe.utils import now_datetime, get_datetime
from erpnext.projects.api.feature_gating import check_feature_access


@frappe.whitelist(allow_guest=False)
def sync_timesheet(timesheet_data, device_id=None, location=None):
	"""
	Sync timesheet data from mobile app
	
	Args:
		timesheet_data: Dict containing timesheet information
		device_id: Mobile device identifier
		location: GPS location data (lat, lng)
	"""
	# Check feature access
	company = timesheet_data.get("company")
	if company:
		check_feature_access("advanced_mobile_app", company, throw=True)
	
	# Create or update timesheet
	if timesheet_data.get("name"):
		ts = frappe.get_doc("Timesheet", timesheet_data["name"])
		ts.update(timesheet_data)
	else:
		ts = frappe.get_doc("Timesheet", timesheet_data)
	
	# Add mobile sync metadata
	if device_id:
		ts.db_set("custom_device_id", device_id)
	if location:
		ts.db_set("custom_sync_location", str(location))
	ts.db_set("custom_last_mobile_sync", now_datetime())
	
	ts.save()
	ts.submit()
	
	# Log sync
	log_mobile_sync("Timesheet", ts.name, device_id, location)
	
	return {
		"status": "success",
		"name": ts.name,
		"synced_at": now_datetime()
	}


@frappe.whitelist(allow_guest=False)
def sync_daily_log(log_data, device_id=None, location=None, photos=None):
	"""
	Sync daily log from mobile app with photos and GPS
	
	Args:
		log_data: Daily log data
		device_id: Mobile device identifier
		location: GPS location (lat, lng)
		photos: List of photo file URLs or base64 data
	"""
	company = frappe.db.get_value("Project", log_data.get("project"), "company")
	if company:
		check_feature_access("advanced_mobile_app", company, throw=True)
	
	if log_data.get("name"):
		dl = frappe.get_doc("Daily Log", log_data["name"])
		dl.update(log_data)
	else:
		dl = frappe.get_doc("Daily Log", log_data)
	
	# Add mobile-specific data
	if location:
		dl.db_set("custom_gps_latitude", location.get("lat"))
		dl.db_set("custom_gps_longitude", location.get("lng"))
	if photos:
		# Attach photos
		for photo in photos:
			frappe.attach_doc("Daily Log", dl.name, photo)
	
	dl.db_set("custom_last_mobile_sync", now_datetime())
	dl.save()
	
	log_mobile_sync("Daily Log", dl.name, device_id, location)
	
	return {"status": "success", "name": dl.name}


@frappe.whitelist(allow_guest=False)
def get_offline_data(doctype, last_sync=None, project=None):
	"""
	Get data for offline mode - returns all records modified since last_sync
	
	Args:
		doctype: DocType to sync
		last_sync: Last sync timestamp
		project: Filter by project
	"""
	check_feature_access("advanced_mobile_app", throw=True)
	
	filters = {}
	if last_sync:
		filters["modified"] = [">", get_datetime(last_sync)]
	if project and doctype in ["Task", "Timesheet", "Daily Log", "RFI", "Submittal"]:
		filters["project"] = project
	
	records = frappe.get_all(
		doctype,
		filters=filters,
		fields=["*"],
		limit=1000
	)
	
	return {
		"records": records,
		"sync_timestamp": now_datetime(),
		"count": len(records)
	}


def log_mobile_sync(doctype, docname, device_id=None, location=None):
	"""Log mobile sync activity"""
	if not frappe.db.exists("DocType", "Mobile Sync Log"):
		return
	
	try:
		frappe.get_doc({
			"doctype": "Mobile Sync Log",
			"sync_type": doctype,
			"document_name": docname,
			"device_id": device_id,
			"location": str(location) if location else None,
			"synced_by": frappe.session.user,
			"sync_timestamp": now_datetime()
		}).insert(ignore_permissions=True)
	except:
		pass  # Don't fail if logging fails

