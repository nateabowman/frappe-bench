# Business Hours Phone System - Quick Start Guide

## What Changed?

Your phone system now supports **business hours scheduling** with different behaviors during and after business hours.

## Quick Setup (3 Steps)

### Step 1: Enable Business Hours
1. Go to: **Twilio Settings**
2. Find: **Business Hours** section
3. Check: **Enable Business Hours**
4. Click: **Save**

### Step 2: Set Your Hours
1. **Business Days**: Select days (default: Monday-Friday)
2. **Business Hours Start**: Set start time (e.g., 09:00:00 = 9 AM)
3. **Business Hours End**: Set end time (e.g., 17:00:00 = 5 PM)
4. Click: **Save**

### Step 3: Customize Messages (Optional)
1. **Business Hours Greeting**: Message during business hours
   - Default: "Thanks for calling Nexelya, someone will be right with you."
2. **Unavailable Message**: Message after business hours
   - Default: Your custom message about business hours
3. **Ring Timeout**: How long to ring (default: 300 seconds = 5 minutes, max: 240 seconds = 4 minutes)
4. Click: **Save**

## How It Works

### During Business Hours (e.g., Monday-Friday, 9 AM - 5 PM):
1. Caller calls your number
2. **Plays**: "Thanks for calling Nexelya, someone will be right with you."
3. **Rings** available agents
4. If no answer after timeout (5 minutes): Call ends

### After Business Hours:
1. Caller calls your number
2. **Plays immediately**: Your after-hours message
3. **No ringing** - call ends after message

## Default Messages

### During Business Hours:
> "Thanks for calling Nexelya, someone will be right with you."

### After Business Hours:
> "Thanks for calling Nexelya, you have reached us after business hours. Our business hours are Monday-Friday, 9 AM to 5 PM. For immediate support, please email sos@nexelya.com or call your account manager for immediate support."

## Important Notes

1. **Timeout Limit**: Twilio's maximum dial timeout is 240 seconds (4 minutes). If you set 5 minutes, it will be capped at 4 minutes.

2. **After Timeout**: Due to Twilio limitations, we cannot play a message after the timeout period. The call will simply end if no one answers.

3. **Time Zone**: Business hours use your server's time zone. Make sure it's set correctly in Frappe Settings.

## Need Help?

See **BUSINESS_HOURS_SETUP.md** for detailed documentation.
