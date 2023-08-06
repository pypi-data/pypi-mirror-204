from oracle_utils import remote_oracle_db_connector
# from ui_management import dynamic_logger
import re
from tkinter import *
from ui_management import grid

g = grid.Grid()


def take_db_snapshot(root,server,username,password,port,sid,when_to_take,how_much_to_wait):
    logger = []

    def run_snap_query():
        try:
            # query = "exec dbms_workload_repository.create_snapshot"
            query = """
                    begin
                        dbms_output.put_line(dbms_workload_repository.create_snapshot);
                    end;
                    """
            rs = remote_oracle_db_connector.execute_query("plsql",query,server,username,password,port,sid)
            rs = rs[0][0]

            # is_success = [each_item for each_item in rs if "successfully completed" in each_item]

            if re.search("\d{5}",rs):
                logger.append("Successfully created the snapshot, fetching the snap id")
                try:
                    query = "select snap_id, snap_level, to_char(begin_interval_time, 'dd/mm/yy hh24:mi:ss') begin from dba_hist_snapshot order by 1 desc fetch first 1 rows only"
                    rs = remote_oracle_db_connector.execute_query("sql",query,server,username,password,port,sid)
                    rs = list(rs[0])
                    logger.append("Snap ID {} was generated on {}".format(rs[0],rs[2]))
                    return rs[0], rs[2], logger
                
                except Exception as e:
                    logger.append(e)
                    logger.append("Failed to fetch the snap id")
                    return "Error","Error",logger
                
            else:
                logger.append("Failed to generate a snap:")
                logger.append(rs)
                return "Error", "Error", logger

        except Exception as e:
            logger.append(e)
            logger.append("Failed to create AWR snapshot")
            return "Error","Error",logger


    snap_id, snap_time, logger = run_snap_query()
    return snap_id, snap_time, logger
    
            

def generate_awr(root,server_detail,username,password,port,sid,begin_snap,end_snap,filepath):
    logger = []
    awr_array = []
    try:
        awr = remote_oracle_db_connector.generate_awr(server_detail,username,password,port,sid,begin_snap,end_snap)
        
        for i in range(len(awr)):
            awr_array.append(awr[i][0])

        with open(filepath,'a') as file_handler:
            for each_row in awr_array:
                file_handler.write(str(each_row))

        return filepath,logger
    
    except Exception as e:
        print(e)
        return "error",["error"]
    