import mysql.connector as mariadb


class CalendarAPI:
    # Returns an instance of the cursor to the usearnings database
    def connect_to_database(self):
        mydb = mariadb.connect(
            host="localhost",
            user="root",
            password="",
            database="usearnings"
        )
        cursor = mydb.cursor()
        return cursor

    def addticker(self, date, ticker, bo_ac):
        '''
        This function looks up the [date:datetime] in the database. 
        If it does not exist, a new row with that date is created. 
        Then, it adds the [ticker:string] to either the before_open
        or after_close list in the database.
        '''
        pass

    def __init__(self):
        super().__init__()
        self.cursor = self.connect_to_database()
