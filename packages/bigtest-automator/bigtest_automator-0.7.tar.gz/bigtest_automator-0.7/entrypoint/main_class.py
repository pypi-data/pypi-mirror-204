from tkinter import *
from ui_management import tk_page_layouts, grid
import entrypoint.initialize as initialize


g = grid.Grid() 

def main():
    initialize.initialize_db()
    root = Tk()
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    frm = Frame(root)
    frm.pack(side=LEFT, padx=20)


    # root.geometry("2000x500")
    root.resizable(0, 0)
    root.title("VMSTAT Automator")

    Label(frm, text="Welcome to VMSTAT automator!", font=('calibre','20','bold')).grid(row=g.get_next_row(),column=0,columnspan=10)

    tk_page_layouts.RecordActions(frm)

    root.mainloop()

if __name__ == "__main__":
    main()