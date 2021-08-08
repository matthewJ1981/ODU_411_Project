from tkinter import *
import tkinter as tk
from tkinter import font as tkFont
from PIL import ImageTk,Image 
import math

from Macro.CreateMacro import *
from Macro.RecordMacroBrowser import *
from Macro.Containers import *
from Macro.ExecuteMacro import *

class ManageMacros(tk.Frame):
    def __init__(self, parentFrame, root, backend, onclickmenu):
        print('Entering ManageMacros.py')
        root.title("littleLEARNERS - Macro Manager")
        self._root = root
        self.backend = backend
        self.parentFrame = parentFrame
        self.onclickmenu = onclickmenu

        if hasattr(self,'child'):
            self.child = None
        self.child = Child()
        self.child.setup(backend,onclickmenu.childIndex)

        self.display(root)
        
    def createMacro(self):
        #self.backend.initChild(self.child.index)
        self.backend.currChild = self.child.index
        self.topFrame.destroy()
        self.middleFrame.destroy()
        CreateMacro(self.parentFrame,self._root, self.backend,self.child,self.onclickmenu)

    def launchMacro(self,macroIndex):
        self.child.currentMacro = self.child.macros[macroIndex]
        self.child.parentPlayback = True
        print("Playing Macro:",self.child.currentMacro.name)
        
        #self.backend.initChild(self.child.index)
        self.backend.currChild = self.child.index
        self.playbackWindow = Toplevel(self._root)
        self.childFrame = ChildDashboard(self.playbackWindow,self.backend)
        self.childFrame.pack(fill=BOTH,expand=TRUE)
        
        self._root.after(500,lambda:ExecuteMacro(self.childFrame,self.child.currentMacro.elements,self.backend,self.child, False))

    def deleteAllMacros(self,root):
        classes = self.backend.parent.children[self.child.index].getClasses()
        activities = []
        for c in classes:
            activities.extend(c.getActivities())
        for a in activities:
            try:
                a.setHasMacro(False)
            except:
                raise
        for e in self.backend.parent.children[self.child.index].getMacroElements():
            try:
                self.backend.db.macroElement.remove(e.id)
            except:
                raise
            if os.path.exists(e.imgPath):
                os.remove(e.imgPath)
        
        self._root.after(5000,lambda:self.onclickmenu(13))


    def deleteMacro(self,macroIndex,root):
        beforeDelLength = len(self.child.macros)
        print("Deleting macro:",self.child.macros[macroIndex].name)

        classes = self.backend.parent.children[self.child.index].getClasses()
        activities = []
        for c in classes:
            activities.extend(c.getActivities())
        for a in activities:
            print('activity2:',a.name)
            if a.id == self.child.macros[macroIndex].activityId:
                try:
                    a.setHasMacro(False)
                except:
                    raise

        for e in self.child.macros[macroIndex].elements:
            try:
                self.backend.db.macroElement.remove(e.id)
            except:
                raise
            if os.path.exists(e.imgPath):
                os.remove(e.imgPath)

           # self.onclickmenu(13)
            self._root.after(5000,lambda:self.onclickmenu(13))
        

    def display(self,root):
        self.rightFrameWidth = self.parentFrame.rightFrame.winfo_width()
        self.rightFrameHeight = self.parentFrame.rightFrame.winfo_height()

        ### top frame
        self.topFrame = Frame(self.parentFrame.rightFrame, width=self.rightFrameWidth, height=170, bd=2, relief="groove")  
        self.topFrame.configure(background='white')
        self.topFrame.pack(anchor=W, padx=(10), pady=(10))
        self.topFrame.pack_propagate(0)

        ##### title
        self.title = Label(self.topFrame, font = ('montserrat', 35, 'bold'), text=(self.child.name + "'s Macros"), foreground="#1B1B1B", background="#ffffff")
        self.title.config(anchor=CENTER)
        self.title.pack(side=TOP)

        createMacroButton = Button(self.topFrame, text="Create New Macro", background="white",command=lambda:self.createMacro())
        createMacroButton.pack(pady = (5,0),anchor='w')

        deleteAllMacrosButton = Button(self.topFrame, text="Delete All Macros", background="white", foreground="red", command=lambda:self.deleteAllMacros(root))
        deleteAllMacrosButton.pack(pady = (5,5),anchor='w')

        
        #middle frame (containing list of macros)
        self.middleFrame = Frame(self.parentFrame.rightFrame, width=self.rightFrameWidth*0.9, height=150, bd=0, relief="groove")  
        self.middleFrame.configure(background='white')
        self.middleFrame.pack(anchor=W, padx=(10), pady=(100))
        self.middleFrame.pack_propagate(0)


        #display each macro:
        currentRow = 0
        currentCol = 0

        photo = Image.open('student/frontEnd/images/goToClass.png') #open image
        resized = photo.resize((80, 100), Image.ANTIALIAS) #resize
        self.font = font.Font(family="Comic Sans",size="16",weight="bold")
        correctedImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage

        for i in range(0,len(self.child.macros)):
            if i>0 and i%6==0:
                currentRow += 3
                currentCol = 0
            
            #launch macro button
            macroButton = Button(self.middleFrame, image=correctedImage, borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff',command = lambda i=i:self.launchMacro(i))
            macroButton.image = correctedImage   
            macroButton.grid(row=currentRow,column=currentCol,padx =(20,20))

            #label with macro name
            mNameLabel = Label(self.middleFrame, font=self.font,text=self.child.macros[i].name, background="white")
            mNameLabel.grid(row=currentRow+1,column=currentCol,padx = (20,20))

            #delete macro button
            deleteButton = Button(self.middleFrame, text="Delete", background="white", foreground="red",command = lambda i=i:self.deleteMacro(i,root))
            deleteButton.grid(row=currentRow+2,column=currentCol,padx = (20,20),pady=(0,50))

            currentCol += 1

    



            



