import sqlite3
from sqlite3 import Error
import datetime 
 
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return conn
 
 
def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


 
def create_task(conn, data ):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """
 
    sql = ''' INSERT INTO gionjistar1( panel_voltage,
                                       panel_current,
                                       battery_voltage,
                                       battery_current,
                                       load_voltage,
                                       load_current,
                                       power_input,
                                       power_output,
                                       output_current_plug_1,
                                       output_current_plug_2,
                                       inverter_current,
                                       irradiation,
                                       time
                                      )
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, data)
    return cur.lastrowid


def select_data(conn, start, end):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM gionjistar1 WHERE time >= ? AND time <= ?", (start, end))
 
    rows = cur.fetchall()
 
    for row in rows:
        print(row)


 
def main():
    database = r"./sqlite.db"
 
    sql_create_gionji_table = """ CREATE TABLE IF NOT EXISTS gionjistar1 (
                                        id integer PRIMARY KEY,
                                        panel_voltage         real,
                                        panel_current         real,
                                        battery_voltage       real,
                                        battery_current       real,
                                        load_voltage          real,
                                        load_current          real,
                                        power_input           real,
                                        power_output          real,
                                        output_current_plug_1 real,
                                        output_current_plug_2 real,
                                        inverter_current      real,
                                        irradiation           real,
                                        time                  timestamp NOT NULL
                                    ); """
 
    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_gionji_table)
    else:
        print("Error! cannot create the database connection.")

    data = (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, datetime.datetime.now() )

    create_task(conn, data )




if __name__ == '__main__':
    main()
