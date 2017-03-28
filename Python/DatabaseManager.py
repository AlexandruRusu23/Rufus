"""
Database Manager Module
"""
import MySQLdb

class DatabaseManager(object):
    """
    Database Manager Class
    """
    def __init__(self, database_name):
        self._database_name = database_name
        server = 'localhost'
        self._db_connection = MySQLdb.connect(server, "root", "internet12", self._database_name)
        self._cursor = self._db_connection.cursor()
        self.create_table()

    def connect(self):
        """
        Connect to DB
        """
        server = 'localhost'
        self._db_connection = MySQLdb.connect(server, "root", "internet12", self._database_name)

    def disconnect(self):
        """
        Disconect from DB
        """
        self._db_connection.close()

    def create_table(self):
        """
        Create tables needed for the main application
        """
        self.connect()
        try:
            self._cursor = self._db_connection.cursor()
            sql_command = """CREATE TABLE IF NOT EXISTS HOME_SCANNER_DATABASE_TEMPERATURE
                (ID              INT            NOT NULL AUTO_INCREMENT,
                VALUE            DOUBLE         NOT NULL,
                TIME_COLLECTED   DATETIME       NOT NULL,
                PRIMARY KEY (ID));"""
            self._cursor.execute(sql_command)

            sql_command = """CREATE TABLE IF NOT EXISTS HOME_SCANNER_DATABASE_GAS_RECORD
                (ID              INT            NOT NULL AUTO_INCREMENT,
                VALUE            DOUBLE         NOT NULL,
                TIME_COLLECTED   DATETIME       NOT NULL,
                PRIMARY KEY (ID));"""
            self._cursor.execute(sql_command)

            sql_command = """CREATE TABLE IF NOT EXISTS HOME_SCANNER_DATABASE_LIGHT
                (ID              INT            NOT NULL AUTO_INCREMENT,
                VALUE            INT            NOT NULL,
                TIME_COLLECTED   DATETIME       NOT NULL,
                PRIMARY KEY (ID));"""
            self._cursor.execute(sql_command)

            sql_command = """CREATE TABLE IF NOT EXISTS HOME_SCANNER_DATABASE_HUMIDITY
                (ID              INT            NOT NULL AUTO_INCREMENT,
                VALUE            DOUBLE         NOT NULL,
                TIME_COLLECTED   DATETIME       NOT NULL,
                PRIMARY KEY (ID));"""
            self._cursor.execute(sql_command)

            sql_command = """CREATE TABLE IF NOT EXISTS HOME_SCANNER_DATABASE_MOTION
                (ID              INT            NOT NULL AUTO_INCREMENT,
                VALUE            INT            NOT NULL,
                TIME_COLLECTED   DATETIME       NOT NULL,
                PRIMARY KEY (ID));"""
            self._cursor.execute(sql_command)

            sql_command = """CREATE TABLE IF NOT EXISTS HOME_SCANNER_DATABASE_DISTANCE
                (ID              INT            NOT NULL AUTO_INCREMENT,
                VALUE            DOUBLE         NOT NULL,
                TIME_COLLECTED   DATETIME       NOT NULL,
                PRIMARY KEY (ID));"""
            self._cursor.execute(sql_command)
        except MemoryError as ex:
            self._db_connection.rollback()
            print ex
            return 0
        self._db_connection.close()

    def insert_data_in_database(self, values_list, table_name):
        """
        Insert one specific data in DB
        """
        self.connect()
        try:
            if None in values_list:
                return
            var_string = ', '.join(['%s'] * len(values_list))
            insert_string = "INSERT INTO %s (value, time_collected) VALUES (%s);"
            query_string = insert_string % (table_name, var_string)
            self._cursor.execute(query_string, values_list)
            self._db_connection.commit()
        except TypeError as terr:
            print terr
            self._db_connection.rollback()
        self._db_connection.close()

    def get_data_from_database(self, table_name):
        """
        Return a list with all records store in a specified table
        """
        self.connect()
        self._cursor = self._db_connection.cursor()
        query_string = 'SELECT * FROM %s' % table_name
        self._cursor.execute(query_string)
        values_list = self._cursor.fetchall()
        self._db_connection.close()
        return values_list
