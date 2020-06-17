import mysql.connector as mariadb
import datetime

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

        if (self.cur.fetchall()):
            print("yay")
        else:
            if (morning):
                sql = "INSERT INTO calendar (date, before_open, after_close) VALUES (%s, %s, %s)"
                val = (convert_date(date), ticker, None)
                print("run " + sql % val)
                self.cur.execute(sql, val)
            else:
                sql = "INSERT INTO calendar (date, before_open, after_close) VALUES (%s, %s, %s)"
                val = (convert_date(date), None, ticker)
                print("run " + sql % val)
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
some_day = datetime.date(2020, 6, 16)
capi.add_ticker(some_day, 'TSLA', AFTER_CLOSE)
some_day = datetime.date(2020, 6, 17)
capi.add_ticker(some_day, 'AAPL', BEFORE_OPEN)
some_day = datetime.date(2020, 6, 18)
capi.add_ticker(some_day, 'LULU', AFTER_CLOSE)
