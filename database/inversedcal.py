import mysql.connector as mariadb
from stringset import StringSet
import datetime

mydb = mariadb.connect(
    host="localhost",
    user="root",
    password="",
    database="usearnings"
)

cur = mydb.cursor()


def create_table():
    cur.execute(
        "CREATE TABLE ticker_dates (ticker VARCHAR(255), dates VARCHAR(511));")


def inverse_calendar():
    sql = "SELECT * FROM calendar"
    cur.execute(sql)
    for row in cur.fetchall():
        b_open = StringSet()
        a_close = StringSet()
        unspecified = StringSet()
        tas = StringSet()
        day = datetime.date.fromisoformat(str(row[0]))
        b_open.from_string(row[1])
        a_close.from_string(row[2])
        unspecified.from_string(row[3])
        tas.from_string(row[4])

        for t in b_open.data:
            insert_date(t, day)

        for t in a_close.data:
            insert_date(t, day)

        for t in unspecified.data:
            insert_date(t, day)

        for t in tas.data:
            insert_date(t, day)


def insert_date(ticker, date, debug=False):
    sql = "SELECT * FROM ticker_dates WHERE ticker = '{}'".format(ticker)
    cur.execute(sql)
    tmp = cur.fetchall()
    if(tmp):
        row = tmp[0]
        dates = StringSet()
        dates.from_string(row[1])
        dates.insert(date.isoformat())
        sql = "UPDATE ticker_dates SET dates = '{}' WHERE ticker = '{}'".format(
            dates.to_string(), ticker)
        if debug:
            print(sql)
        cur.execute(sql)
    else:
        sql = "INSERT INTO ticker_dates (ticker, dates) VALUES ('{}', '{}')".format(
            ticker, date.isoformat())
        if debug:
            print(sql)
        cur.execute(sql)


def remove_date(ticker, date, debug=False):
    sql = "SELECT * FROM ticker_dates WHERE ticker = '{}'".format(ticker)
    cur.execute(sql)
    tmp = cur.fetchall()
    if(tmp):
        row = tmp[0]
        dates = StringSet()
        dates.from_string(row[1])
        dates.remove(date.isoformat())
        sql = "UPDATE ticker_dates SET dates = '{}' WHERE ticker = '{}'".format(
            dates.to_string(), ticker)
        if debug:
            print(sql)
        cur.execute(sql)
    else:
        print("Attempting to remove from a ticker that is not indexed")


class Ticker_Explorer:
    def __init__(self):
        super().__init__()
        self.con = mariadb.connect(
            host="localhost",
            user="root",
            password="",
            database="usearnings"
        )
        self.cur = self.con.cursor()

    '''
    returns a sorted list of dates in isoformat on which [ticker] has an earning
    report
    '''

    def get_dates(self, ticker):
        sql = "SELECT * FROM ticker_dates WHERE ticker = '{}'".format(ticker)
        self.cur.execute(sql)
        tmp = self.cur.fetchall()
        row = tmp[0]
        sset = StringSet()
        sset.from_string(row[1])
        return sset.data


# insert_date("AFMD", datetime.date(2020, 6, 23), debug=True)
# insert_date("AFMD", datetime.date(2020, 6, 24), debug=True)
# insert_date("AFMD", datetime.date(2020, 6, 25), debug=True)
# remove_date("AFMD", datetime.date(2020, 6, 23), debug=True)

# insert_date("AFMD", datetime.date(2020, 6, 23))
# insert_date("AFMD", datetime.date(2020, 6, 24))
# insert_date("AFMD", datetime.date(2020, 6, 25))
# remove_date("AFMD", datetime.date(2020, 6, 23))

# inverse_calendar()

te = Ticker_Explorer()
print(te.get_dates("AMZN"))
