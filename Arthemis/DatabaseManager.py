"""
Database Manager Module
"""
import MySQLdb
import ResourceProvider

RESOURCE_PROVIDER = ResourceProvider.ResourceProvider()

class DatabaseManager(object):
    """
    Database Manager Class
    """
    def __init__(self):
        self.__database_name = RESOURCE_PROVIDER.get_string_table(RESOURCE_PROVIDER.DATABASE_NAME)
        self.__db_connection = None
        self.__cursor = None
        self.create_tables()

    def __connect(self):
        """
        Connect to DB
        """
        server = 'localhost'
        self.__db_connection = MySQLdb.connect(server, "root", "internet12", self.__database_name)
        self.__cursor = self.__db_connection.cursor()

    def __disconnect(self):
        """
        Disconect from DB
        """
        self.__db_connection.close()

    def create_tables(self):
        """
        Create tables needed for the main application
        """
        self.__connect()
        try:
            self.__cursor = self.__db_connection.cursor()
            sql_command = """CREATE TABLE IF NOT EXISTS HOME_SCANNER_DATABASE_TEMPERATURE
                (ID              INT            NOT NULL AUTO_INCREMENT,
                VALUE            DOUBLE         NOT NULL,
                TIME_COLLECTED   DATETIME       NOT NULL,
                PRIMARY KEY (ID));"""
            self.__cursor.execute(sql_command)

            sql_command = """CREATE TABLE IF NOT EXISTS HOME_SCANNER_DATABASE_GAS_RECORD
                (ID              INT            NOT NULL AUTO_INCREMENT,
                VALUE            DOUBLE         NOT NULL,
                TIME_COLLECTED   DATETIME       NOT NULL,
                PRIMARY KEY (ID));"""
            self.__cursor.execute(sql_command)

            sql_command = """CREATE TABLE IF NOT EXISTS HOME_SCANNER_DATABASE_LIGHT
                (ID              INT            NOT NULL AUTO_INCREMENT,
                VALUE            INT            NOT NULL,
                TIME_COLLECTED   DATETIME       NOT NULL,
                PRIMARY KEY (ID));"""
            self.__cursor.execute(sql_command)

            sql_command = """CREATE TABLE IF NOT EXISTS HOME_SCANNER_DATABASE_HUMIDITY
                (ID              INT            NOT NULL AUTO_INCREMENT,
                VALUE            DOUBLE         NOT NULL,
                TIME_COLLECTED   DATETIME       NOT NULL,
                PRIMARY KEY (ID));"""
            self.__cursor.execute(sql_command)

            sql_command = """CREATE TABLE IF NOT EXISTS HOME_SCANNER_DATABASE_MOTION
                (ID              INT            NOT NULL AUTO_INCREMENT,
                VALUE            INT            NOT NULL,
                TIME_COLLECTED   DATETIME       NOT NULL,
                PRIMARY KEY (ID));"""
            self.__cursor.execute(sql_command)

            sql_command = """CREATE TABLE IF NOT EXISTS HOME_SCANNER_DATABASE_DISTANCE
                (ID              INT            NOT NULL AUTO_INCREMENT,
                VALUE            DOUBLE         NOT NULL,
                TIME_COLLECTED   DATETIME       NOT NULL,
                PRIMARY KEY (ID));"""
            self.__cursor.execute(sql_command)
            sql_command = """CREATE TABLE IF NOT EXISTS HOME_SCANNER_DATABASE_DISTANCE
                (ID                         INT             NOT NULL AUTO_INCREMENT,
                TEMPERATURE_THRESHOLD       INT             NOT NULL,
                HUMIDITY_THRESHOLD          INT             NOT NULL,
                FACE_DETECTION              INT             NOT NULL,
                MOTION_DETECTION            INT             NOT NULL,
                HUMAN_DETECTION             INT             NOT NULL,
                PRIMARY KEY (ID));"""
            self.__cursor.execute(sql_command)
        except MemoryError as ex:
            self.__db_connection.rollback()
            print ex
            return 0
        self.__disconnect()

    def insert_data_in_database(self, values_list, table_name):
        """
        Insert one specific data in DB
        """
        self.__connect()
        try:
            if None in values_list:
                return
            var_string = ', '.join(['%s'] * len(values_list))
            insert_string = "INSERT INTO %s (value, time_collected) VALUES (%s);"
            query_string = insert_string % (table_name, var_string)
            self.__cursor.execute(query_string, values_list)
            self.__db_connection.commit()
        except TypeError as terr:
            print terr
            self.__db_connection.rollback()
        self.__disconnect()

    def get_data_from_database(self, table_name):
        """
        Return a list with all records store in a specified table
        """
        self.__connect()
        self.__cursor = self.__db_connection.cursor()
        query_string = 'SELECT * FROM %s' % table_name
        self.__cursor.execute(query_string)
        values_list = self.__cursor.fetchall()
        self.__disconnect()
        return values_list
