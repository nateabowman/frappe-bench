# How to Change the Phone Message (Easy Guide)

## Current Message

When callers reach your phone number and no agents are available, they hear:

> "Thanks for calling Nexelya, you have reached us after business hours. Our business hours are Monday-Friday, 9 AM to 5 PM. For immediate support, please email sos@nexelya.com or call your account manager for immediate support."

## How to Change the Message (Easy Way)

### Option 1: Via Frappe UI (Recommended)

1. **Login to your Frappe/ERPNext system**
2. **Go to**: `Twilio Settings` (search for it in the search bar)
3. **Find the field**: `Unavailable Message`
4. **Update the message** to whatever you want
5. **Save** the document

That's it! The new message will be used for all future calls.

### Option 2: Quick Change Steps

1. Open Frappe Desk
2. Search: `Twilio Settings`
3. Click on `Twilio Settings` document
4. Scroll to find `Unavailable Message` field
5. Edit the text
6. Click `Save`

## What Happens When No Agent is Available?

The system plays the "Unavailable Message" when:
- No agents have `Voice Call Settings` configured for that phone number
- Agents are configured but:
  - **Phone mode**: Agent's mobile number is not configured
  - **Computer mode**: Agent is not currently logged in

## Tips for Writing a Good Unavailable Message

1. **Be professional and friendly**
2. **Include business hours** (so callers know when to call back)
3. **Provide alternative contact methods** (email, support ticket, etc.)
4. **Keep it concise** (callers don't want to wait too long)
5. **Use clear language** (avoid jargon)

## Example Messages

### Simple:
> "Thank you for calling Nexelya. Our team is currently unavailable. Please leave a message or call back during business hours, Monday through Friday, 9 AM to 5 PM Eastern Time."

### With Email:
> "Thanks for calling Nexelya. You've reached us outside of business hours. Our team is available Monday through Friday, 9 AM to 5 PM. For urgent matters, please email support@nexelya.com. We'll respond within 24 hours."

### With Voicemail:
> "Thank you for calling Nexelya. We're currently unavailable. Please leave a detailed message with your name and contact number, and we'll return your call during business hours, Monday through Friday, 9 AM to 5 PM."

## Technical Details

- **File Location**: The code is in `apps/twilio_integration/twilio_integration/twilio_integration/twilio_handler.py`
- **Method**: `IncomingCall.process()` (around line 136)
- **Configuration**: The message is stored in `Twilio Settings` doctype, field `unavailable_message`
- **Voice**: Uses Twilio's "alice" voice (natural-sounding female voice)
- **Language**: English (US)

## Need Help?

If you need to make more advanced changes (like adding voicemail, call queues, or business hours checking), contact your system administrator or refer to the `PHONE_ATTENDANT_IMPROVEMENTS.md` document.
