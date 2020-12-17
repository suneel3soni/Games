"""
create playing_field
"""

from tkinter import *


class Playing_field(Frame):
    def __init__(self, parent=None, width=310, height=400):
        Frame.__init__(self, parent)
        self.grid(row=0, column=0)
        self.configure(width=width, height=height)
        self.field = Canvas(self, width=width,
                            height=height, background="cornsilk2")
        self.field.pack()
        self.field.focus_set()
        self.field.create_line(200, 0, 200, 400)  # right line
        self.table_coordinates = self.create_table_coordinates()

    def create_table_coordinates(self):
        table = {}
        lis = []
        x = 10
        y = 10
        for i in range(20):
            for j in range(15):
                lis.append((x, y))
                x = x + 20
            x = 10
            table[i] = lis
            lis = []
            y = y + 20
        return table

    def return_canvas(self):
        return self.field

    def return_table_coordinates(self):
        return self.table_coordinates

win = Playing_field()
