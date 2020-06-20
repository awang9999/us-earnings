# Example URL
# https://finance.yahoo.com/calendar/earnings?from=2020-06-14&to=2020-06-20&day=2020-06-19
# Base URL: https://finance.yahoo.com/calendar/earnings
# Query parameters: ?from=2020-06-14&to=2020-06-20&day=2020-06-19
# Start: ?
# Information: from=2020-06-14, to=2020-06-20, day=2020-06-19
# Separator: &

import requests
from bs4 import BeautifulSoup

URL = 'https://finance.yahoo.com/calendar/earnings?from=2020-06-14&to=2020-06-20&day=2020-06-19'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

print("Page response: " + str(page.status_code))

table_div = soup.find('div', id='cal-res-table')
tickers = table_div.find_all('a', class_='Fw(600) C($linkColor)')
times = table_div.find_all(
    'td', class_='Va(m) Ta(end) Pstart(15px) W(20%) Fz(s)')

for t in tickers:
    tick = t.text.strip()
    print(tick)

for t in times:
    sp = t.find('span')
    if(not sp == None):
        time = sp.text.strip()
        print(time)
    else:
        time = t.text.strip()
        print(time)
