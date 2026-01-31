import re
import json
from datetime import datetime
from twilio.rest import Client as TwilioClient
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant
from twilio.twiml.voice_response import VoiceResponse, Dial

import frappe
from frappe import _
from frappe.utils.password import get_decrypted_password
from frappe.utils import get_datetime, now_datetime
from .utils import get_public_url, merge_dicts

class Twilio:
	"""Twilio connector over TwilioClient.
	"""
	def __init__(self, settings):
		"""
		:param settings: `Twilio Settings` doctype
		"""
		self.settings = settings
		self.account_sid = settings.account_sid
		self.application_sid = settings.twiml_sid
		self.api_key = settings.api_key
		self.api_secret = settings.get_password("api_secret")
		self.twilio_client = self.get_twilio_client()

	@classmethod
	def connect(self):
		"""Make a twilio connection.
		"""
		settings = frappe.get_doc("Twilio Settings")
		if not (settings and settings.enabled):
			return
		return Twilio(settings=settings)

	def get_phone_numbers(self):
		"""Get account's twilio phone numbers.
		"""
		numbers = self.twilio_client.incoming_phone_numbers.list()
		return [n.phone_number for n in numbers]

	def generate_voice_access_token(self, from_number: str, identity: str, ttl=60*60):
		"""Generates a token required to make voice calls from the browser.
		"""
		# identity is used by twilio to identify the user uniqueness at browser(or any endpoints).
		identity = self.safe_identity(identity)

		# Create access token with credentials
		token = AccessToken(self.account_sid, self.api_key, self.api_secret, identity=identity, ttl=ttl)

		# Create a Voice grant and add to token
		voice_grant = VoiceGrant(
			outgoing_application_sid=self.application_sid,
			incoming_allow=True, # Allow incoming calls
		)
		token.add_grant(voice_grant)
		return token.to_jwt()

	@classmethod
	def safe_identity(cls, identity: str):
		"""Create a safe identity by replacing unsupported special charaters `@` with (at)).
		Twilio Client JS fails to make a call connection if identity has special characters like @, [, / etc)
		https://www.twilio.com/docs/voice/client/errors (#31105)
		"""
		return identity.replace('@', '(at)')

	@classmethod
	def emailid_from_identity(cls, identity: str):
		"""Convert safe identity string into emailID.
		"""
		return identity.replace('(at)', '@')

	def get_recording_status_callback_url(self):
		url_path = "/api/method/twilio_integration.twilio_integration.api.update_recording_info"
		return get_public_url(url_path)

	def generate_twilio_dial_response(self, from_number: str, to_number: str, timeout=None):
		"""Generates voice call instructions to forward the call to agents Phone.
		"""
		resp = VoiceResponse()
		dial = Dial(
			caller_id=from_number,
			timeout=timeout if timeout else 30,
			record=self.settings.record_calls,
			recording_status_callback=self.get_recording_status_callback_url(),
			recording_status_callback_event='completed'
		)
		dial.number(to_number)
		resp.append(dial)
		return resp

	def get_call_info(self, call_sid):
		return self.twilio_client.calls(call_sid).fetch()

	def generate_twilio_client_response(self, client, ring_tone='at', timeout=None):
		"""Generates voice call instructions to forward the call to agents computer.
		"""
		resp = VoiceResponse()
		dial = Dial(
			ring_tone=ring_tone,
			timeout=timeout if timeout else 30,
			record=self.settings.record_calls,
			recording_status_callback=self.get_recording_status_callback_url(),
			recording_status_callback_event='completed'
		)
		dial.client(client)
		resp.append(dial)
		return resp

	@classmethod
	def get_twilio_client(self):
		twilio_settings = frappe.get_doc("Twilio Settings")
		if not twilio_settings.enabled:
			frappe.throw(_("Please enable twilio settings before sending WhatsApp messages"))
		
		auth_token = get_decrypted_password("Twilio Settings", "Twilio Settings", 'auth_token')
		client = TwilioClient(twilio_settings.account_sid, auth_token)

		return client

def is_business_hours(settings):
	"""Check if current time is within business hours"""
	if not settings.get('business_hours_enabled'):
		return True  # If not enabled, always consider it business hours
	
	now = now_datetime()
	
	# Check day of week
	day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
	current_day = day_names[now.weekday()]
	
	business_days = settings.get('business_days', '').split('\n') if settings.get('business_days') else []
	business_days = [d.strip() for d in business_days if d.strip()]
	if business_days and current_day not in business_days:
		return False
	
	# Check time
	if settings.get('business_hours_start') and settings.get('business_hours_end'):
		start_time = settings.get('business_hours_start')
		end_time = settings.get('business_hours_end')
		current_time = now.time()
		
		# Parse time strings (format: HH:MM:SS or time object)
		if isinstance(start_time, str):
			start_parts = start_time.split(':')
			start_hour, start_min = int(start_parts[0]), int(start_parts[1])
			end_parts = end_time.split(':')
			end_hour, end_min = int(end_parts[0]), int(end_parts[1])
		else:
			start_hour, start_min = start_time.hour, start_time.minute
			end_hour, end_min = end_time.hour, end_time.minute
		
		current_minutes = current_time.hour * 60 + current_time.minute
		start_minutes = start_hour * 60 + start_min
		end_minutes = end_hour * 60 + end_min
		
		return start_minutes <= current_minutes < end_minutes
	
	return True  # Default to business hours if times not set

class IncomingCall:
	def __init__(self, from_number, to_number, meta=None):
		self.from_number = from_number
		self.to_number = to_number
		self.meta = meta

	def process(self):
		"""Process the incoming call
		* Check business hours if enabled
		* Figure out who is going to pick the call (call attender)
		* Check call attender settings and forward the call to Phone
		"""
		twilio = Twilio.connect()
		settings = frappe.get_doc('Twilio Settings')
		settings_dict = settings.as_dict() if hasattr(settings, 'as_dict') else frappe.db.get_value('Twilio Settings', 'Twilio Settings', ['business_hours_enabled', 'business_days', 'business_hours_start', 'business_hours_end', 'business_hours_greeting', 'business_hours_timeout', 'business_hours_timeout_message', 'unavailable_message'], as_dict=True)
		
		owners = get_twilio_number_owners(self.to_number)
		attender = get_the_call_attender(owners)
		
		# Check if business hours are enabled and if we're in business hours
		in_business_hours = is_business_hours(settings_dict)
		
		if not attender:
			resp = VoiceResponse()
			business_hours_enabled = settings_dict.get('business_hours_enabled') if settings_dict else False
			
			if in_business_hours and business_hours_enabled:
				# During business hours but no agent available - use timeout message
				timeout_message = settings_dict.get('business_hours_timeout_message') or \
					'We are currently unavailable. Please call back at another time.'
				resp.say(timeout_message, voice='alice', language='en-US')
			elif not in_business_hours and business_hours_enabled:
				# After business hours
				unavailable_message = settings_dict.get('unavailable_message') or \
					'Thanks for calling Nexelya, you have reached us after business hours. ' \
					'Our business hours are Monday-Friday, 9 AM to 5 PM. ' \
					'For immediate support, please email sos@nexelya.com or call your account manager for immediate support.'
				resp.say(unavailable_message, voice='alice', language='en-US')
			else:
				# Business hours not enabled - use default unavailable message
				unavailable_message = settings_dict.get('unavailable_message') if settings_dict else \
					'Agent is unavailable to take the call, please call after some time.'
				resp.say(unavailable_message, voice='alice', language='en-US')
			return resp

		# We have an attender available
		# Check if business hours are enabled - if not, use old behavior (no greeting)
		business_hours_enabled = settings_dict.get('business_hours_enabled') if settings_dict else False
		
		if in_business_hours and business_hours_enabled:
			# During business hours: play greeting then dial
			resp = VoiceResponse()
			greeting = settings_dict.get('business_hours_greeting') or \
				'Thanks for calling Nexelya, someone will be right with you.'
			resp.say(greeting, voice='alice', language='en-US')
			
			# Get timeout (default 5 minutes = 300 seconds, but Twilio max is 240 seconds)
			timeout = settings_dict.get('business_hours_timeout') or 300
			timeout = min(timeout, 240)  # Twilio Dial timeout max is 240 seconds (4 minutes)
			
			if attender['call_receiving_device'] == 'Phone':
				dial = Dial(
					caller_id=self.from_number,
					timeout=timeout,
					record=settings.record_calls,
					recording_status_callback=twilio.get_recording_status_callback_url(),
					recording_status_callback_event='completed'
				)
				dial.number(attender['mobile_no'])
				resp.append(dial)
			else:
				dial = Dial(
					ring_tone='at',
					timeout=timeout,
					record=settings.record_calls,
					recording_status_callback=twilio.get_recording_status_callback_url(),
					recording_status_callback_event='completed'
				)
				dial.client(twilio.safe_identity(attender['name']))
				resp.append(dial)
			return resp
		elif not in_business_hours and business_hours_enabled:
			# After business hours: play message
			resp = VoiceResponse()
			unavailable_message = settings_dict.get('unavailable_message') or \
				'Thanks for calling Nexelya, you have reached us after business hours. ' \
				'Our business hours are Monday-Friday, 9 AM to 5 PM. ' \
				'For immediate support, please email sos@nexelya.com or call your account manager for immediate support.'
			resp.say(unavailable_message, voice='alice', language='en-US')
			return resp
		else:
			# Business hours not enabled - use old behavior (no greeting, just dial)
			if attender['call_receiving_device'] == 'Phone':
				return twilio.generate_twilio_dial_response(self.from_number, attender['mobile_no'])
			else:
				return twilio.generate_twilio_client_response(twilio.safe_identity(attender['name']))

class TwilioCallDetails:
	def __init__(self, call_info, call_from = None, call_to = None):
		self.call_info = call_info
		self.account_sid = call_info.get('AccountSid')
		self.application_sid = call_info.get('ApplicationSid')
		self.call_sid = call_info.get('CallSid')
		self.call_status = self.get_call_status(call_info.get('CallStatus'))
		self._call_from = call_from
		self._call_to = call_to

	def get_direction(self):
		"""TODO: Check why Twilio gives always Direction as `inbound`?
		"""
		if self.call_info.get('Caller').lower().startswith('client'):
			return 'Outgoing'
		return 'Incoming'

	def get_from_number(self):
		return self._call_from or self.call_info.get('From')

	def get_to_number(self):
		return self._call_to or self.call_info.get('To')

	@classmethod
	def get_call_status(cls, twilio_status):
		"""Convert Twilio given status into system status.
		"""
		twilio_status = twilio_status or ''
		return ' '.join(twilio_status.split('-')).title()

	def to_dict(self):
		return {
			'type': self.get_direction(),
			'status': self.call_status,
			'id': self.call_sid,
			'from': self.get_from_number(),
			'to': self.get_to_number()
		}


def get_twilio_number_owners(phone_number):
	"""Get list of users who is using the phone_number.
	>>> get_twilio_number_owners('+11234567890')
	{
		'owner1': {'name': '..', 'mobile_no': '..', 'call_receiving_device': '...'},
		'owner2': {....}
	}
	"""
	user_voice_settings = frappe.get_all(
		'Voice Call Settings',
		filters={'twilio_number': phone_number},
		fields=["name", "call_receiving_device"]
	)
	user_wise_voice_settings = {user['name']: user for user in user_voice_settings}

	user_general_settings = frappe.get_all(
		'User',
		filters = [['name', 'IN', user_wise_voice_settings.keys()]],
		fields = ['name', 'mobile_no']
	)
	user_wise_general_settings = {user['name']: user for user in user_general_settings}

	return merge_dicts(user_wise_general_settings, user_wise_voice_settings)


def get_active_loggedin_users(users):
	"""Filter the current loggedin users from the given users list
	"""
	rows = frappe.db.sql("""
		SELECT `user`
		FROM `tabSessions`
		WHERE `user` IN %(users)s
		""", {'users': users})
	return [row[0] for row in set(rows)]

def get_the_call_attender(owners):
	"""Get attender details from list of owners
	"""
	if not owners: return
	current_loggedin_users = get_active_loggedin_users(list(owners.keys()))
	for name, details in owners.items():
		if ((details['call_receiving_device'] == 'Phone' and details['mobile_no']) or
			(details['call_receiving_device'] == 'Computer' and name in current_loggedin_users)):
			return details
