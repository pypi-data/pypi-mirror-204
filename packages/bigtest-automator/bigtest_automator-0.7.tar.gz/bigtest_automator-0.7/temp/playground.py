import remote_oracle_db_connector, oracledb,ast

host = "34.194.224.7"
username = "baninst1"
password = "u_pick_it"
sid = "DPD8"
port = 8000
begin_snap = "36879"
end_snap = "36880"
filepath = "/tmp"

try:

    params = oracledb.ConnectParams(host=host, port=port, service_name=sid)
    connection = oracledb.connect(user=username, password=password, params=params)
    cursor = connection.cursor()
    cursor.arraysize = 10000
    # rs = remote_oracle_db_connector.execute_query("select snap_id, snap_level, to_char(begin_interval_time, 'dd/mm/yy hh24:mi:ss') from dba_hist_snapshot order by 1 desc fetch first 1 rows only",host,username,password,port,sid)
    # query = "dbms_output.put_line(exec dbms_workload_repository.create_snapshot);"

    # query = """
    #     begin
    #         dbms_output.put_line(dbms_workload_repository.create_snapshot);
    #     end;
    # """

    # rs = remote_oracle_db_connector.execute_query("sql","SELECT DBID FROM V$DATABASE",host,username,password,port,sid)
    rs = cursor.execute("SELECT DBID FROM V$DATABASE")
    result_set = []
    for row in rs:
        result_set.append(row)
    db_id = result_set[0][0]
    query = """
            SELECT output FROM TABLE
            (dbms_workload_repository.awr_report_html
                ({},{},{},{})
            )
            """.format(db_id,str(1),begin_snap,end_snap)
    # rs = remote_oracle_db_connector.execute_query("plsql",query,host,username,password,port,sid)
    cursor.execute(query)
    result = cursor.fetchall()

    mainarray = []

    for i in range(len(result)):
        mainarray.append(result[i][0])

    # print(mainarray)

    print(len(mainarray))

    with open("/Users/shantharamp/Downloads/adf.html","a") as f:
        for j in range(len(mainarray)):
            f.write(str(mainarray[j]))

    


    # print(rs)
except Exception as e:
    print(e)
    # raise ValueError("error while exeucing the query")



