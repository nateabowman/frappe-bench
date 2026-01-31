import frappe
import requests
from frappe.utils import today


@frappe.whitelist()
def get_weather_for_location(latitude, longitude):
	"""Get weather data for a location using Open-Meteo API (free, no API key required)"""
	try:
		url = f"https://api.open-meteo.com/v1/forecast"
		params = {
			"latitude": latitude,
			"longitude": longitude,
			"current": "temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m",
			"temperature_unit": "fahrenheit",
			"wind_speed_unit": "mph",
			"precipitation_unit": "inch",
		}
		
		response = requests.get(url, params=params, timeout=10)
		response.raise_for_status()
		data = response.json()
		
		current = data.get("current", {})
		
		# Map weather codes to conditions
		weather_code = current.get("weather_code", 0)
		condition = get_weather_condition(weather_code)
		
		return {
			"success": True,
			"temperature": current.get("temperature_2m"),
			"humidity": current.get("relative_humidity_2m"),
			"precipitation": current.get("precipitation"),
			"wind_speed": current.get("wind_speed_10m"),
			"condition": condition,
			"weather_code": weather_code,
		}
	except Exception as e:
		frappe.log_error(f"Weather API error: {str(e)}", "Weather Fetch Error")
		return {
			"success": False,
			"error": str(e),
		}


def get_weather_condition(code):
	"""Map WMO weather code to condition string"""
	conditions = {
		0: "Clear",
		1: "Partly Cloudy",
		2: "Partly Cloudy",
		3: "Cloudy",
		45: "Fog",
		48: "Fog",
		51: "Rain",
		53: "Rain",
		55: "Rain",
		61: "Rain",
		63: "Rain",
		65: "Rain",
		71: "Snow",
		73: "Snow",
		75: "Snow",
		77: "Snow",
		80: "Rain",
		81: "Rain",
		82: "Rain",
		85: "Snow",
		86: "Snow",
		95: "Other",
		96: "Other",
		99: "Other",
	}
	return conditions.get(code, "Other")


def fetch_weather_for_active_sites():
	"""Scheduled task to fetch weather for all active job sites"""
	active_sites = frappe.get_all(
		"Job Site",
		filters={"status": ["in", ["Active", "In Progress"]]},
		fields=["name", "latitude", "longitude"],
	)
	
	for site in active_sites:
		if site.latitude and site.longitude:
			weather = get_weather_for_location(site.latitude, site.longitude)
			if weather.get("success"):
				frappe.db.set_value("Job Site", site.name, {
					"current_temperature": weather.get("temperature"),
					"current_weather": weather.get("condition"),
				}, update_modified=False)
	
	frappe.db.commit()
