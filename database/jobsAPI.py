import mysql.connector as mariadb
import datetime
from stringset import StringSet
import re

'''
This function validates whether or not a string is an email address 
(at least by convention)
'''


def valid_email(email):
    regex = "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    if(re.match(regex, email)):
        return True
    else:
        return False


class JobsAPI:
    def __init__(self):
        super().__init__()
        self.con = mariadb.connect(
            host="localhost",
            user="admin",
            password="agsd-lt2018",
            database="usearnings"
        )
        self.cur = self.con.cursor()

    '''
    email should be a string containing the @ symbol followed by the . symbol.
    tickers should be a list of strings. If only one symbol, it should be
    [TICKER], or a list of length 1.
    '''

    def add_job(self, email, tickers):
        if(len(tickers) == 0):
            print("cannot add job with no tickers")
        elif(not valid_email(email)):
            print("invalid email address")
        else:
            str_set = StringSet()
            str_set.from_string_list(tickers)
            sql = "SELECT * FROM jobs WHERE email = %s AND tickers = %s"
            val = (email, str_set.to_string())
            self.cur.execute(sql, val)
            temp = self.cur.fetchall()
            if(temp):
                print("Identical job already exists")
            else:
                sql = "INSERT INTO jobs (id, email, tickers) VALUES (%s, %s, %s)"
                val = (None, email, str_set.to_string())
                self.cur.execute(sql, val)
                print("added ROW with email:%s and tickers:%s" %
                      (email, str_set.to_string()))

    '''
    email: string and tickers: string list expected
    This function grabs the unique id of the specific job containing exactly the
    email and tickers specified.
    '''

    def get_job_id(self, email, tickers):
        str_set = StringSet()
        str_set.from_string_list(tickers)
        sql = "SELECT * FROM jobs WHERE email = %s AND tickers = %s"
        val = (email, str_set.to_string())
        self.cur.execute(sql, val)
        temp = self.cur.fetchall()
        if(temp):
            return (temp[0])[0]
        else:
            print("job id doesn't exist with email={} and tickers={}".format(
                email, str_set.to_string()))
            return -1

    '''
    id : int, tickers : string list
    This function updates the ROW identified by id and adds the tickers specified
    in the arguement to the tickers in the ROW.
    '''

    def update_job_add_tickers(self, id, tickers):
        self.cur.execute("SELECT * FROM jobs WHERE id = {:d}".format(id))
        row = self.cur.fetchall()[0]
        id = row[0]
        email = row[1]
        old_tickers = StringSet()
        old_tickers.from_string(row[2])
        for t in tickers:
            old_tickers.insert(t)
        sql = "UPDATE jobs SET tickers = '{}' WHERE id = {:d}".format(
            old_tickers.to_string(), id)
        self.cur.execute(sql)

    '''
    id : int, tickers : string list
    This function updates the ROW identified by id and removes the tickers specified
    in the arguement from the tickers in the ROW.
    '''

    def update_job_remove_tickers(self, id, tickers): pass
    '''
    id : int
    This function removes the ROW indexed by the provided id
    '''

    def remove_job(self, id):
        sql = "DELETE FROM jobs WHERE jobs.id = {:d}".format(id)
        self.cur.execute(sql)

# Email validation tests
# mail1 = "alexander.wang2001@gmail.com"
# mail2 = "aw576@cornell.edu"
# mail3 = "corningstong.awang@io"

# print(valid_email(mail1))
# print(valid_email(mail2))
# print(valid_email(mail3))


# Add Job tests
# japi = JobsAPI()
# japi.add_job("alexander.wang2001@gmail.com",
#              ['AAPL', 'NDVA', 'TSLA', 'MMM', 'BAC', 'JPM'])
# japi.add_job("invalid.awa.g@io", ['AAPL'])
# japi.add_job("aw576@cornell.edu", [])

# Remove job tests and id test
# x = japi.get_job_id("alexander.wang2001@gmail.com",
#                     ['AAPL', 'NDVA', 'TSLA', 'MMM', 'BAC', 'JPM'])
# japi.remove_job(x)

# Test adding ticker to a job
# japi.update_job_add_tickers(x, ['DSX', 'LMT', 'TSLA'])

# x = japi.get_job_id("alexander.wang2001@gmail.com",
#                     ['AAPL', 'NDVA', 'TSLA', 'MMM', 'BAC', 'JPM', 'DSX', 'LMT'])

# Test removing ticker from a job
# japi.update_job_remove_tickers(x, ['AAPL', 'JPM'])
