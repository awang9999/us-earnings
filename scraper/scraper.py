# Example URL
# https://finance.yahoo.com/calendar/earnings?from=2020-06-14&to=2020-06-20&day=2020-06-19
# Base URL: https://finance.yahoo.com/calendar/earnings
# Query parameters: ?from=2020-06-14&to=2020-06-20&day=2020-06-19
# Start: ?
# Information: from=2020-06-14, to=2020-06-20, day=2020-06-19
# Separator: &

import requests
from bs4 import BeautifulSoup
from stringset import StringSet
import datetime

BEFORE_OPEN = 0
AFTER_CLOSE = 1
UNSPECIFIED = 2
TAS = 3

'''
create_url(date : datetime.date) returns a string url to the corresponding yahoo
earnings calendar page of the given date.
'''


def create_url(date):
    # MON = 0, SUN = 6 ==> MON = 1, SUN = 0
    sundx = (date.weekday() + 1) % 7
    satdx = 6 - sundx

    sun_before = (date - datetime.timedelta(sundx)).isoformat()
    sat_after = (date + datetime.timedelta(satdx)).isoformat()
    date_str = date.isoformat()
    base_url = "https://finance.yahoo.com/calendar/earnings?from={}&to={}&day={}"
    return base_url.format(sun_before, sat_after, date_str)


'''
scrape(url : string) should scrape the provided URL according to the purposes of this
project and return a tuple (date : datetime.date, before_open : string list, 
after_close : string list, unspecified : string list, tas : string list)
'''


def scrape(url):
    date_string = url[-10:]
    before_open = StringSet()
    after_close = StringSet()
    unspecified = StringSet()
    tas = StringSet()

    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    # print("Page response: " + str(page.status_code))
    table_div = soup.find('div', id='cal-res-table')
    if(not table_div == None):
        tickers = table_div.find_all('a', class_='Fw(600) C($linkColor)')
        times = table_div.find_all(
            'td', class_='Va(m) Ta(end) Pstart(15px) W(20%) Fz(s)')

        ticker_lst = []
        time_lst = []

        for t in tickers:
            tick = t.text.strip()
            ticker_lst.append(tick)

        for t in times:
            sp = t.find('span')
            if(not sp == None):
                time = sp.text.strip()
                if time == "Before Market Open":
                    time_lst.append(BEFORE_OPEN)
                elif time == "After Market Close":
                    time_lst.append(AFTER_CLOSE)
                else:
                    time_lst.append(UNSPECIFIED)
            else:
                time = t.text.strip()
                time_lst.append(TAS)

        pair = (ticker_lst, time_lst)

        for tick, time in zip(ticker_lst, time_lst):
            if(time == BEFORE_OPEN):
                before_open.insert(tick)
            elif(time == AFTER_CLOSE):
                after_close.insert(tick)
            elif(time == TAS):
                tas.insert(tick)
            else:
                unspecified.insert(tick)
        return (datetime.date.fromisoformat(date_string),
                before_open.data,
                after_close.data,
                unspecified.data,
                tas.data)
    else:
        print("no data")
        return None


'''
scrape_date(date : datetime.date) takes a datetime.date object and returns the
tuple (date : datetime.date, before_open : string list, 
after_close : string list, unspecified : string list, tas : string list)
'''


def scrape_day(date, debug=False):
    url = create_url(date)
    ret = scrape(url)
    if(debug):
        for x in ret:
            print(x)
    return ret

# #Tests
# x = scrape_day(datetime.date(2020, 6, 26), debug=True)
