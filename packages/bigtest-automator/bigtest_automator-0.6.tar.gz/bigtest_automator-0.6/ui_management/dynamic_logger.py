import tkinter
class Logger():
    def __init__(self,root,text,info) -> None:
        text.configure(state="normal")
        text.insert(tkinter.INSERT,info+"\n")
        text.configure(state="disabled")
        root.update()