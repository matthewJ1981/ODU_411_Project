
import mysql.connector
import os
import sys
from dbTestInit import dbInit

class dbConnect:

    def __init__(self, _host = "default"):
        try:
            # Omitting the host will use the local cnf file to connect to ODU.  Use a host to connect to a local mysql container for testing
            # if _host == "default":
            #     self._cnx = mysql.connector.connect(option_files = os.path.dirname(os.path.realpath(__file__))+ '/.cnf')
            # else:
            #     self._cnx = mysql.connector.connect(user = "root", password = "1234", host = _host)
            # self._cursor = self._cnx.cursor()
            self._cnx = mysql.connector.connect(option_files = os.path.dirname(os.path.realpath(__file__))+ '/.cnf')
            self._cursor = self._cnx.cursor()
        except Exception as e:
            print(e)
            raise
        else:
            print("Connected to database @ " + self._cnx.server_host)
            #self.useDB()

    #database cursor
    def cursor(self):
        return self._cursor
    
    #database connection
    def cnx(self):
        return self._cnx
    
    #datbase connection and cursor as tuple
    def conn(self):
        return self._cnx, self._cursor
    #close cursor and connection
    def close(self):
        self._cursor.close()
        self._cnx.close()
        print("Closed connection to database")

    #### Methods to create and use a database for testing

    #Run dbInit code to create a test database
    def createTestDB(self):
        dbInit(self._cursor, self._cnx)

    #select littlelearners database after creating it
    def useDB(self):
        try:
            self._cursor.execute("use littlelearners;")
        except:
            return False
        
        return True
        # self._cursor.execute("describe parent;")
        # print(self._cursor.fetchall())

if __name__ == "__main__":
    db = dbConnect("localhost")
    db.close()