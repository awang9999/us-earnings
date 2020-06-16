import mysql.connector as mariadb

mydb = mariadb.connect(
    host="localhost",
    user="root",
    password="",
    database="usearnings"
)

cursor = mydb.cursor()

cursor.execute(
    "CREATE DATABASE usearnings CHARACTER SET ascii COLLATE ascii_general_ci;")

cursor.execute(
    "CREATE TABLE calendar (date DATE, before_open VARCHAR(511), after_close VARCHAR(511));")

cursor.execute(
    "CREATE TABLE jobs (id INT AUTO_INCREMENT PRIMARY KEY, email VARCHAR(1023), tickers VARCHAR(12287));")

cursor.execute("SHOW TABLES")
for x in cursor:
    print(x)
