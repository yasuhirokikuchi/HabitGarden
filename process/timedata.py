import pandas as pd
from datetime import datetime, date

# ŠÔŠÖ˜A

def get_today_str():
    return str(date.today())  # •¶š—ñŒ^‚É•ÏŠ·‚µ‚ÄŒ»İ‚Ì“ú•t‚ğ•Ô‚·

def get_habit_name_map(data):
    return {h["id"]: h["name"] for h in data["habits"]}

def calculate_streak(history: dict): # Œp‘±“ú”‚ğ•Ô‚·
    if not history:
        return 0
    streak = 0
    check_date = date.today()
    today_str = str(date.today())

    while True:
        d_str = str(check_date)
        if d_str in history and len(history[d_str]) > 0:
            streak += 1
            check_date = check_date - pd.Timedelta(days=1)
        else:
            if d_str == today_str and (d_str in history and len(history[d_str]) == 0):
                check_date = check_date - pd.Timedelta(days=1)
                continue
            break
    return streak