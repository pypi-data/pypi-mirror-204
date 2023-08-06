import sqlite3,os
 
def connect_to_db():
    db_location = os.path.join(os.getcwd(),"bigtest_automator", "serverdb.db")

    try:
        con = sqlite3.connect(db_location,isolation_level=None)
        if con is not None:
            return con.cursor(), con
        else:
            raise ValueError("Could not establish a DB connection by using the DB file "+db_location)
    except sqlite3.Error as e:
        print(e)

def query_executor(query):
    #Get connection cursor
    cursor,con = connect_to_db()

    if cursor is not None:
        try:
            result_set = cursor.execute(query)
            con.commit()
            return result_set

        except sqlite3.Error as e:
            print(e)
            raise ValueError("Error in executing the Query")
     
    else:
        raise ValueError("Could not get a connection object from the DB")

def main_table_creator():
    main_table_query = """
    CREATE TABLE IF NOT EXISTS SERVERS (
        ID integer PRIMARY KEY AUTOINCREMENT,
        NAME text NOT NULL,
        SERVER_IP text NOT NULL,
        USER_NAME text NOT NULL,
        AUTH_METHOD text NOT NULL,
        KEY_FILE_LOCATION text,
        PASSWORD text
    );"""

    query_executor(main_table_query)
