import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(host='localhost',
                                         database='usearnings',
                                         user='admin',
                                         password='agsd-lt2018')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

        sql = "INSERT INTO calendar (date, before_open, after_close, unspecified, tas) VALUES ('2020-06-24', NULL, 'AMZN', 'MSFT', NULL)"
        cursor.execute(sql)
        connection.commit()
        print(cursor.rowcount, "Record inserted successfully into Laptop table")

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")