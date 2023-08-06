from tkinter import *
from tkinter import messagebox
from datetime import datetime,timedelta
import time,math
import tkinter.messagebox as mb
import tkinter.scrolledtext as st
from ui_management import dynamic_logger,grid
from internal_db_management import db_ops, get_server_details
from oracle_utils import oracle_awr

g = grid.Grid()


class TakeSnapshot():
    success = True
    failed_server = []
    logger = []
    snap_id = ""
    snap_time = ""

    def __init__(self,root,server_list,when_to_take,how_much_to_wait):

        for item in root.winfo_children():
            item.destroy()
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        Label(root, text="Take DB snapshot", font=('calibre','15','bold')).grid(row=g.get_next_row(),column=0,columnspan=10)
        Label(root, text="DB Connection Details", font=('calibre','15','bold')).grid(row=g.get_next_row(),column=0,columnspan=10)
        Label(root, text="Enter the following details to connect to the DB", font=('calibre','13','bold')).grid(row=g.get_next_row(),column=0,columnspan=10)
        message = """
            Note - Note - Multiple selections are not supported in this feature!
            """

        Label(root, text=message, font=('calibre','13')).grid(row=g.get_next_row(),column=0,columnspan=10)

        g.get_blank_lines(root,1)


        db_user_grid_row = g.get_next_row()
        db_pass_grid_row = g.get_next_row()
        db_port_grid_row = g.get_next_row()
        db_sid_grid_row = g.get_next_row()


        Label(root,text="Database username: ",pady=10).grid(row=db_user_grid_row,column=0,sticky="w")
        Label(root,text="Database password: ",pady=10).grid(row=db_pass_grid_row,column=0,sticky="w")
        Label(root,text="Port: ",pady=10).grid(row=db_port_grid_row,column=0,sticky="w")
        Label(root,text="SID: ",pady=10).grid(row=db_sid_grid_row,column=0,sticky="w")


        username_entry = Entry(root,width=40,borderwidth=2)
        username_entry.grid(row=db_user_grid_row,column=1,padx=10,pady=10)
        password_entry = Entry(root,show='*',width=40,borderwidth=2)
        password_entry.grid(row=db_pass_grid_row,column=1,padx=10,pady=10)
        port_entry = Entry(root,width=40,borderwidth=2)
        port_entry.grid(row=db_port_grid_row,column=1,padx=10,pady=10)
        sid_entry = Entry(root,width=40,borderwidth=2)
        sid_entry.grid(row=db_sid_grid_row,column=1,padx=10,pady=10)

        def submit_info():
            if not port_entry.get().isdigit():
                messagebox.showerror("Error","Please check your input. Port must be a number")
            elif(' ' in username_entry.get() or ' ' in password_entry.get() or ' ' in sid_entry.get()):
                messagebox.showerror("Error","Please enter valid values")
            elif(len(username_entry.get()) < 1 or len(password_entry.get()) < 1  or len(sid_entry.get()) < 1 ):
                messagebox.showerror("Error","Please enter valid values")
            else:
                full_server_detail = get_server_details.GetServerDetails.get_server_details(server_list,"SERVERS")
                TakeSnapshot.get_db_snapshot(root,full_server_detail,username_entry.get(), password_entry.get(), port_entry.get(), sid_entry.get(),when_to_take,how_much_to_wait)
                
        button_grid_row = g.get_next_row()
        Button(root,text="Submit",command=submit_info).grid(row=button_grid_row,column=0)
        Button(root,text="Exit",command=root.quit).grid(row=button_grid_row,column=1)
    

    def get_db_snapshot(root,server_list,db_username,db_password,db_port,db_sid,when_to_take,how_much_to_wait):

        server_ip = []
        for each_server in server_list:
            server_ip.append(each_server[2])

        def write_transaction_log(server_id_list):
            for server in server_id_list:
                query = "INSERT INTO AWR (SERVER_ID, SNAP_ID, SNAP_TIME) VALUES (\"{}\",\"{}\",\"{}\")".format(server,TakeSnapshot.snap_id,TakeSnapshot.snap_time)
                try:
                    db_ops.query_executor(query)
                except Exception as e:
                    print("Failed to write to the DB")
                    print(e)

        def exit_window():
            answer = mb.askyesno(title='Are you sure?', message="Are you sure that you want to exit? Possible transaction loss if you proceed when a transaction is in progress.")
            if answer:
                root.quit()

        for item in root.winfo_children():
            item.destroy()

        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1) 

        Label(root, text="Taking a snapshot...", font=('calibre','15','bold')).grid(row=g.get_next_row(),column=0,columnspan=10)
        logtext = st.ScrolledText(root, width = 75, height = 30, font = ("DejaVu Sans Mono",12))
        logtext.grid(row=g.get_next_row(),column=0,columnspan=10)
        dynamic_logger.Logger(root,logtext,"Running the command...")
        Button(root,text="Exit",command=exit_window).grid(row=g.get_next_row(),column=1)

        def run_snapshot(each_server,when_to_take,how_much_to_wait):

            if when_to_take == "now":
                TakeSnapshot.snap_id, TakeSnapshot.snap_time, TakeSnapshot.logger = oracle_awr.take_db_snapshot(root,each_server,db_username,db_password,db_port,db_sid,when_to_take,how_much_to_wait)

                if TakeSnapshot.snap_id == "Error" or TakeSnapshot.snap_time == "Error":
                    TakeSnapshot.success = False
                    TakeSnapshot.failed_server.append(each_server)
                return TakeSnapshot.logger
            
            else:

                current_time = datetime.now()
                target_time = current_time + timedelta(minutes=int(how_much_to_wait))

                while(current_time < target_time):
                    time.sleep(30)
                    current_time = datetime.now()
                    dynamic_logger.Logger(root,logtext,"Waiting for {} more hours...".format(target_time-current_time))

                    # TakeSnapshot.logger.append("Waiting for {} more minutes...".format(target_time-current_time))
                TakeSnapshot.logger.append(run_snapshot(each_server,"now",0))
                return TakeSnapshot.logger
            
        for each_server in server_ip:
            logger = run_snapshot(each_server,when_to_take,how_much_to_wait)
            for each_line in logger:
                dynamic_logger.Logger(root,logtext,each_line)

        # with cf.ThreadPoolExecutor() as executor:
        #     results = [executor.submit(run_snapshot,each_server,when_to_take,how_much_to_wait) for each_server in server_ip]
        #     for f in cf.as_completed(results):
        #         for logs in range(len(f.result())):
        #             dynamic_logger.Logger(root,logtext,str(f.result()[logs])+"\n")

        if(len(TakeSnapshot.failed_server)>0 and len(server_ip)==len(TakeSnapshot.failed_server)):
            dynamic_logger.Logger(root,logtext,"Failed to generate snapshot on all of the seclected servers. This transaction will not be stored to the database.")
            server_id=[]
            [server_id.append(server[0]) for server in server_list]
            
        elif(len(TakeSnapshot.failed_server)>0):
            dynamic_logger.Logger(root,logtext,"Execution complete, but the snapshot was failed to create on the following server(s):")
            for server in TakeSnapshot.failed_server:
                dynamic_logger.Logger(root,logtext,server)

        else:
            dynamic_logger.Logger(root,logtext,"Snapshot was created successfully on all the selected servers")
            server_id=[]
            [server_id.append(server[0]) for server in server_list]
            write_transaction_log(server_id)
       