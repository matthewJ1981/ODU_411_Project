from tkinter import *

def clear(root):
    list= root.grid_slaves()
    for l in list:
        l.destroy()