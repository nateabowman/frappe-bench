# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe.utils import now
from datetime import timedelta


def get_cached_analytics_data(cache_key, fetch_function, cache_duration_minutes=30):
	"""Get cached analytics data or fetch fresh if cache expired"""
	
	cache_key_full = f"hrms:analytics:{cache_key}"
	cached_data = frappe.cache().get(cache_key_full)
	
	if cached_data:
		return cached_data
	
	# Fetch fresh data
	data = fetch_function()
	
	# Cache for specified duration
	frappe.cache().setex(
		cache_key_full,
		data,
		time=cache_duration_minutes * 60
	)
	
	return data


def invalidate_analytics_cache(pattern=None):
	"""Invalidate analytics cache"""
	
	if pattern:
		# Invalidate specific pattern
		frappe.cache().delete_keys(f"hrms:analytics:{pattern}*")
	else:
		# Invalidate all analytics cache
		frappe.cache().delete_keys("hrms:analytics:*")


def get_cache_key(employee=None, department=None, period=None, chart_type=None):
	"""Generate cache key for analytics data"""
	
	parts = [chart_type or "general"]
	if employee:
		parts.append(f"emp:{employee}")
	if department:
		parts.append(f"dept:{department}")
	if period:
		parts.append(f"period:{period}")
	
	return ":".join(parts)
