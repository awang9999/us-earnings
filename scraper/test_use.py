from jobsAPI import JobsAPI
from calendarAPI import CalendarAPI
from stringset import StringSet
from datetime import date

BEFORE_OPEN = 0
AFTER_CLOSE = 1
UNSPECIFIED = 2

capi = CalendarAPI()
day = date(2020, 6, 19)
capi.add_ticker(day, 'SENEB', BEFORE_OPEN)
capi.add_ticker(day, 'KMX', BEFORE_OPEN)
capi.add_ticker(day, 'LITB', BEFORE_OPEN)
capi.add_ticker(day, 'JBL', BEFORE_OPEN)
capi.add_ticker(day, 'LBYYQ', BEFORE_OPEN)
