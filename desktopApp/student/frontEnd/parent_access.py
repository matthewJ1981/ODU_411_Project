import sys
from tkinter import *
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
import ctypes, sys
import os
import platform
import logging as _logging
from time import strftime
from PIL import ImageTk,Image

import os, sys
#Need to add parent path to system path to import
sys.path.insert(0, os.path.abspath("./parent"))
#start import from /parent/ directory
from frontEnd.parentPortal.parentPortalMain import *

class ParentAccess():
    def __init__(self, root, backend):
        self.root = root
        root.title("littleLEARNERS - Access Parent Portal")
        self.fm = Frame(root)
        self.fm.configure(background='white', padx=25, pady=25) 
        self.fm.pack(fill=BOTH, expand=True)
        self.fm.columnconfigure((0, 1), weight=1)     
        self.fm.rowconfigure((0, 1, 2, 3), weight=1)

        #message
        self.pwdLabel= Label(self.fm,text="To access the Parent Portal,", bg='#ffffff', font = ('montserrat', 16, 'bold'))
        self.pwdLabel.grid(row=0, column=0, sticky="S")
        self.pwdLabel2= Label(self.fm, text="enter your password:", bg='#ffffff', font = ('montserrat', 16, 'bold'))
        self.pwdLabel2.grid(row=1, column=0,  columnspan=2, sticky="N")

        #entry
        self.passwordEntry = Entry(self.fm, bg="#ffffff")
        self.passwordEntry = Entry(self.fm,show = "*")
        self.passwordEntry.grid(row=2,column=0, columnspan=2, sticky='N')

        #enter button
        photo = Image.open('student/frontEnd/images/enter.png') #open image
        resized = photo.resize((100, 35), Image.ANTIALIAS) #resize
        correctedImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage
        self.enter=Button(self.fm, image=correctedImage, borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff', command=lambda: accessParentPortal(backend.parent.username, self.passwordEntry.get()))
        self.enter.image = correctedImage
        self.enter.grid(row=3, column =0, columnspan=2)

        photo = Image.open('student/frontEnd/images/exit.png') #open image
        resized = photo.resize((100, 34), Image.ANTIALIAS) #resize
        correctedImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage
        self.enter=Button(self.fm, image=correctedImage, borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff', command=lambda: root.destroy())
        self.enter.image = correctedImage
        self.enter.grid(row=4, column = 0, columnspan=2, sticky="N")

        def setup_icon():          
            p1 = PhotoImage(file = 'student/frontEnd/images/icon.png')
            root.iconphoto(False, p1) 

        #display parent portal
        def accessParentPortal(username, password):
             global win3
             returnCode, returnMessage = backend.login(username, password)
             if returnCode == "000":             
               self.fm.destroy()        
               win3 = self.root
               win3.lift()
               #win3.geometry("1400x800")
               ParentPortalMain(win3, backend)               
             else:
                 print(returnMessage)
                  

        setup_icon()