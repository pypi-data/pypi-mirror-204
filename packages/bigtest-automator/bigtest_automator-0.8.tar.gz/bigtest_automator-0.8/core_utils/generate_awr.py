from tkinter import *
from tkinter import messagebox
import tkinter.messagebox as mb
import tkinter.scrolledtext as st
from tkinter import filedialog as f
import os
from ui_management import dynamic_logger
from internal_db_management import db_ops
from internal_db_management import get_server_details
from oracle_utils import oracle_awr
from ui_management import grid

g = grid.Grid()

class GenerateAWR:
    destination = ""
    full_file_name = ""

    def __init__(self,root,snap_list) -> None:

        for item in root.winfo_children():
            item.destroy()
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)


        def get_keyfile():
            if len(filename_entry.get()) < 5 or str(filename_entry.get()).isdigit():
                messagebox.showerror("Error",message="Enter a valid filename with at least 5 alphanumerical characters")
            else:
                dest = f.askdirectory(title = "Select a Destination")
                full_file_path = os.path.abspath(dest)
                GenerateAWR.full_file_name = os.path.join(full_file_path,filename_entry.get()+".html")
                file_dialog_button.destroy()
                keyfileLabel.destroy()
                Label(root,text="File chosen:"+GenerateAWR.full_file_name).grid(row=file_chosen_row,column=1)

        Label(root, text="Generate an AWR", font=('calibre','15','bold')).grid(row=g.get_next_row(),column=0,columnspan=10)
        Label(root, text="DB Connection Details", font=('calibre','15','bold')).grid(row=g.get_next_row(),column=0,columnspan=10)
        Label(root, text="Enter the following details to connect to the DB", font=('calibre','13','bold')).grid(row=g.get_next_row(),column=0,columnspan=10)
        g.get_blank_lines(root,1)


        db_user_grid_row = g.get_next_row()
        db_pass_grid_row = g.get_next_row()
        db_port_grid_row = g.get_next_row()
        db_sid_grid_row = g.get_next_row()
        file_name_row = g.get_next_row()
        directory_row = g.get_next_row()
        file_chosen_row = g.get_next_row()


        Label(root,text="Database username: ",pady=10).grid(row=db_user_grid_row,column=0,sticky="w")
        Label(root,text="Database password: ",pady=10).grid(row=db_pass_grid_row,column=0,sticky="w")
        Label(root,text="Port: ",pady=10).grid(row=db_port_grid_row,column=0,sticky="w")
        Label(root,text="SID: ",pady=10).grid(row=db_sid_grid_row,column=0,sticky="w")
        Label(root,text="Provide a valid filename for your report. DO NOT APPEND .HTML: ",pady=10).grid(row=file_name_row,column=0)
        filename_entry = Entry(root,width=40,borderwidth=2)
        filename_entry.grid(row=file_name_row,column=1)
        keyfileLabel = Label(root,text="Select the target directory to store the report: ",pady=10)
        keyfileLabel.grid(row=directory_row,column=0)
        file_dialog_button = Button(root, text="Browse", command=get_keyfile)
        file_dialog_button.grid(row=directory_row,column=1)


        username_entry = Entry(root,width=40,borderwidth=2)
        username_entry.grid(row=db_user_grid_row,column=1,padx=10,pady=10)
        password_entry = Entry(root,show='*',width=40,borderwidth=2)
        password_entry.grid(row=db_pass_grid_row,column=1,padx=10,pady=10)
        port_entry = Entry(root,width=40,borderwidth=2)
        port_entry.grid(row=db_port_grid_row,column=1,padx=10,pady=10)
        sid_entry = Entry(root,width=40,borderwidth=2)
        sid_entry.grid(row=db_sid_grid_row,column=1,padx=10,pady=10)


        def submit_info():
            username = username_entry.get()
            password = password_entry.get()
            port = port_entry.get()
            sid = sid_entry.get()

            if not port.isdigit():
                messagebox.showerror("Error", message="Please check your input. Port must be a number")
            elif(' ' in username or ' ' in password or ' ' in sid):
                messagebox.showerror("Error", message="Please enter valid values")
            elif(len(username) < 1 or len(password) < 1  or len(sid) < 1 ):
                messagebox.showerror("Error", message="Please enter valid values")
            else:
                full_server_detail = get_server_details.GetServerDetails.get_server_details(snap_list,"GEN_AWR")
                if(full_server_detail[0][0] != full_server_detail[1][0]):
                    messagebox.showerror("Error",message="The begin and end snap ID are not from the same database!")
                else:

                    def write_transaction_log():
                        query = "DELETE FROM AWR WHERE SNAP_ID IN ('{}','{}')".format(full_server_detail[0][7],full_server_detail[1][7])
                        db_ops.query_executor(query)

                    def exit_window():
                        answer = mb.askyesno(title='Are you sure?', message="Are you sure that you want to exit? Possible transaction loss if you proceed when a transaction is in progress.")
                        if answer:
                            root.quit()

                    for item in root.winfo_children():
                        item.destroy()

                    root.rowconfigure(0, weight=1)
                    root.columnconfigure(0, weight=1) 

                    Label(root, text="Generating the AWR...", font=('calibre','15','bold')).grid(row=g.get_next_row(),column=0,columnspan=10)
                    logtext = st.ScrolledText(root, width = 75, height = 30, font = ("DejaVu Sans Mono",12))
                    logtext.grid(row=g.get_next_row(),column=0,columnspan=10)
                    dynamic_logger.Logger(root,logtext,"Running the command...")
                    Button(root,text="Exit",command=exit_window).grid(row=g.get_next_row(),column=1)

                    print(full_server_detail[0], username, password, port, sid,full_server_detail[0][7],full_server_detail[1][7],GenerateAWR.full_file_name)
                    outfile, logger = oracle_awr.generate_awr(root, full_server_detail[0][2], username, password, port, sid,full_server_detail[0][7],full_server_detail[1][7],GenerateAWR.full_file_name)

                    if outfile == "error":
                        dynamic_logger.Logger(root,logtext,"Could not generate the AWR report")
                        for log in logger:
                            dynamic_logger.Logger(root,logtext,log)
                    
                    else:
                        for log in logger:
                            dynamic_logger.Logger(root,logtext,log)
                        dynamic_logger.Logger(root,logtext,"Successfully generated the AWR at:"+outfile)
                        dynamic_logger.Logger(root,logtext,"These snaps have been erased from the local table")
                        write_transaction_log()

        button_grid_row = g.get_next_row()
        Button(root,text="Submit",command=submit_info).grid(row=button_grid_row,column=0)
        Button(root,text="Exit",command=root.quit).grid(row=button_grid_row,column=1)