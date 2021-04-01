import sqlite3

"""
This class represents database handler for this program, it stores and retrieves from server
"""
class MyBase(object):
    def __init__(self, db_name = "simijo.db"):
        self._db_connection = sqlite3.connect(db_name, check_same_thread=False)
        #this curser does all things
        self._db_cur = self._db_connection.cursor()
        #creating tables in database
        #similarity connection
        self._db_cur.execute("CREATE TABLE IF NOT EXISTS ds1Ds2Similarity(ds1 REAL, ds2 REAL)")
        self._db_cur.execute("CREATE TABLE IF NOT EXISTS ds1Similarity(ds1 REAL, ds2 REAL)")
        self._db_cur.execute("CREATE TABLE IF NOT EXISTS ds2Similarity(ds1 REAL, ds2 REAL)")
        #descriptor data
        self._db_cur.execute("CREATE TABLE IF NOT EXISTS ds1Data(fileId REAL, data TEXT)")
        self._db_cur.execute("CREATE TABLE IF NOT EXISTS ds1Names(fileId REAL, fileName TEXT)")
        #picture names
        self._db_cur.execute("CREATE TABLE IF NOT EXISTS ds2Data(fileId REAL, data TEXT)")
        self._db_cur.execute("CREATE TABLE IF NOT EXISTS ds2Names(fileId REAL, fileName TEXT)")

    """
    Method execute query on database with given parameters
    returns data from server
    """
    def query(self, query, params):
        return self._db_cur.execute(query, params)

    """
    Method saves given data to database
    Parameters:
        tableName: name of table where to save data
        argv: list of data to store
    """
    def insert(self, tableName, *argv):
        if tableName == "ds1Names":
            self.query("INSERT INTO ds1Names(fileId, fileName) VALUES (?, ?)",  argv)
        elif tableName == "ds2Names":
            self.query("INSERT INTO ds2Names(fileId, fileName) VALUES (?, ?)",  argv)
        elif tableName == "ds1Ds2Similarity":
            self.query("INSERT INTO ds1Ds2Similarity(ds1, ds2) VALUES (?, ?)",  argv)
        elif tableName == "ds1Similarity":
            self.query("INSERT INTO ds1Similarity(ds1, ds2) VALUES (?, ?)",  argv)
        elif tableName == "ds2Similarity":
            self.query("INSERT INTO ds2Similarity(ds1, ds2) VALUES (?, ?)",  argv)
        elif tableName == "ds1Data":
            self.query("INSERT INTO ds1Data(fileId, data) VALUES (?, ?)",  argv)
        elif tableName == "ds2Data":
            self.query("INSERT INTO ds2Data(fileId, data) VALUES (?, ?)",  argv)

    """
    Method receives query and returns data
    Parameters:
        query: sql query to process
    """
    def receive(self, query):
        self._db_cur.execute(query,)
        return self.fetchAll()

    """
    Method fetch one
    """
    def fetchOne(self):
        return self._db_cur.fetchone()

    """
    Method fetchall
    """
    def fetchAll(self):
        return self._db_cur.fetchall()

    """
    Method commits
    """
    def commit(self):
        return self._db_connection.commit()

    """
    Mehod close cursor and database connection
    """
    def __del__(self):
        self._db_cur.close()
        self._db_connection.close()