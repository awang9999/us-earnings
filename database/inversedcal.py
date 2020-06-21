import mysql.connector as mariadb

mydb = mariadb.connect(
    host="localhost",
    user="root",
    password="",
    database="usearnings"
)

cursor = mydb.cursor()


def create_table():
    cursor.execute(
        "CREATE TABLE ticker_dates (ticker VARCHAR(255), dates VARCHAR(511));")


def inverse_calendar():
    pass
