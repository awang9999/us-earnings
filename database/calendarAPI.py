import mysql.connector as mariadb
import datetime
from stringset import StringSet

BEFORE_OPEN = 0
AFTER_CLOSE = 1
UNSPECIFIED = 2
TAS = 3

class CalendarAPI:

    def add_ticker(self, date, ticker, time):
        '''
        This function looks up the [date:datetime] in the database.
        If it does not exist, a new row with that date is created.
        Then, it adds the [ticker:string] to either the before_open
        or after_close list in the database.
        '''
        self.cur.execute(
            "SELECT * FROM calendar WHERE date = '%s'" % date.isoformat())
        temp = self.cur.fetchall()
        if (temp):
            row = temp[0]
            tickers = StringSet()
            if(time == BEFORE_OPEN):
                tickers.from_string(row[1])
                tickers.insert(ticker)
                sql = "UPDATE calendar SET before_open = '{}' WHERE date = '{}'".format(tickers.to_string(), date.isoformat())
                self.cur.execute(sql)
            elif(time == AFTER_CLOSE):
                tickers.from_string(row[2])
                tickers.insert(ticker)
                sql = "UPDATE calendar SET after_close = '{}' WHERE date = '{}'".format(tickers.to_string(), date.isoformat())
                self.cur.execute(sql)
            elif(time == UNSPECIFIED):
                tickers.from_string(row[3])
                tickers.insert(ticker)
                sql = "UPDATE calendar SET unspecified = '{}' WHERE date = '{}'".format(tickers.to_string(), date.isoformat())
                self.cur.execute(sql)
            else:
                tickers.from_string(row[4])
                tickers.insert(ticker)
                sql = "UPDATE calendar SET tas = '{}' WHERE date = '{}'".format(tickers.to_string(), date.isoformat())
                self.cur.execute(sql)
        else:
            if (time == BEFORE_OPEN):
                sql = "INSERT INTO calendar (date, before_open, after_close, unspecified, tas) VALUES ('{}', '{}', NULL, NULL, NULL)".format(date.isoformat(), ticker)
                self.cur.execute(sql)
            elif(time == AFTER_CLOSE):
                sql = "INSERT INTO calendar (date, before_open, after_close, unspecified, tas) VALUES ('{}', NULL, '{}', NULL, NULL)".format(date.isoformat(), ticker)
                self.cur.execute(sql)
            elif(time == UNSPECIFIED):
                sql = "INSERT INTO calendar (date, before_open, after_close, unspecified, tas) VALUES ('{}', NULL, NULL, '{}', NULL)".format(date.isoformat(), ticker)
                self.cur.execute(sql)
            else:
                sql = "INSERT INTO calendar (date, before_open, after_close, unspecified, tas) VALUES ('{}', NULL, NULL, NULL, '{}')".format(date.isoformat(), ticker)
                self.cur.execute(sql)
        self.con.commit()

    def remove_ticker(self, date, ticker, time):
        self.cur.execute(
            "SELECT * FROM calendar WHERE date = '{}'".format(date.isoformat()))
        temp = self.cur.fetchall()
        if(temp):
            row = temp[0]
            tickers = StringSet()
            if(time == BEFORE_OPEN):
                tickers.from_string(row[1])
                tickers.remove(ticker)
                sql = "UPDATE calendar SET before_open = '{}' WHERE date = '{}'".format(tickers.to_string(), date.isoformat())
                self.cur.execute(sql)
            elif(time == AFTER_CLOSE):
                tickers.from_string(row[2])
                tickers.remove(ticker)
                sql = "UPDATE calendar SET after_close = '{}' WHERE date = '{}'".format(tickers.to_string(), date.isoformat())
                self.cur.execute(sql)
            elif(time == UNSPECIFIED):
                tickers.from_string(row[3])
                tickers.remove(ticker)
                sql = "UPDATE calendar SET unspecified = '{}' WHERE date = '{}'".format(tickers.to_string(), date.isoformat())
                self.cur.execute(sql)
            else:
                tickers.from_string(row[4])
                tickers.remove(ticker)
                sql = "UPDATE calendar SET tas = '{}' WHERE date = '{}'".format(tickers.to_string(), date.isoformat())
                self.cur.execute(sql)
        self.con.commit()


    def remove_date(self, date):
        self.cur.execute("DELETE FROM calendar WHERE date = '{}'".format(date.isoformat()))
        self.con.commit()

    def __init__(self):
        super().__init__()
        self.con = mariadb.connect(
            host="localhost",
            database="usearnings",
            user="admin",
            password="agsd-lt2018"
        )
        self.cur = self.con.cursor()

    def __delete__(self, instance):
         if(self.con.is_connected()):
            self.cur.close()
            self.con.close()
            print("calendarAPI object destroyed.")

# # TESTS
# capi = CalendarAPI()

# # Alphabetically sorted after insertion test
# some_day = datetime.date(2020, 6, 16)
# capi.add_ticker(some_day, 'TSLA', AFTER_CLOSE)
# capi.add_ticker(some_day, 'AAPL', AFTER_CLOSE)
# capi.add_ticker(some_day, 'DAL', AFTER_CLOSE)
# capi.add_ticker(some_day, 'BAC', AFTER_CLOSE)
# capi.add_ticker(some_day, 'BA', AFTER_CLOSE)

# # before_open and after_close shouldn't affect each other. duplicates across two
# # columns is allowed.
# some_day = datetime.date(2020, 6, 17)
# capi.add_ticker(some_day, 'AAPL', BEFORE_OPEN)
# capi.add_ticker(some_day, 'AAPL', AFTER_CLOSE)
# capi.add_ticker(some_day, 'AAPL', UNSPECIFIED)
# capi.add_ticker(some_day, 'AAPL', AFTER_CLOSE)
# capi.add_ticker(some_day, 'AAPL', BEFORE_OPEN)
# capi.add_ticker(some_day, 'AAPL', TAS)

# # Inserting duplicate tickers test
# some_day = datetime.date(2020, 6, 18)
# capi.add_ticker(some_day, 'LULU', AFTER_CLOSE)
# capi.add_ticker(some_day, 'LULU', AFTER_CLOSE)
# capi.add_ticker(some_day, 'MSFT', AFTER_CLOSE)
# capi.add_ticker(some_day, 'LULU', AFTER_CLOSE)
# capi.add_ticker(some_day, 'MSFT', AFTER_CLOSE)
# capi.remove_ticker(some_day, 'PPL', AFTER_CLOSE)

# capi.remove_date(date=datetime.date(2020, 6, 18))
# capi.remove_date(date=datetime.date(2020, 6, 17))
# capi.remove_date(date=datetime.date(2020, 6, 16))