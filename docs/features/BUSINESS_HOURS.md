# Business Hours Phone System Setup

## Overview

Your phone system now supports business hours scheduling with different messages and behaviors during and after business hours.

## Features

### 1. Business Hours Configuration
- Enable/disable business hours checking
- Set business days (Monday-Sunday)
- Set business hours start and end times
- Custom greeting for business hours
- Custom timeout message

### 2. During Business Hours
- **Greeting**: "Thanks for calling Nexelya, someone will be right with you."
- **Behavior**: Calls ring agents until answered
- **Timeout**: After 5 minutes (300 seconds) of no answer, call ends
- **Note**: Twilio's maximum Dial timeout is 4 minutes (240 seconds), so timeout is capped at 240 seconds

### 3. After Business Hours
- **Message**: Custom after-hours message
- **Behavior**: Message plays immediately, no ringing
- **Default Message**: "Thanks for calling Nexelya, you have reached us after business hours. Our business hours are Monday-Friday, 9 AM to 5 PM. For immediate support, please email sos@nexelya.com or call your account manager for immediate support."

## Setup Instructions

### Step 1: Enable Business Hours

1. **Login to Frappe/ERPNext**
2. **Go to**: `Twilio Settings` (search in the search bar)
3. **Find the section**: `Business Hours`
4. **Enable**: Check the `Enable Business Hours` checkbox
5. **Save**

### Step 2: Configure Business Days

1. In `Twilio Settings`, find `Business Days` field
2. Select the days you're open (e.g., Monday-Friday)
3. **Default**: Monday, Tuesday, Wednesday, Thursday, Friday

### Step 3: Set Business Hours

1. **Business Hours Start**: Set start time (e.g., 09:00:00 for 9 AM)
2. **Business Hours End**: Set end time (e.g., 17:00:00 for 5 PM)
3. **Default**: 9 AM to 5 PM

### Step 4: Customize Messages (Optional)

1. **Business Hours Greeting**: 
   - Default: "Thanks for calling Nexelya, someone will be right with you."
   - Customize as needed

2. **Timeout Message**:
   - Default: "We are currently unavailable. Please call back at another time."
   - Played if no one answers within timeout period

3. **Unavailable Message** (After Hours):
   - Default: "Thanks for calling Nexelya, you have reached us after business hours. Our business hours are Monday-Friday, 9 AM to 5 PM. For immediate support, please email sos@nexelya.com or call your account manager for immediate support."
   - Played when callers call outside business hours

### Step 5: Set Ring Timeout

1. **Ring Timeout (seconds)**: How long to ring before giving up
2. **Default**: 300 seconds (5 minutes)
3. **Note**: Twilio maximum is 240 seconds (4 minutes), so values above 240 will be capped at 240

### Step 6: Save and Test

1. **Click** `Save` on Twilio Settings
2. **Test** by calling your Twilio number:
   - During business hours: Should hear greeting and ring
   - After business hours: Should hear after-hours message immediately

## Configuration Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| Enable Business Hours | Checkbox | Unchecked | Enable/disable business hours checking |
| Business Days | MultiSelect | Mon-Fri | Days of the week you're open |
| Business Hours Start | Time | 09:00:00 | Start time (24-hour format) |
| Business Hours End | Time | 17:00:00 | End time (24-hour format) |
| Business Hours Greeting | Text | "Thanks for calling Nexelya..." | Message during business hours |
| Ring Timeout (seconds) | Integer | 300 | How long to ring (max 240) |
| Timeout Message | Text | "We are currently unavailable..." | Message if no answer |

## How It Works

### During Business Hours Flow:

1. Caller calls your Twilio number
2. System checks if current time is within business hours
3. If yes:
   - Plays greeting: "Thanks for calling Nexelya, someone will be right with you."
   - Tries to find available agent
   - If agent found: Rings agent (phone or computer)
   - If no agent: Plays timeout message
   - If agent doesn't answer within timeout: Call ends (no timeout message - Twilio limitation)

### After Business Hours Flow:

1. Caller calls your Twilio number
2. System checks if current time is within business hours
3. If no:
   - Plays after-hours message immediately
   - No ringing occurs
   - Call ends

## Technical Notes

### Timeout Limitation

**Important**: Twilio's Dial verb has a maximum timeout of 240 seconds (4 minutes). If you set a timeout longer than 240 seconds, it will be automatically capped at 240 seconds.

**Current Behavior**: After the timeout period, if no one answers, Twilio will end the call. Due to Twilio's TwiML limitations, we cannot play a message after a Dial timeout. The call will simply end.

**Future Enhancement**: To implement a post-timeout message, we would need to use Twilio webhooks/callbacks, which is more complex but possible.

### Timezone

The system uses the server's timezone. Make sure your server timezone is set correctly (you can check in Frappe Settings → System Settings).

### Business Hours Calculation

- Business hours are calculated based on:
  - Current day of week (must match selected business days)
  - Current time (must be between start and end time)
- Times are in 24-hour format (e.g., 09:00 = 9 AM, 17:00 = 5 PM)

## Troubleshooting

### Message not playing correctly
- Check that `Enable Business Hours` is checked
- Verify business days and hours are set correctly
- Check server timezone

### Calls not ringing during business hours
- Verify agents have `Voice Call Settings` configured
- Check that agents' `call_receiving_device` is set (Phone or Computer)
- For Phone mode: Ensure `mobile_no` is configured
- For Computer mode: Ensure agent is logged in

### Timeout not working
- Remember: Maximum timeout is 240 seconds (4 minutes)
- Timeout only applies during business hours
- If no agents are available, timeout message plays immediately

## Migration

After updating the code, run:

```bash
cd /home/ubuntu/frappe-bench
bench --site prod.nexelya.com migrate
```

This will add the new fields to Twilio Settings.
