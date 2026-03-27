
from datetime import datetime, timedelta

# 1. Subtract five days from current date.
current_date = datetime.now()
five_days_ago = current_date - timedelta(days=5)
print("Current date:", current_date)
print("Five days ago:", five_days_ago)

print("-" * 40)

# 2. Print yesterday, today, tomorrow.
today = datetime.now().date()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)

print("-" * 40)

# 3. Drop microseconds from datetime.
current_datetime = datetime.now()
without_microseconds = current_datetime.replace(microsecond=0)

print("With microseconds:", current_datetime)
print("Without microseconds:", without_microseconds)

print("-" * 40)

# 4. Calculate two date difference in seconds.
date1_str = input("Enter first date and time (YYYY-MM-DD HH:MM:SS): ")
date2_str = input("Enter second date and time (YYYY-MM-DD HH:MM:SS): ")

date1 = datetime.strptime(date1_str, "%Y-%m-%d %H:%M:%S")
date2 = datetime.strptime(date2_str, "%Y-%m-%d %H:%M:%S")

difference_in_seconds = abs((date2 - date1).total_seconds())
print("Difference in seconds:", difference_in_seconds)