# def format_time(hours) -> str:
#     return f"{hours // 24}d {hours % 24:02d}h"

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def format_time(hours, start_date_str="01 Jan 2025"):
    start_date = datetime.strptime(start_date_str, "%d %b %Y")
    end_date = start_date + timedelta(hours=hours)
    diff = relativedelta(end_date, start_date)

    parts = [
        (diff.years, "year"),
        (diff.months, "month"),
        (diff.days, "day"),
        (diff.hours, "hour")
    ]

    formatted = ", ".join(f"{value} {name}{'s' if value != 1 else ''}"
                          for value, name in parts if value > 0)

    return formatted or "0 hours"
