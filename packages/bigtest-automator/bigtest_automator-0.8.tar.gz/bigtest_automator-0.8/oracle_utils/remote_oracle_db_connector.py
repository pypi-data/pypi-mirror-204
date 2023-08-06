import oracledb

def connect_to_oracle_db(server,user,password,port,sid):
    try:
        print(server, user, password, port, sid)
        params = oracledb.ConnectParams(host=server, port=port, service_name=sid)
        connection = oracledb.connect(user=user, password=password, params=params)
        return connection, connection.cursor() 

    except Exception as e:
        print(e)
        raise ValueError("Error connecting to the database")

def execute_query(type,query,server,user,password,port,sid):
    connection= ""
    cursor = ""
    try:
        result_set = []
        
        connection, cursor = connect_to_oracle_db(server,user,password,port,sid)

        if type == "plsql":
            cursor.callproc("dbms_output.enable")
            chunk_size = 1000
            lines_var = cursor.arrayvar(str, chunk_size)
            num_lines_var = cursor.var(int)
            num_lines_var.setvalue(0, chunk_size)
            cursor.execute(query)
            while True:
                cursor.callproc("dbms_output.get_lines", (lines_var, num_lines_var))
                num_lines = num_lines_var.getvalue()
                lines = lines_var.getvalue()[:num_lines]
                result_set.append(lines)
                return result_set
        
        else:
            rs = cursor.execute(query)
            connection.commit()
            for row in rs:
                result_set.append(row)
            return result_set
    
    except Exception as e:
        print(e)
        raise ValueError("Error while executing the query")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def generate_awr(server,user,password,port,sid,begin_snap,end_snap):
    try:
        return_awr_report = ""

        connection, cursor = connect_to_oracle_db(server,user,password,port,sid)
        cursor.execute("SELECT DBID FROM V$DATABASE")
        db_id = cursor.fetchone()[0]

        query = """
                SELECT output FROM TABLE
                (dbms_workload_repository.awr_report_html
                    ({},{},{},{})
                )
                """.format(db_id,str(1),begin_snap,end_snap)
        
        cursor.execute(query)
        result = cursor.fetchall()

        return_awr_report = result
        
        return return_awr_report
    
    except Exception as e:
        print(e)
        raise ValueError("Error while generating the AWR report")
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()