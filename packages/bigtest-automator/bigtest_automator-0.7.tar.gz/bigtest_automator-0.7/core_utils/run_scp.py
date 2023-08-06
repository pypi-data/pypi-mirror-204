from tkinter import *
from ui_management import grid, dynamic_logger
from internal_db_management import db_ops
from internal_db_management.get_server_details import GetServerDetails
import paramiko
import tkinter.messagebox as mb
import concurrent.futures as cf
import tkinter.scrolledtext as st
from tkinter import filedialog as f
from scp import SCPClient

import os
g = grid.Grid()


class RunSCP():
    destination = ""
    def __init__(self,root,scp_server_list) -> None:

        def submit_destination():
            ExecuteSCPCommand(root,full_server_detail)

        def get_keyfile():
            dest = f.askdirectory(title = "Select a Destination")
            RunSCP.destination = os.path.abspath(dest)
            file_dialog_button.destroy()
            keyfileLabel.destroy()
            Label(root,text="File chosen:"+RunSCP.destination).grid(row=g.get_next_row(),column=0)
            Button(root,text="Continue",command=submit_destination).grid(row=g.get_next_row(),column=0)


        for item in root.winfo_children():
            item.destroy()
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1) 

        # Label(root, text="Collecting VMSTAT...", font=('calibre','15','bold')).grid(row=g.get_next_row(),column=0,columnspan=10)
        full_server_detail = GetServerDetails.get_server_details(scp_server_list,"VMSTAT")

        Label(root, text="Select Destination", font=('calibre','15','bold')).grid(row=g.get_next_row(),column=0,columnspan=10)
        Label(root,text="Select a common destination to store your files: ",pady=10).grid(row=g.get_next_row(),column=0)
        keyfileLabel = Label(root,text="Select the directory: ",pady=10)
        keyfileLabel.grid(row=g.get_next_row(),column=0)

        file_dialog_button = Button(root, text="Browse", command=get_keyfile)
        file_dialog_button.grid(row=g.get_next_row(),column=0)

        
class ExecuteSCPCommand():
    success = True
    failed_server = []

    def __init__(self,root,full_server_detail) -> None:

        for item in root.winfo_children():
            item.destroy()
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1) 

        def write_transaction_log(full_server_detail):
            for each_server in full_server_detail:
                COMMON_NAME = each_server[7]
                query = "DELETE FROM VMSTAT WHERE COMMON_NAME='{}'".format(COMMON_NAME)
                print(query)
                db_ops.query_executor(query)

        
        def exit_window():
            answer = mb.askyesno(title='Are you sure?', message="Are you sure that you want to exit? Possible transaction loss if you proceed when a transaction is in progress.")
            if answer:
                root.quit()

        logtext = st.ScrolledText(root, width = 75, height = 30, font = ("DejaVu Sans Mono",12))
        logtext.grid(row=g.get_next_row(),column=0,columnspan=10)
        dynamic_logger.Logger(root,logtext,"Getting the files...")
        Button(root,text="Exit",command=exit_window).grid(row=g.get_next_row(),column=1)
    
        def ssh_connect(each_server):
            logger = []
            ID, NAME, SERVER_IP, USER_NAME, AUTH_METHOD, KEY_FILE_LOCATION, PASSWORD, COMMON_NAME = each_server
            remote_source_file = "/tmp/"+COMMON_NAME+"*.txt"
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

                # ftpclient = client.open_sftp()
                # ftpclient.get(remote_source_file,RunSCP.destination+"/"+COMMON_NAME+"_"+SERVER_IP+".txt")

                with SCPClient(client.get_transport(), sanitize=lambda x: x) as scp:
                    scp.get(remote_path=remote_source_file, local_path=RunSCP.destination)

            except Exception as e:
                logger.append(e)
                logger.append("ERROR! Either failed to connect to {} ({}) or failed to get {} after connecting ".format(NAME,SERVER_IP,remote_source_file))
                ExecuteSCPCommand.success = False
                ExecuteSCPCommand.failed_server.append(NAME)

            finally:
                # ftpclient.close()
                client.close()
                return logger


        with cf.ThreadPoolExecutor() as executor:
            results = [executor.submit(ssh_connect,each_server) for each_server in full_server_detail]
            for f in cf.as_completed(results):
                for logs in range(len(f.result())):
                    dynamic_logger.Logger(root,logtext,str(f.result()[logs])+"\n")

        if(len(ExecuteSCPCommand.failed_server)>0 and len(full_server_detail)==len(ExecuteSCPCommand.failed_server)):
            dynamic_logger.Logger(root,logtext,"The command failed to run on all of the selected servers. Please try again.")
            server_id=[]
            [server_id.append(server[0]) for server in full_server_detail]
            
        elif(len(ExecuteSCPCommand.failed_server)>0):
            dynamic_logger.Logger(root,logtext,"Execution complete, but the command was failed to run on the following server(s):")
            for server in ExecuteSCPCommand.failed_server:
                dynamic_logger.Logger(root,logtext,server)

        else:
            dynamic_logger.Logger(root,logtext,"Execution completed successfully on all the selected servers, deleting entries from pending table.")
            write_transaction_log(full_server_detail)


# ftp_client=ssh_client.open_sftp()
# ftp_client.get(‘remotefileth’,’localfilepath’)
# ftp_client.close()