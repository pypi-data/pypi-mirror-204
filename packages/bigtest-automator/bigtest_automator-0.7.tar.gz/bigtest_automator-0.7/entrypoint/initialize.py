import os,sqlite3

def create_tables(db_file):

    create_servers_table = """
        CREATE TABLE IF NOT EXISTS SERVERS (
        ID integer PRIMARY KEY AUTOINCREMENT,
        NAME text NOT NULL,
        SERVER_IP text NOT NULL,
        USER_NAME text NOT NULL,
        AUTH_METHOD text NOT NULL,
        KEY_FILE_LOCATION text,
        PASSWORD text
    )
    """
    create_vmstat_table = """
        CREATE TABLE IF NOT EXISTS VMSTAT ( 
    	ID integer PRIMARY KEY AUTOINCREMENT,
    	EXECUTION_TIME text NOT NULL,
    	COMMON_NAME text NOT NULL,
    	COMMAND text NOT NULL,
    	SERVER text NOT NULL)
    """
    create_awr_table = """
        CREATE TABLE IF NOT EXISTS AWR ( 
        ID integer PRIMARY KEY AUTOINCREMENT, 
        SERVER_ID text NOT NULL, 
        SNAP_ID text NOT NULL, 
        SNAP_TIME text NOT NULL 
    )
    """
    try:
        con = sqlite3.connect(db_file,isolation_level=None)
        cursor = con.cursor()
        print("Creating table SERVERS")
        cursor.execute(create_servers_table)
        print("Creating table VMSTAT")
        cursor.execute(create_vmstat_table)
        print("Creating table AWR")
        cursor.execute(create_awr_table)
        con.commit()

    except Exception as e:
        print(e)
        print("Failed to execute DDLs")

    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()

def initialize_db():
    if not os.path.exists(os.path.join(os.getcwd(),"bigtest_automator","serverdb.db")):
        os.mkdir(os.path.join(os.getcwd(),"bigtest_automator"))
        db_file = os.path.join(os.getcwd(),"bigtest_automator","serverdb.db")
        print("Creating database file: "+db_file)
        with open(db_file, 'w') as fp:
            pass
        create_tables(db_file)

