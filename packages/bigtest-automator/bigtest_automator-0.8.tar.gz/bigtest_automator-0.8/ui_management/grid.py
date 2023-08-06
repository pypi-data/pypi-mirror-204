from tkinter import *
class Grid:

    row_counter = 0

    def get_next_row(self):
        Grid.row_counter += 1
        return Grid.row_counter

    def get_blank_lines(self,root,num_of_blank_lines):
        for _ in range(num_of_blank_lines):
            Label(root,text="").grid(row=Grid.get_next_row(self),column=0)