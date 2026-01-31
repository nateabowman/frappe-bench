# Phone Message Changes - Summary

## What Was Changed

### 1. Updated the Unavailable Message

**Old Message:**
> "Agent is unavailable to take the call, please call after some time."

**New Message:**
> "Thanks for calling Nexelya, you have reached us after business hours. Our business hours are Monday-Friday, 9 AM to 5 PM. For immediate support, please email sos@nexelya.com or call your account manager for immediate support."

### 2. Made the Message Configurable

The message is now stored in the `Twilio Settings` doctype as a field called `Unavailable Message`. This makes it easy to change without editing code.

## How to Change the Message (Easy Way)

### Step-by-Step Instructions:

1. **Login to Frappe/ERPNext**
2. **Search for**: `Twilio Settings` (in the search bar)
3. **Open** the `Twilio Settings` document
4. **Find** the field: `Unavailable Message`
5. **Edit** the message text
6. **Click** `Save`

That's it! The new message will be used immediately for all future calls.

## Files Modified

1. **`apps/twilio_integration/twilio_integration/twilio_integration/twilio_handler.py`**
   - Updated `IncomingCall.process()` method (line ~136)
   - Now reads message from `Twilio Settings` with a default fallback

2. **`apps/twilio_integration/twilio_integration/twilio_integration/doctype/twilio_settings/twilio_settings.json`**
   - Added new field: `unavailable_message`
   - Field type: `Small Text`
   - Default value: Your custom message
   - Location: After `Record Calls` field

## Next Steps

1. **Run migration** (if not already done):
   ```bash
   cd /home/ubuntu/frappe-bench
   bench --site prod.nexelya.com migrate
   ```

2. **Test the message**:
   - Call your Twilio phone number
   - Ensure no agents are available (not logged in or not configured)
   - You should hear the new message

3. **Customize if needed**:
   - Go to `Twilio Settings`
   - Edit the `Unavailable Message` field
   - Save

## Technical Details

- **Voice**: Uses Twilio's "alice" voice (natural-sounding female voice)
- **Language**: English (US)
- **Code Location**: `IncomingCall.process()` method in `twilio_handler.py`
- **Configuration**: `Twilio Settings` doctype, field `unavailable_message`
- **Fallback**: If the field is empty, uses the default message in code

## Documentation

- **Quick Guide**: See `HOW_TO_CHANGE_PHONE_MESSAGE.md`
- **Advanced Options**: See `PHONE_ATTENDANT_IMPROVEMENTS.md`

## Notes

- The message is played when no agents are available to take calls
- An agent is "available" if:
  - **Phone mode**: Has `call_receiving_device == 'Phone'` AND has `mobile_no` configured
  - **Computer mode**: Has `call_receiving_device == 'Computer'` AND is currently logged in
- The message change takes effect immediately after saving `Twilio Settings`
