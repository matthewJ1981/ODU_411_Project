from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font as tkFont
from PIL import ImageTk,Image
import datetime
from datetime import date, timedelta,datetime
#####
import os, sys
#sys.path.insert(0, os.path.abspath("../Macro"))

from Macro.RecordMacroBrowser import *
from Macro.Containers import *
######

class CreateMacro(tk.Frame):
    def __init__(self,parent,root,backend,child,onclickmenu):
        print('Entering CreateMacro.py')
        self.root = root
        self.backend = backend
        self.onclickmenu = onclickmenu
        self.child = child
        self.parentFrame = parent
        self.rightFrame = parent.rightFrame
        self.window = None
        self.font = font.Font(family="montserrat",size="16",weight="bold")

        

        self.openActs = self.getAvailableActivities() #activities that do not have an associated macro
        
        
        self.displayMacroCreationFields()

    def displayMacroCreationFields(self):
        self.rightFrameWidth = self.rightFrame.winfo_width()
        self.rightFrameHeight = self.rightFrame.winfo_height()

        #instructions frame
        self.topFrame = Frame(self.rightFrame, width=self.rightFrameWidth, height=300, bd=2, relief="groove")
        self.topFrame.configure(background='white')
        #self.topFrame.pack(anchor=W, padx=(10), pady=(10))
        #self.topFrame.pack_propagate(0)

        instructionsLabel = Label(self.topFrame, text="Instructions go here", background="white")
        #instructionsLabel.grid(padx = (20,20))

        #Macro Creation Fields
        self.bottomFrame = Frame(self.rightFrame, width=self.rightFrameWidth, height=300, bd=2, relief="groove")
        self.bottomFrame.configure(background='white')
        self.bottomFrame.pack(anchor=W, padx=(10), pady=(10))
        self.bottomFrame.pack_propagate(0)

        #Display Macro Name field
        macroNameLabel = Label(self.bottomFrame, text='Set a name for the macro:', background="white", font="bold", anchor="w", width=50)
        macroNameLabel.grid(column = 0, row = 1)

        self.mNameVar = StringVar(self.bottomFrame, value='Name')
        self.macroNameField = Entry(self.bottomFrame,width=50,textvariable=self.mNameVar)
        self.macroNameField.grid(column= 1, row = 1, padx=(20, 0), pady=10,sticky=W)

        #Display activity list
        activitySelectInstructions = label = Label(self.bottomFrame, text="Select the activity corresponding to the macro: \n(If an activity already has a macro,\n delete the macro before recording a new one.)", background="white", font="bold", anchor="w",width=50)
        activitySelectInstructions.grid(column = 0, row=2,sticky=W)

        #activity dropdown
        
        self.activityDropDown = ttk.Combobox(self.bottomFrame, text = 'Activity', values=[x[0] for x in self.openActs],width=50)
        self.activityDropDown.grid(column=1,row=2,columnspan=2,padx=(20, 0), pady=10,sticky='W')

        
        #Display Starting URL field
        self.startURLInstructions = Label(self.bottomFrame, text='Enter the URL of the webpage you would like to start on:', background="white", font="bold", anchor="w",width=50)
        self.startURLInstructions.grid(column = 0, row=5,sticky='W')

        self.urlVar = StringVar(self.bottomFrame, value='https://app.seesaw.me/')
        self.startURLField = Entry(self.bottomFrame,width=50, textvariable=self.urlVar)
        self.startURLField.grid(column=1,row=5,columnspan=3,padx=(20, 0), pady=10,sticky=W)

        self.createButton= Button(self.bottomFrame, width=20, text = "Create and Continue", foreground="green", font="bold", command=self.createMacro)
        self.createButton.grid(column=0,row=6,padx=(20,0),pady=10,sticky='E')

        self.cancelButton= Button(self.bottomFrame, width=10, text = "Cancel", foreground="red", font="bold")
        self.cancelButton.grid(column=1,row=6,padx=(20,0),pady=10,sticky='W') 

    def createMacro(self):
        inputIsValid = self.verifyUserInput()
       
        if inputIsValid:
            self.onclickmenu(2)
            #self.backend.currChild = self.child.index
            self.recordingWindow = Toplevel(self.root,width=1400,height=800)
         
            RecordMacroBrowser(self.recordingWindow,self.backend,self.child)

    def verifyUserInput(self):
        macroName = self.macroNameField.get()
        url = self.startURLField.get()
        activity = self.activityDropDown.get()
     
        #Determine errors
        errormessage = None
        if macroName == '':
            self.showError(0)
            return False
        for m in self.child.macros:
            if m.name == macroName:
                self.showError(1)
                return False

        self.child.currentMacro = Macro()
        self.child.currentMacro.name = macroName
        self.child.currentMacro.startUrl = url
        for name,id in self.openActs:
            if activity == name:
                self.child.currentMacro.activityId = id
        if self.child.currentMacro.activityId is None:
            self.child.currentMacro = None
            self.showError(2)
            return False

        #debug
        print("current macro name",self.child.currentMacro.name)
        print("current macro activity id",self.child.currentMacro.activityId)
        print("current macro url",self.child.currentMacro.startUrl)
        return True

    def showError(self,id):
        if id is 0:
            #emptyNameError
            errorMessage = "Error: Macro must have a name"

        elif id is 1:
            #duplicateNameError
            errorMessage = "Error: A macro already exists with that name. \n Please use a unique name for the macro."

        elif id is 2:
            #improperActivityError
            errorMessage = "Error: Please select an activity from the dropdown menu. \n If a macro already exists for the desired activity, \n please delete the existing macro before creating a new one."
        print(errorMessage)

        self.createWindow()
        self.errorLabel = Label(self.window, font=self.font,text=errorMessage,borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff')
        self.errorLabel.grid(row=0,column=0,padx=10,pady=10)
       
        photo = Image.open('student/frontEnd/images/okay.png') #open image
        resized = photo.resize((100, 35), Image.ANTIALIAS) #resize
        self.okImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage
        self.okButton = Button(self.window, image=self.okImage, borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff',command=lambda:self.window.destroy())
        self.okButton.grid(row=1,column=0, padx=10, pady=10)

    def getAvailableActivities(self):
        acts = []
        td = datetime.today()
        today = self.backend.formatDate(td)

        for c in self.child.classes:
            activities = c.getActivities()
            for a in activities:
                sItems = a.getScheduleItems()
                for s in sItems:
                    dt = s.getDateTime()
                    adate = self.backend.formatDate(self.backend.formatAsDatetime(dt))
                    print('adate:',adate,'today:',today)
                    if adate == today:
                    #if adate == '04/23/21':
                        if not a.hasMacro:
                            acts.append((c.name + ": " + a.name,a.id))
                            print(a.name,a.id)
        #print(acts)
        return acts

    def createWindow(self):
        if self.window:
            self.window.destroy()
        self.window = tk.Toplevel()
        self.window.attributes('-topmost','true')
        self.window.configure(bg='white')
        self.rootX = self.root.winfo_x()
        self.rootY = self.root.winfo_y()
        self.window.geometry("+%d+%d" % (self.rootX + 350, self.rootY + 350))
            

                        

        






        





