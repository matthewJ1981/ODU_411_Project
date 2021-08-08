from tkinter import *
import sys
import os
from PIL import ImageTk,Image
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
import webbrowser
from .studentClass import Student
from student.frontEnd.ChildEmbeddedBrowser import MainFrame


class Hallway(tk.Frame):
    def __init__(self, parent):       
        tk.Frame.__init__(self, parent)
        self.parent = parent
        
        self.my_canvas = Canvas(self, width="800", height="500")
        self.my_canvas.pack(fill="both", expand=True)
        self.bind("<Configure>", self.resizer)

        photo = Image.open('student/frontEnd/images/seesaw_button.png') #open image
        resized = photo.resize((150, 40), Image.ANTIALIAS) #resize
        correctedImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage
        self.seesawButton=Button(self, image=correctedImage, borderwidth = 0, bg='#fcf7e3', highlightthickness=0, activebackground='#fcf7e3',command=lambda:self.loadWebpage('https://app.seesaw.me/#/login'))
        self.seesawButton.image = correctedImage
        seesawButton_window = self.my_canvas.create_window(485, 290, anchor="center", window = self.seesawButton)

        photo = Image.open('student/frontEnd/images/zeil_button.png') #open image
        resized = photo.resize((200, 52), Image.ANTIALIAS) #resize
        correctedImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage
        self.zeilButton=Button(self, image=correctedImage, borderwidth = 0, bg='#fcf7e3', highlightthickness=0, activebackground='#fcf7e3',command=lambda:self.loadWebpage('https://www.cs.odu.edu/~411orang/build/website/Directory/outline/index.html'))
        self.zeilButton.image = correctedImage
        zeilButton_window = self.my_canvas.create_window(485, 375, anchor="center", window = self.zeilButton)

    
        photo = Image.open('student/frontEnd/images/zoom_button.png') #open image
        resized = photo.resize((250, 65), Image.ANTIALIAS) #resize
        correctedImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage
        self.zoomButton=Button(self, image=correctedImage, borderwidth = 0, bg='#fcf7e3', highlightthickness=0, activebackground='#fcf7e3',command=lambda:self.loadWebpage('https://zoom.us/join'))
        self.zoomButton.image = correctedImage
        zoomButton_window = self.my_canvas.create_window(485, 500, anchor="center", window = self.zoomButton)
        
       
   
    def resizer(self, e): #e is an event, function to dynamically resize background
        global bg, resized_bg, center_bg
        bg = Image.open('student/frontEnd/images/hallway.png')   
        resized_bg = bg.resize((e.width, e.height), Image.ANTIALIAS) #resize image according to event    
        center_bg = ImageTk.PhotoImage(resized_bg) #Define image again
        self.my_canvas.create_image(0,0, image=center_bg, anchor="nw")
        
    def loadWebpage(self,link):
        self.parent.show_browser(MainFrame)
        if link == 'https://zoom.us/join':
            webbrowser.open(link, new=2)
        else:
            self.after(500,lambda:self.parent.centerFrame.navigate(link))
    
       
    

   


