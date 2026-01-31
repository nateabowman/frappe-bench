import frappe
from frappe.utils import flt, getdate, date_diff


def calculate_variance(budget, actual):
	"""Calculate budget variance"""
	if not budget:
		return 0
	return flt(budget - actual, 2)


def calculate_variance_percent(budget, actual):
	"""Calculate budget variance percentage"""
	if not budget:
		return 0
	variance = budget - actual
	return flt((variance / budget) * 100, 2)


def calculate_earned_value(budget, percent_complete):
	"""Calculate earned value (BCWP)"""
	return flt(budget * (percent_complete / 100), 2)


def calculate_spi(earned_value, planned_value):
	"""Calculate Schedule Performance Index"""
	if not planned_value:
		return 1
	return flt(earned_value / planned_value, 3)


def calculate_cpi(earned_value, actual_cost):
	"""Calculate Cost Performance Index"""
	if not actual_cost:
		return 1
	return flt(earned_value / actual_cost, 3)


def calculate_estimate_at_completion(budget, cpi):
	"""Calculate Estimate at Completion"""
	if not cpi or cpi == 0:
		return budget
	return flt(budget / cpi, 2)


def get_working_days(start_date, end_date, holiday_list=None):
	"""Calculate working days between two dates"""
	if not start_date or not end_date:
		return 0
	
	start = getdate(start_date)
	end = getdate(end_date)
	total_days = date_diff(end, start) + 1
	
	if not holiday_list:
		return total_days
	
	# Get holidays
	holidays = frappe.get_all(
		"Holiday",
		filters={"parent": holiday_list, "holiday_date": ["between", [start, end]]},
		pluck="holiday_date",
	)
	
	return total_days - len(holidays)


def format_currency_for_display(amount, currency=None):
	"""Format amount for display"""
	if not currency:
		currency = frappe.db.get_default("currency") or "USD"
	return frappe.format_value(amount, {"fieldtype": "Currency", "options": currency})


def jinja_methods():
	"""Jinja methods for templates"""
	return {
		"calculate_variance": calculate_variance,
		"calculate_variance_percent": calculate_variance_percent,
		"format_currency": format_currency_for_display,
	}
