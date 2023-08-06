from tkinter import *
from tkinter import ttk, messagebox
from tkinter import filedialog as f
import os,re
from internal_db_management import db_ops as db
from core_utils import run_vmstat as rv
from core_utils import run_scp as rscp
from internal_db_management.pwd_handler import PasswordHandler
from core_utils.take_awr_snapshot import TakeSnapshot
from core_utils.generate_awr import GenerateAWR
from ui_management import grid

g = grid.Grid() 

class ServerManagement:

    selected_servers = []
    selected_vmstat_servers = []
    type_of_auth = ""
    password = ""
    keyfile_location = ""
    action_item = ""

    def go_to_next_page(self,root,action_item):

        if(len(ServerManagement.selected_servers)==0):
            messagebox.showerror("Error!","You must select at least one server from the list to continue")
        
        else:
            # RecordActions(root,ServerManagement.selected_servers)
            InvokeActions(root,action_item)

    def exit_window(self,root):
        root.quit()

    def __init__(self,root,action_item):
        ServerManagement.action_item = action_item
        for item in root.winfo_children():
            item.destroy()
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        self.get_available_servers(root)
        next_button = Button(root,text="Next>",command=lambda:self.go_to_next_page(root,action_item))
        next_button.grid(row=300,column=3)
        exit_window = Button(root,text="Exit",command=lambda:self.exit_window(root))
        exit_window.grid(row=300,column=4)
            
    def record_selection(self,mylist):
        ServerManagement.selected_servers.clear()
        ServerManagement.selected_servers = mylist

    def get_available_servers(self,root):
        
        for item in root.winfo_children():
            item.destroy()

        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        Label(root, text="Sever Management", font=('calibre','15','bold')).grid(row=g.get_next_row(),column=0,columnspan=10)
        Label(root, text="Select the servers that you want to run the reports on:",font=('calibre','15','normal')).grid(row=g.get_next_row(),column=0,sticky="w")
        same_row = g.get_next_row()
        add_button = Button(root,text="Add a Server", command=lambda:self.add_a_server(root)).grid(row=same_row,column=1)
        remove_button = Button(root,text="Delete a Server", command=self.delete_a_server).grid(row=same_row,column=2)
        refresh_button = Button(root,text="Refresh", command=lambda:self.refresh(root)).grid(row=same_row,column=3)

        def getServers(event):
            self.record_selection(list(tv.selection()))

        rs = db.query_executor("SELECT ID, NAME, SERVER_IP, USER_NAME, AUTH_METHOD FROM SERVERS")
        same_row = g.get_next_row()

        tv = ttk.Treeview(root, columns=(1,2,3,4,5),show='headings')
        tv.grid(row=g.get_next_row(),columnspan=10,sticky='nsew',rowspan=100)

        tv.heading(1, text='ID')
        tv.heading(2, text='Name')
        tv.heading(3, text='Server IP')
        tv.heading(4, text='Username')
        tv.heading(5, text='Type of Authentication')


        for rows in rs:
            tv.insert('','end',iid=rows[0],values=rows)

        tv.bind("<<TreeviewSelect>>",getServers)

    def add_a_server(self,root):

        def decide_auth_method(event):

            if(keyfileMenu.get() == "Password"):

                def get_password(event):
                    ServerManagement.password = password_entry.get()
                   
                ServerManagement.type_of_auth = "Password"
                authtype_menu.destroy()
                Label(addWindow,text="Enter the password: ",pady=10).grid(row=4,column=0)
                password_entry = Entry(addWindow,width=40, show="*", borderwidth=2)
                password_entry.grid(row=4,column=1,padx=10,pady=10)
                addWindow.bind('<Leave>', get_password)

            elif(keyfileMenu.get()=="Private Key File"):

                ServerManagement.type_of_auth = "Private Key File"
                keyfile_label = Label(addWindow,text="Select the keyfile: ",pady=10)
                keyfile_label.grid(row=4,column=0)

                def get_keyfile():
                    private_key_path = f.askopenfilename(title = "Select a Key File")

                    if private_key_path.endswith('.pem') or private_key_path.endswith('.ppk'):
                        ServerManagement.keyfile_location = os.path.abspath(private_key_path)
                        file_dialog_button.destroy()
                        keyfile_label.destroy()
                        Label(addWindow,text="File chosen:"+ServerManagement.keyfile_location).grid(row=3,column=1)

                    else:
                        messagebox.showerror("Error!",message="Only .pem or .ppk files are allowed!")
                        private_key_path = ""
                        # get_keyfile()

                file_dialog_button = Button(addWindow,text="Browse", command=get_keyfile)
                file_dialog_button.grid(row=4,column=1)

                # file_dialog_button.destroy()
                # keyfile_label.destroy()
                # Label(addWindow,text="File chosen:"+ServerManagement.keyfile_location).grid(row=3,column=1)

        def submit_info():
            ip_regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"

            if len(name_entry.get())<5 or len(ip_entry.get())<5 or len(username_entry.get())<5:
                messagebox.showerror("Error!", message="Please check your inputs. Minimum character length is 5")
                     
            elif not re.search(ip_regex,ip_entry.get()):
                messagebox.showerror("Error!",message="Enter a valid IP!")
            
            elif(' ' in name_entry.get() or ' ' in username_entry.get()):
                messagebox.showerror("Error!",message="You cannot have a space in username or server name")
                
            else:
                query_string=""
                if(ServerManagement.type_of_auth == "Password"):
                    if(len(ServerManagement.password)<4):
                        messagebox.showerror("Error!",message="Less than 4 characters for password? Enter a valid password!")
                    else:
                        query_string = """
                        INSERT INTO SERVERS (NAME, SERVER_IP, USER_NAME, AUTH_METHOD, PASSWORD) 
                        VALUES ('{name}','{ip}','{username}','{authmethod}','{password}');
                        """.format(name=name_entry.get(),ip=ip_entry.get(),username=username_entry.get(),authmethod=ServerManagement.type_of_auth, password=PasswordHandler.encrypt_password(ServerManagement.password))

                    
                elif(ServerManagement.type_of_auth == "Private Key File"):
                    query_string = """
                    INSERT INTO SERVERS (NAME, SERVER_IP, USER_NAME, AUTH_METHOD, KEY_FILE_LOCATION) 
                    VALUES ('{name}','{ip}','{username}','{authmethod}','{keyfilelocation}');
                    """.format(name=name_entry.get(),ip=ip_entry.get(),username=username_entry.get(),authmethod=ServerManagement.type_of_auth, keyfilelocation=ServerManagement.keyfile_location)
                
                if(len(query_string)>1):
                    db.query_executor(query_string)
                    addWindow.grab_release()
                    addWindow.destroy()
                

        addWindow = Toplevel(root)
        addWindow.title("Add a New Server")
        addWindow.grab_set()

        Label(addWindow,text="Name: ",pady=10).grid(row=0,column=0)
        Label(addWindow,text="IP Address: ",pady=10).grid(row=1,column=0)
        Label(addWindow,text="Username: ",pady=10).grid(row=2,column=0)
        Label(addWindow,text="Authentication Type: ",pady=10).grid(row=3,column=0)

        #Create a dropdown Menu
        menu_list = ["Private Key File", "Password"]
        keyfileMenu= StringVar(addWindow)
        keyfileMenu.set("Authentication Method")

        authtype_menu = OptionMenu(addWindow, keyfileMenu, *menu_list, command=decide_auth_method)

        name_entry = Entry(addWindow,width=40,borderwidth=2)
        name_entry.grid(row=0,column=1,padx=10,pady=10)
        ip_entry = Entry(addWindow,width=40,borderwidth=2)
        ip_entry.grid(row=1,column=1,padx=10,pady=10)
        username_entry = Entry(addWindow,width=40,borderwidth=2)
        username_entry.grid(row=2,column=1,padx=10,pady=10)

        authtype_menu.grid(row=3,column=1,padx=10,pady=10)

        Button(addWindow,text="Submit",command=submit_info).grid(row=6,column=0)
        Button(addWindow,text="Cancel",command=addWindow.destroy).grid(row=6,column=1)

    def refresh(self,root):
        ServerManagement.selected_servers.clear()
        for item in root.winfo_children():
            item.destroy()
        Label(root, text="Welcome to VMSTAT automator!", font=('calibre','20','bold')).grid(row=g.get_next_row(),column=0,columnspan=10)
        self.__init__(root,ServerManagement.action_item)

    def delete_a_server(self):

        if(len(self.selected_servers)==0):
            messagebox.showerror("Error","Please select at least one server to delete", icon="error")
        else:
            mb = messagebox.askquestion("Delete","Are you sure about deleting {} selected server(s) from the database?".format(str(len(self.selected_servers))),icon="warning")
            if mb == 'yes':
                inclause = ""
                for iter in range(len(self.selected_servers)):
                    inclause = inclause + "," + str(self.selected_servers[iter]) 
                inclause = inclause[1:]
                query = "DELETE FROM SERVERS WHERE ID IN ({});".format(inclause)
                db.query_executor(query)


class RecordActions:

    def __init__(self,root) -> None:


        for item in root.winfo_children():
            item.destroy()

        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        def go_to_next_page(root):
            if(radioVar.get()==""):
                messagebox.showerror("Error!","Choose an action to proceed further")
            else:
                # InvokeActions(root,radioVar.get())
                if radioVar.get() == "runvmstat" or radioVar.get() == "runawr":
                    ServerManagement(root,radioVar.get())
                else:
                    InvokeActions(root,radioVar.get())

        def exit_window(root):
            root.quit()

        Label(root, text="Select Action", font=('calibre','15','bold')).grid(row=g.get_next_row(),column=0,columnspan=10)
        Label(root, text="Select a common action that you want to perform ", font=('calibre','12','bold')).grid(row=g.get_next_row(),column=0,columnspan=10)
        next_button = Button(root,text="Next>",command=lambda:go_to_next_page(root))
        next_button.grid(row=300,column=3)
        exit = Button(root,text="Exit",command=lambda:exit_window(root))
        exit.grid(row=300,column=4)

        # i=1
        # for server in range(len(server_list)):
        #     rs = db.query_executor("SELECT NAME, SERVER_IP FROM SERVERS WHERE ID = {}".format(server_list[server]))
        #     for item in rs:
        #         #listbox.insert(i,str(i)+". "+item[0]+" ("+item[1]+")")
        #         Label(root,text=str(i)+". "+item[0]+" ("+item[1]+")").grid(row=g.get_next_row(),column=0,sticky="w")
        #         i += 1
        # #some additional space
        # g.get_blank_lines(root,2)

        def record_user_action():
            pass
            
        radioVar = StringVar(value='runvmstat')
        r1 = Radiobutton(root,text="Run VMSTAT",variable=radioVar,value="runvmstat",command=record_user_action)
        r1.grid(row=g.get_next_row(),column=0,sticky="news")
        r2 = Radiobutton(root,text="Collect VMSTAT Report",variable=radioVar,value="collectvmstat",command=record_user_action)
        r2.grid(row=g.get_next_row(),column=0,sticky="news")
        r3 = Radiobutton(root,text="Take a DB snapshot",variable=radioVar,value="runawr",command=record_user_action)
        r3.grid(row=g.get_next_row(),column=0,sticky="news")
        r4 = Radiobutton(root,text="Generate an AWR Report",variable=radioVar,value="collectawr",command=record_user_action)
        r4.grid(row=g.get_next_row(),column=0,sticky="news")


class InvokeActions:
    when_to_run=""
    how_much_to_wait = ""
    begin_snap_id = ""
    end_snap_id = ""
    selected_snap_list = []

    def __init__(self,root,action_item) -> None:

        for item in root.winfo_children():
            item.destroy()
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        if(action_item == "runvmstat"):

            # for item in root.winfo_children():
            #     item.destroy()
            # root.rowconfigure(0, weight=1)
            # root.columnconfigure(0, weight=1)

            def submit_info():
                if not duration_entry.get().isdigit() or not frequency_entry.get().isdigit():
                    messagebox.showerror("Error","Please check your input. Duration and Frequency must be a number")
                elif(len(name_entry.get())<5 or name_entry.get().isdigit() or ' ' in name_entry.get()):
                    messagebox.showerror("Error","Please enter a valid name for this report, with length greater than 5 and has at least one alphabet and must not have any space between them")
                else:
                    rv.RunVmstat(root,ServerManagement.selected_servers,duration_entry.get(),frequency_entry.get(),name_entry.get())
                

            Label(root, text="Run VMSTAT", font=('calibre','15','bold')).grid(row=g.get_next_row(),column=0,columnspan=10)
            Label(root, text="Enter a few more details to proceed:", font=('calibre','13','bold')).grid(row=g.get_next_row(),column=0,columnspan=10)
            dur_grid_row = g.get_next_row()
            freq_grid_row = g.get_next_row()
            name_grid_row = g.get_next_row()
            Label(root,text="Total Test Duration in Minutes: ",pady=10).grid(row=dur_grid_row,column=0,sticky="w")
            Label(root,text="Frequency: ",pady=10).grid(row=freq_grid_row,column=0,sticky="w")
            Label(root,text="A unique name for this test: ",pady=10).grid(row=name_grid_row,column=0,sticky="w")

            duration_entry = Entry(root,width=40,borderwidth=2)
            duration_entry.grid(row=dur_grid_row,column=1,padx=10,pady=10)
            frequency_entry = Entry(root,width=40,borderwidth=2)
            frequency_entry.grid(row=freq_grid_row,column=1,padx=10,pady=10)
            name_entry = Entry(root,width=40,borderwidth=2)
            name_entry.grid(row=name_grid_row,column=1,padx=10,pady=10)

            button_grid_row = g.get_next_row()
            Button(root,text="Submit",command=submit_info).grid(row=button_grid_row,column=0)
            Button(root,text="Exit",command=root.quit).grid(row=button_grid_row,column=1)


        elif(action_item == "collectvmstat"):
            
            Label(root, text="Collect VMSTAT Reports", font=('calibre','15','bold')).grid(row=g.get_next_row(),column=0,columnspan=10)
            Label(root, text="Here are the uncollected reports, select the servers from which you want to copy the reports and click proceed", font=('calibre','13','bold')).grid(row=g.get_next_row(),column=0,columnspan=10)
            g.get_blank_lines(root,1)

            def delete_from_vms():
                query = "DELETE FROM VMSTAT"
                delete_sure = messagebox.askyesno(title="Are you sure?",message="Are you sure that you want to delete all rows from the table?")
                if delete_sure:
                    db.query_executor(query)
                    messagebox.showinfo(message="All rows from the table VMSTAT have been deleted.")
                    root.quit()

            def collect_vmstat(vms_server_list):
                if len(ServerManagement.selected_vmstat_servers) == 0:
                    messagebox.showerror("Error","Please select at least one server to proceed", icon="error")
                else:
                    rscp.RunSCP(root,vms_server_list)

            same_row = g.get_next_row()
            Button(root,text="Proceed>", command=lambda:collect_vmstat(ServerManagement.selected_vmstat_servers)).grid(row=same_row,column=1)
            Button(root,text="DELETE ALL ROWS", command=lambda:delete_from_vms()).grid(row=same_row,column=2)

            g.get_blank_lines(root,2)
            
            def record_vms_selection(current_list):
                ServerManagement.selected_vmstat_servers.clear()
                ServerManagement.selected_vmstat_servers = current_list
                    
            def get_vms_servers(event):
                record_vms_selection(list(tv.selection()))

            rs = db.query_executor("SELECT V.ID,V.EXECUTION_TIME,V.COMMON_NAME,V.COMMAND, S.NAME, S.SERVER_IP FROM VMSTAT V, SERVERS S WHERE V.SERVER = S.ID")

            tv = ttk.Treeview(root, columns=(1,2,3,4,5,6),show='headings')
            tv.grid(row=g.get_next_row(),columnspan=10,sticky='nsew',rowspan=100)

            tv.heading(1, text='ID')
            tv.heading(2, text='Executed On')
            tv.heading(3, text='Name Provided')
            tv.heading(4, text='Command Used')
            tv.heading(5, text='Server Name')
            tv.heading(6, text='Server IP')


            for rows in rs:
                tv.insert('','end',iid=rows[0],values=rows)

            tv.bind("<<TreeviewSelect>>",get_vms_servers)
          


        elif(action_item == "runawr"):

            # ServerManagement(root)

            if len(ServerManagement.selected_servers)!=1:
                messagebox.showerror("ERROR!",message="For this option, you will have to select just one server at a time.\n Please close the window and select only one DB at a time.")
                root.quit()

            else:
                Label(root, text="Take an AWR snapshot", font=('calibre','15','bold')).grid(row=g.get_next_row(),column=0,columnspan=10)
                Label(root, text="Choose when to take the snapshot", font=('calibre','13','bold')).grid(row=g.get_next_row(),column=0,columnspan=10)
                g.get_blank_lines(root,1)

                def take_awr_snapshot():
                    if awr_radio_var.get() == "now":
                        InvokeActions.when_to_run = "now"
                        TakeSnapshot(root,ServerManagement.selected_servers,InvokeActions.when_to_run, InvokeActions.how_much_to_wait)


                    elif awr_radio_var.get() == "later":
                        InvokeActions.when_to_run = "later"
                        message = """
                            You have chosen to take the snapshot later at a time. \n
                            Please note that for this to work, you must keep this program running until the time window. \n
                            Do you still want to proceed?
                        """
                        up_consent = messagebox.askyesno(title="Can you leave this open?",message=message)

                        if up_consent:

                            for item in root.winfo_children():
                                item.destroy()
                            root.rowconfigure(0, weight=1)
                            root.columnconfigure(0, weight=1)

                            def validate_take_after_minutes(minutes):
                                if not str(minutes).isdigit():
                                    messagebox.showerror("Error!",message="Enter a valid number!")
                                else:
                                    InvokeActions.how_much_to_wait = take_after_minute_entry.get()
                                    TakeSnapshot(root,ServerManagement.selected_servers,InvokeActions.when_to_run,InvokeActions.how_much_to_wait)

                            same_row = g.get_next_row()
                            Label(root,text="Take after: ",pady=10).grid(row=same_row,column=0,sticky="w")
                            take_after_minute_entry = Entry(root,width=40,borderwidth=2)
                            take_after_minute_entry.grid(row=same_row,column=1,padx=10,pady=10)
                            Label(root,text="minute(s) ",pady=10).grid(row=same_row,column=2,sticky="w")
                            Button(root,text="Proceed>", command=lambda:validate_take_after_minutes(take_after_minute_entry.get())).grid(row=g.get_next_row(),column=1)

                    else:
                        messagebox.showerror("Error","Please select at least one option to proceed", icon="error")


                awr_radio_var = StringVar()
                r1 = Radiobutton(root,text="Take immediately",variable=awr_radio_var,value="now")
                r1.grid(row=g.get_next_row(),column=0,sticky="news")
                r2 = Radiobutton(root,text="Take in sometime",variable=awr_radio_var,value="later")
                r2.grid(row=g.get_next_row(),column=0,sticky="news")
        

                Button(root,text="Next>", command=take_awr_snapshot).grid(row=g.get_next_row(),column=1)

            
        else:
            Label(root, text="Generate an AWR report", font=('calibre','15','bold')).grid(row=g.get_next_row(),column=0,columnspan=10)
            Label(root, text="Here are the uncollected snapshots, select begin and end snap IDs to proceed", font=('calibre','13','bold')).grid(row=g.get_next_row(),column=0,columnspan=10)
            g.get_blank_lines(root,1)

            def delete_from_awr():
                query = "DELETE FROM AWR"
                delete_sure = messagebox.askyesno(title="Are you sure?",message="Are you sure that you want to delete all rows from the table?")
                if delete_sure:
                    db.query_executor(query)
                    messagebox.showinfo(message="All rows from the table AWR have been deleted.")
                    root.quit()

            def generate_awr():
                if len(InvokeActions.selected_snap_list) == 0:
                    messagebox.showerror("Error","Please select at least one server to proceed", icon="error")
                elif len(InvokeActions.selected_snap_list)!=2:
                    messagebox.showerror("Error",message="Please select only 2 rows:\n First row as begin snap, second as the end")
                else:
                    GenerateAWR(root,InvokeActions.selected_snap_list)

            same_row = g.get_next_row()
            Button(root,text="Proceed>", command=lambda:generate_awr()).grid(row=same_row,column=1)
            Button(root,text="DELETE ALL ROWS", command=lambda:delete_from_awr()).grid(row=same_row,column=2)

            g.get_blank_lines(root,2)
            
            def record_snap_selection(current_list):
                InvokeActions.selected_snap_list.clear()
                InvokeActions.selected_snap_list = current_list
                    
            def get_vms_servers(event):
                record_snap_selection(list(tv.selection()))

            rs = db.query_executor("SELECT A.ID, S.ID, S.NAME, A.SNAP_ID, A.SNAP_TIME FROM AWR A, SERVERS S WHERE A.SERVER_ID = S.ID")

            tv = ttk.Treeview(root, columns=(1,2,3,4,5),show='headings')
            tv.grid(row=g.get_next_row(),columnspan=10,sticky='nsew',rowspan=100)

            tv.heading(1, text='ID')
            tv.heading(2, text='Server ID')
            tv.heading(3, text='Server Name')
            tv.heading(4, text='Snap ID')
            tv.heading(5, text='Snap Time')

            for rows in rs:
                tv.insert('','end',iid=rows[0],values=rows)

            tv.bind("<<TreeviewSelect>>",get_vms_servers)
