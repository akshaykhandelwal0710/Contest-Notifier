import datetime

priority_hours = 24

utcTimeDelta = datetime.timedelta(hours=0)
utcTZObject = datetime.timezone(utcTimeDelta, name="UTC")

cfTimeDelta = datetime.timedelta(hours=3)
cfTZObject = datetime.timezone(cfTimeDelta, name="CF")

istTimeDelta = datetime.timedelta(hours=5, minutes=30)
istTZObject = datetime.timezone(istTimeDelta, name="IST")
