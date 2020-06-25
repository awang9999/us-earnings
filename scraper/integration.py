import datetime
import scraper
from calendarAPI import CalendarAPI

BEFORE_OPEN = 0
AFTER_CLOSE = 1
UNSPECIFIED = 2
TAS = 3

capi = CalendarAPI()


def grab_data_and_input(date):
    ret = scraper.scrape_day(date)
    if(not ret == None):
        day = ret[0]
        b_open = ret[1]
        a_close = ret[2]
        unspec = ret[3]
        tas = ret[4]
        for x in b_open:
            capi.add_ticker(day, x, BEFORE_OPEN)
        for x in a_close:
            capi.add_ticker(day, x, AFTER_CLOSE)
        for x in unspec:
            capi.add_ticker(day, x, UNSPECIFIED)
        for x in tas:
            capi.add_ticker(day, x, TAS)


def scrape_between_range(start_date, end_date):
    d = start_date
    delta = datetime.timedelta(days=1)
    while(d <= end_date):
        grab_data_and_input(d)
        print("scraped " + d.isoformat())
        d += delta


day1 = datetime.date(2020, 6, 24)
day2 = datetime.date(2021, 6, 17)
day3 = datetime.date(2021, 6, 24)

until_EOY = scrape_between_range(day2, day3)
