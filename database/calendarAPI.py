import mysql.connector as mariadb
import datetime
from stringset import StringSet

BEFORE_OPEN = True
AFTER_CLOSE = False


def convert_date(date):
    return date.strftime('%Y-%m-%d')


class CalendarAPI:

    def add_ticker(self, date, ticker, morning):
        '''
        This function looks up the [date:datetime] in the database.
        If it does not exist, a new row with that date is created.
        Then, it adds the [ticker:string] to either the before_open
        or after_close list in the database.
        '''
        self.cur.execute(
            "SELECT * FROM calendar WHERE date = '%s'" % convert_date(date))
        temp = self.cur.fetchall()
        if (temp):
            row = temp[0]
            tickers = StringSet()
            if(morning):
                tickers.from_string(row[1])
                tickers.insert(ticker)
                sql = "UPDATE calendar SET before_open = %s WHERE date = %s"
                val = (tickers.to_string(), convert_date(date))
                self.cur.execute(sql, val)
            else:
                tickers.from_string(row[2])
                tickers.insert(ticker)
                sql = "UPDATE calendar SET after_close = %s WHERE date = %s"
                val = (tickers.to_string(), convert_date(date))
                self.cur.execute(sql, val)
        else:
            if (morning):
                sql = "INSERT INTO calendar (date, before_open, after_close) VALUES (%s, %s, %s)"
                val = (convert_date(date), ticker, None)
                # print("run " + sql % val)
                self.cur.execute(sql, val)
            else:
                sql = "INSERT INTO calendar (date, before_open, after_close) VALUES (%s, %s, %s)"
                val = (convert_date(date), None, ticker)
                # print("run " + sql % val)
                self.cur.execute(sql, val)

    def remove_ticker(self, date, ticker, morning):
        self.cur.execute(
            "SELECT * FROM calendar WHERE date = '%s'" % convert_date(date))
        temp = self.cur.fetchall()
        if(temp):
            row = temp[0]
            tickers = StringSet()
            if(morning):
                tickers.from_string(row[1])
                tickers.remove(ticker)
                sql = "UPDATE calendar SET before_open = %s WHERE date = %s"
                val = (tickers.to_string(), convert_date(date))
                self.cur.execute(sql, val)
            else:
                tickers.from_string(row[2])
                tickers.remove(ticker)
                sql = "UPDATE calendar SET after_close = %s WHERE date = %s"
                val = (tickers.to_string(), convert_date(date))
                self.cur.execute(sql, val)

    def __init__(self):
        super().__init__()
        self.con = mariadb.connect(
            host="localhost",
            user="root",
            password="",
            database="usearnings"
        )
        self.cur = self.con.cursor()


# TESTS
capi = CalendarAPI()

# Alphabetically sorted after insertion test
some_day = datetime.date(2020, 6, 16)
capi.add_ticker(some_day, 'TSLA', AFTER_CLOSE)
capi.add_ticker(some_day, 'AAPL', AFTER_CLOSE)
capi.add_ticker(some_day, 'DAL', AFTER_CLOSE)
capi.add_ticker(some_day, 'BAC', AFTER_CLOSE)
capi.add_ticker(some_day, 'BA', AFTER_CLOSE)

# before_open and after_close shouldn't affect each other. duplicates across two
# columns is allowed.
some_day = datetime.date(2020, 6, 17)
capi.add_ticker(some_day, 'AAPL', BEFORE_OPEN)
capi.add_ticker(some_day, 'AAPL', AFTER_CLOSE)
capi.add_ticker(some_day, 'AAPL', BEFORE_OPEN)
capi.add_ticker(some_day, 'AAPL', AFTER_CLOSE)
capi.add_ticker(some_day, 'AAPL', BEFORE_OPEN)

# Inserting duplicate tickers test
some_day = datetime.date(2020, 6, 18)
capi.add_ticker(some_day, 'LULU', AFTER_CLOSE)
capi.add_ticker(some_day, 'LULU', AFTER_CLOSE)
capi.add_ticker(some_day, 'MSFT', AFTER_CLOSE)
capi.add_ticker(some_day, 'LULU', AFTER_CLOSE)
capi.add_ticker(some_day, 'MSFT', AFTER_CLOSE)
capi.remove_ticker(some_day, 'PPL', AFTER_CLOSE)
