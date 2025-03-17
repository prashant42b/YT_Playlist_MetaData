from datetime import datetime, timezone, timedelta

def convert_utc_to_ist(utc_time_str):
    
    #Parse the UTC time string
    utc_time = datetime.fromisoformat(utc_time_str.replace("Z", "+00:00"))
    
    #Define IST timezone (UTC+5:30)
    ist_offset = timedelta(hours=5, minutes=30)
    ist_time = utc_time + ist_offset
    
    # Format as a string (DD-MM-YYYY)
    return ist_time.strftime("%d-%m-%Y %H:%M:%S IST")