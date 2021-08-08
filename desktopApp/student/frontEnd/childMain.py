from cefpython3 import cefpython as cef
import ctypes
from tkinter import *
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
import sys
import os
import platform
import logging as _logging
from PIL import ImageTk,Image
from time import strftime

sys.path.insert(0, os.path.abspath("/student/frontEnd/"))

from .studentClass import Student
from .hallway import Hallway
from .schedule import Schedule
from .ChildEmbeddedBrowser import MainFrame
from .childDashboard import ChildDashboard
from parent.frontEnd.parentPortal.parentPortalMain import *
from Main_Parent import Main
from .parent_access import ParentAccess





class ChildMain(tk.Frame):

    def __init__(self, root, backend):   
   
        self.root = root
        self.backend = backend
        root.geometry("1400x800")
        root.configure(bg="white")        
        self.setup_icon()

        tk.Frame.__init__(self, root)
        self.master.title("littleLEARNERS")

        self.studentList = []
        self.studentList.append(Student('student/frontEnd/images/Erin.jpg', 'Erin', 'Doe'))
        self.studentList.append(Student('student/frontEnd/images/timmy.jpg', 'Timmy', 'Smith'))
        self.columns = len(self.studentList)
  
        self.topFrame = Frame(root, bg='white', height=50, pady=25, padx=40)
        self.topFrame.pack(side=TOP, fill=X)
        self.topFrame.columnconfigure((0, 1, 2, 3), weight=1)    
        
        self.centerFrame = Frame(root, bg="white", padx=25)
        self.centerFrame.pack(fill=BOTH, expand=True)
        self.centerFrame.columnconfigure((0, 3), weight=1)
        self.centerFrame.columnconfigure((1, 2), weight=1)
        self.centerFrame.rowconfigure((0, 1, 2), weight=1)
        
        #display student
        self.display_students()

        #display parent access button
        self.parentAccess()
        self.setup_banner_image()      
        

        #self.update()
        
    # def update(self):
    #     self.backend.update()
    #     self.backend.pushUpdates()
    #     self._job = self.root.after(10000, self.update)
            
    def setup_icon(self):          
        p1 = PhotoImage(file = 'student/frontEnd/images/icon.png')
        self.root.iconphoto(False, p1)        


    def setup_banner_image(self):         
        photo = Image.open('student/frontEnd/images/orangePic3.png') #open image
        resized = photo.resize((200, 87), Image.ANTIALIAS) #resize
        correctedImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage        
        pictureFrame = Label(self.topFrame, image=correctedImage, anchor=NE, bg="white")
        pictureFrame.image = correctedImage #do this so image isnt lost in garbage collection
        pictureFrame.grid(column=0, row=0, rowspan=2, sticky="W")

    def display_main_helper(self, index, frame):
        self.backend.initChild(index)
        self.display_main(frame)

    def display_main(self, frame):
         new_center = frame(self.root, self.backend)
         if self.centerFrame is not None:
            self.centerFrame.destroy()
            self.topFrame.destroy()
         self.centerFrame = new_center
         self.centerFrame.pack(fill=BOTH, expand=True)


    def display_name(self, student, columns):   
        firstName = student.getFirstName()
        name = Label(self.centerFrame, font = ('montserrat', 32, 'bold'), text=firstName, foreground="#1B1B1B", background="#ffffff")
        name.grid(row=1, column=cols, sticky=N)


    def resize_image(self, fileName):
            photo = Image.open(fileName) #open image
            resized = photo.resize((200, 240), Image.ANTIALIAS) #resize
            correctedImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage
            return correctedImage


    def display_students(self):
        cols = 1
        #for i, child in enumerate(self.studentList):
        for i, child in enumerate(self.backend.parent.children):            
            #correctedImage = self.resize_image(child.getImage()) #retrieve and resize student picture
            correctedImage = self.resize_image(child.image) #retrieve and resize student picture
            
            pictureFrame = Button(self.centerFrame, image=correctedImage, borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff', command=lambda i = i :self.display_main_helper(i, ChildDashboard))
            pictureFrame.image = correctedImage #do this so image isnt lost in garbage collection
            pictureFrame.grid(row=0, column=cols, sticky=S)
            self.display_name(child, cols)
            cols += 1
    
    #OLD display_students
    # def display_students(self):
    #     cols = 1
    #     for child in self.studentList:
    #         correctedImage = self.resize_image(child.getImage()) #retrieve and resize student picture
    #         pictureFrame = Button(self.centerFrame, image=correctedImage, borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff', command=lambda:[self.display_main(ChildDashboard)])
    #         pictureFrame.image = correctedImage #do this so image isnt lost in garbage collection
    #         pictureFrame.grid(row=0, column=cols, sticky=S)
    #         self.display_name(child, cols)
    #         cols += 1

    def display_name(self, child, cols):   
            firstName = child.getName()
            name = Label(self.centerFrame, font = ('montserrat', 32, 'bold'), text=firstName, foreground="#1B1B1B", background="#ffffff")
            name.grid(row=1, column=cols, sticky=N)
    

    def parentAccess(self):
        photo = Image.open('student/frontEnd/images/parentAccess.png') #open image
        resized = photo.resize((120, 70), Image.ANTIALIAS) #resize
        correctedImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage
        parent = Button(self.topFrame, image=correctedImage, borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff', command=self.parentView)
        parent.image = correctedImage
        parent.grid(column=3, row=0, sticky="E")

    #parent view without password
    # def parentView(self):
    #     global win2        
    #     win2 = Toplevel(self.root)
    #     win2.geometry("1200x800")       
    #     ParentPortalMain(win2, self.backend)

    def parentView(self):
        global win2    
        win2 = Toplevel(self.root)
        win2.geometry("400x300")
        ParentAccess(win2, self.backend)  
                
     

  

   
   


 

"""
def Main():
    studentList = []
    studentList.append(Student('student/frontEnd/images/Erin.jpg', 'Erin', 'Doe'))
    studentList.append(Student('student/frontEnd/images/timmy.jpg', 'Timmy', 'Smith'))
    columns = len(studentList)
    root = tk.Tk()


   
    childGUI = ChildMain(root, backend)

    
    childGUI.mainloop()

if __name__=='__main__':
    Main()
    """