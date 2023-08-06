#takes in IDs at once, returns a a list of list with details.
#query
#SELECT ID, NAME, SERVER_IP, USER_NAME, AUTH_METHOD, KEY_FILE_LOCATION, PASSWORD FROM SERVERS WHERE ID IN ();
from internal_db_management import db_ops as db
from internal_db_management.pwd_handler import PasswordHandler

class GetServerDetails():
    def get_server_details(server_list,table_name):
        if table_name == "SERVERS":
            query = ""
            if(len(server_list)==1):
                query = "SELECT ID, NAME, SERVER_IP, USER_NAME, AUTH_METHOD, KEY_FILE_LOCATION, PASSWORD FROM SERVERS WHERE ID IN ("+server_list[0]+");"
            else:
                id_tuple = tuple(server_list)
                query = "SELECT ID, NAME, SERVER_IP, USER_NAME, AUTH_METHOD, KEY_FILE_LOCATION, PASSWORD FROM SERVERS WHERE ID IN "+str(id_tuple)+";"

        
        elif table_name == "VMSTAT":
            query = ""
            if(len(server_list)==1):
                query = """SELECT
                            S.ID, S.NAME, S.SERVER_IP, S.USER_NAME, S.AUTH_METHOD, S.KEY_FILE_LOCATION, S.PASSWORD, V.COMMON_NAME
                            FROM
                            SERVERS S, VMSTAT V WHERE
                            S.ID = V.SERVER AND
                            V.ID IN ({});
                        """.format(server_list[0])
            else:
                id_tuple = tuple(server_list)
                query = """SELECT
                            S.ID, S.NAME, S.SERVER_IP, S.USER_NAME, S.AUTH_METHOD, S.KEY_FILE_LOCATION, S.PASSWORD, V.COMMON_NAME
                            FROM
                            SERVERS S, VMSTAT V WHERE
                            S.ID = V.SERVER AND
                            V.ID IN {};
                        """.format(str(id_tuple))
                
        elif table_name == "GEN_AWR":
            id_tuple = tuple(server_list)
            query = """
                SELECT S.ID, S.NAME, S.SERVER_IP, S.USER_NAME, S.AUTH_METHOD, S.KEY_FILE_LOCATION, S.PASSWORD, A.SNAP_ID
                FROM 
                SERVERS S, AWR A WHERE
                A.SERVER_ID = S.ID AND
                A.ID IN {}
            """.format(str(id_tuple))

        rs = db.query_executor(query)
        rs_list = list(rs.fetchall())
        for each_server_list in range(len(rs_list)):
            rs_list[each_server_list] = list(rs_list[each_server_list])
            if rs_list[each_server_list][4] == 'Password':
                rs_list[each_server_list][6] = PasswordHandler.decrypt_password(rs_list[each_server_list][6])

        return rs_list


