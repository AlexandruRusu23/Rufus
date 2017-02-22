import sqlite3
"""
Database manipulation
"""

def main():
    """
    database test function
    """
    conn = sqlite3.connect('test.db')

    print "Opened database successfully"

    conn.execute('''CREATE TABLE IF NOT EXISTS HOME_SCANNER_DATABASE
        (ID              INTEGER     PRIMARY KEY AUTOINCREMENT        NOT NULL,
        MQ2_1            INTEGER     NOT NULL,
        MQ2_2            INTEGER     NOT NULL,
        LIGHT_1          INTEGER     NOT NULL,
        LIGHT_2          INTEGER     NOT NULL,
        TEMPERATURE      REAL        NOT NULL,
        HUMIDITY         INTEGER     NOT NULL,
        MOTION           INTEGER     NOT NULL,
        DISTANCE         REAL        NOT NULL,
        TIME_COLLECTED   DATE        NOT NULL
        );''')

    print "Table created successfully"

    conn.execute("INSERT INTO HOME_SCANNER_DATABASE (MQ2_1,MQ2_2,LIGHT_1,LIGHT_2,\
        TEMPERATURE,HUMIDITY,MOTION,DISTANCE,TIME_COLLECTED) \
        VALUES (432, 120, 320, 32, 132, 233, 0, 13, '2017-02-22')")

    conn.commit()

    conn.close()

if __name__ == '__main__':
    main()
