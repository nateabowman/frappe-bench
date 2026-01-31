# Phone Attendant and Call Recording Improvements

## Current Issue

When calling your phone number, you hear: **"Agent is unavailable to take the call, please call after some time."**

## Where This Message Comes From

The message is defined in:
**File**: `apps/twilio_integration/twilio_integration/twilio_integration/twilio_handler.py`
**Line**: 136
**Class**: `IncomingCall.process()`

### Current Logic

1. When a call comes in, the system looks for available agents using `get_the_call_attender(owners)`
2. An agent is considered available if:
   - **Phone mode**: `call_receiving_device == 'Phone'` AND has a `mobile_no` configured
   - **Computer mode**: `call_receiving_device == 'Computer'` AND user is currently logged in
3. If no agent is available, the caller hears the "Agent is unavailable" message

## Improvements Available

### 1. Better Phone Attendant Messages

**Current**: Generic "Agent is unavailable to take the call, please call after some time."

**Options**:
- Customizable message per phone number
- Professional business hours message
- Voicemail option
- Callback request option
- Queue/hold music while waiting
- Multiple agent routing (try multiple agents before giving up)

### 2. Call Recording

**Current Status**: Call recording is already implemented but may need configuration.

**Where**: In `Twilio Settings` doctype, there's a `record_calls` field.

**How it works**:
- When enabled, all calls are automatically recorded
- Recordings are stored in Twilio and the URL is saved in the `Call Log` doctype
- Recordings can be accessed via the `recording_url` field in Call Log

**To enable/improve**:
1. Go to: `Twilio Settings` in Frappe
2. Enable `Record Calls` checkbox
3. Recordings will be automatically saved to Call Log records

## Recommended Solutions

### Option 1: Improve the Unavailable Message (Quick Fix)

Modify the message to be more professional and include options:

```python
# In twilio_handler.py, line ~136
if not attender:
    resp = VoiceResponse()
    # Better message
    resp.say(
        'Thank you for calling. Our team is currently unavailable. '
        'Please leave a voicemail or call back during business hours. '
        'Have a great day!',
        voice='alice',
        language='en-US'
    )
    # Could add voicemail recording here
    # resp.record(max_length=120, action='/api/method/twilio_integration.api.handle_voicemail')
    return resp
```

### Option 2: Add Voicemail Support (Medium Complexity)

Allow callers to leave voicemails when no agent is available:
- Use Twilio's `<Record>` verb
- Save voicemails as documents in Frappe
- Email notifications to agents

### Option 3: Call Queue/Routing (Advanced)

- Try multiple agents before giving up
- Hold music while searching for agents
- Queue system for multiple callers
- Business hours checking

### Option 4: Enhanced Call Recording

- Recording quality settings (mono/stereo)
- Recording format options
- Transcription integration
- Automatic call summary generation

## Files to Modify

1. **twilio_handler.py** (line 136): Unavailable message
2. **api.py**: Add voicemail handling endpoint (if implementing voicemail)
3. **Twilio Settings doctype**: Add configuration options for messages and recording settings
4. **Voice Call Settings doctype**: Per-user availability settings

## Quick Configuration Check

1. Check if agents have `Voice Call Settings` configured:
   - Go to: `Voice Call Settings`
   - Ensure users have:
     - `call_receiving_device` set (Phone or Computer)
     - If Phone: `mobile_no` configured
     - `twilio_number` set

2. Check Twilio Settings:
   - Go to: `Twilio Settings`
   - Enable `Record Calls` for better call recording
   - Verify Twilio credentials are correct

## Next Steps

Would you like me to:
1. **Customize the unavailable message** (quick fix)?
2. **Add voicemail support** (medium complexity)?
3. **Implement call queue/routing** (advanced)?
4. **Enhance call recording configuration** (configuration)?

Let me know which option(s) you'd like to implement!
