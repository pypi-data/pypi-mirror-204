from tkinter import *
from ui_management import grid, dynamic_logger
from internal_db_management import db_ops
from internal_db_management.get_server_details import GetServerDetails
import paramiko
from datetime import datetime
import tkinter.messagebox as mb
import concurrent.futures as cf
import tkinter.scrolledtext as st

g = grid.Grid()


class RunVmstat:
    def __init__(self,root,server_list,duration,frequency,name):
        for item in root.winfo_children():
            item.destroy()
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1) 
        Label(root, text="Running VMSTAT...", font=('calibre','15','bold')).grid(row=g.get_next_row(),column=0,columnspan=10)

        full_server_detail = GetServerDetails.get_server_details(server_list,"SERVERS")

        vmstat_command = "vmstat -n "+str(frequency)+" "+str(duration)+" -t>/tmp/"+name+"_"+str(duration)+"s_"+datetime.today().strftime('%Y_%m_%d_%H_%M_%S')+"_$HOSTNAME.txt &"
        ExecuteCommands(root,full_server_detail,vmstat_command,name)


class ExecuteCommands():
    success = True
    failed_server = []

    def __init__(self,root,list_of_servers,command,common_name) -> None:

        def write_transaction_log(time,common_name,command,server_list):
            for server in server_list:
                query = "INSERT INTO VMSTAT (EXECUTION_TIME,COMMON_NAME,COMMAND,SERVER) VALUES(\"{}\",\"{}\",\"{}\",\"{}\");".format(str(time),common_name,command,server)
                db_ops.query_executor(query)

        
        def exit_window():
            answer = mb.askyesno(title='Are you sure?', message="Are you sure that you want to exit? Possible transaction loss if you proceed when a transaction is in progress.")
            if answer:
                root.quit()

        ExecuteCommands.root = root
        logtext = st.ScrolledText(root, width = 75, height = 30, font = ("DejaVu Sans Mono",12))
        logtext.grid(row=g.get_next_row(),column=0,columnspan=10)
        dynamic_logger.Logger(root,logtext,"Running the command...")
        Button(root,text="Exit",command=exit_window).grid(row=g.get_next_row(),column=1)
       
        def ssh_connect(each_server):
            logger = []
            ID, NAME, SERVER_IP, USER_NAME, AUTH_METHOD, KEY_FILE_LOCATION, PASSWORD = each_server
            try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                if AUTH_METHOD == 'Password':
                    client.connect(SERVER_IP, username=USER_NAME, password=PASSWORD,timeout=10)
                    logger.append("trying to connect to {} ({}) with {} and the password...".format(NAME,SERVER_IP,USER_NAME))
                else:
                    private_key = paramiko.RSAKey.from_private_key_file(KEY_FILE_LOCATION)
                    client.connect(SERVER_IP, username=USER_NAME, pkey=private_key,timeout=10)
                    logger.append("trying to connect to {} ({}) using {} and the keyfile...".format(NAME,SERVER_IP,KEY_FILE_LOCATION))

                stdin, stdout, stderr = client.exec_command(command)

                
                logger.append("Result of command {}:".format(command))
                logger.append(stdout.read())

            except Exception as e:
                logger.append(e)
                logger.append("ERROR! Either failed to connect to {} ({}) or failed to execute {} after connecting ".format(NAME,SERVER_IP,command))
                ExecuteCommands.success = False
                ExecuteCommands.failed_server.append(NAME)

            finally:
                client.close()
                return logger


        with cf.ThreadPoolExecutor() as executor:
            results = [executor.submit(ssh_connect,each_server) for each_server in list_of_servers]
            for f in cf.as_completed(results):
                for logs in range(len(f.result())):
                    dynamic_logger.Logger(root,logtext,str(f.result()[logs])+"\n")

        if(len(ExecuteCommands.failed_server)>0 and len(list_of_servers)==len(ExecuteCommands.failed_server)):
            dynamic_logger.Logger(root,logtext,"The command failed to run on all of the selected servers. This transaction will not be stored to the database.")
            server_id=[]
            [server_id.append(server[0]) for server in list_of_servers]
            
        elif(len(ExecuteCommands.failed_server)>0):
            dynamic_logger.Logger(root,logtext,"Execution complete, but the command was failed to run on the following server(s):")
            for server in ExecuteCommands.failed_server:
                dynamic_logger.Logger(root,logtext,server)

        else:
            dynamic_logger.Logger(root,logtext,"Execution completed successfully on all the selected servers")
            server_id=[]
            [server_id.append(server[0]) for server in list_of_servers]
            write_transaction_log(datetime.today().strftime('%Y_%m_%d_%H_%M_%S'),common_name,command,server_id)



