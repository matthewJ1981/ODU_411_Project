import math
import datetime as dt
from tkinter import *
from tkinter import font as tkFont
from PIL import ImageTk,Image 

class ManageStudentSchedule:
    def __init__(self, mainClass, backEnd, onclickMenu):
        print("      Entering Parent - Manage student schedule screen - /parent/frontEnd/dashboard/pages/manageStudentSchedule.py")

        def editButtonClick(x, y, z):
            onclickMenu.childIndex = x
            onclickMenu.classIndex = y
            onclickMenu.classActivityIndex = z
            onclickMenu(9)
        
        def cancelButtonClick():
            onclickMenu(2)

        def addClassButtonClick():
            onclickMenu(11)
        

        def displayManageStudentSchedule():     
            mainClass.rightFrame.update_idletasks() # Calls all pending idle tasks to get frame sizes
            self.rightFrameWidth = mainClass.rightFrame.winfo_width()
            self.rightFrameHeight = mainClass.rightFrame.winfo_height()
            
            # account information frame (left)
            self.scheduleFrame = Frame(mainClass.rightFrame, width=self.rightFrameWidth*0.8, height=self.rightFrameHeight - 100, bd=0)  
            self.scheduleFrame.configure(background='white')

            self.pageTitleLable = Label(self.scheduleFrame, text="Manage Student Schedule", background="white", font="bold")
            self.pageTitleLable.pack()

            self.canvas = Canvas(self.scheduleFrame, width=self.rightFrameWidth*0.7, height=self.rightFrameHeight - 100, bd=0)
            self.canvas.configure(background='white')
            self.canvas.pack(side=LEFT, fill=BOTH, expand="yes")

            self.verticalScrollBar = Scrollbar(self.scheduleFrame, orient="vertical", command=self.canvas.yview)
            self.verticalScrollBar.pack(side=RIGHT, fill="y")

            self.canvas.configure(yscrollcommand=self.verticalScrollBar.set)

            self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))


            self.scheduleListFrame = Frame(self.canvas, bd=0)  
            self.scheduleListFrame.configure(background='white')

            self.canvas.create_window((0,0), window=self.scheduleListFrame, anchor=NW)
            
            self.scheduleFrame.pack(side=LEFT, fill=BOTH, padx=(20), pady=(30))
            self.scheduleFrame.pack_propagate(0)


            children = backEnd.parent.getChildren()
            rowIndex = 0
            
            
            for child in children:
                if child.getID() == onclickMenu.childIndex:
                    studentClasses = child.getClasses()
                    if studentClasses != []:   
                        classIndex = 0          
                        for studentClass in studentClasses:
                            className = studentClass.getName()
                            # activities
                            classActivityIndex = 0 
                            classActivities = studentClass.getActivities()
                            for classActivity in classActivities:
                                activityName = classActivity.getName()
                                scheduleItems = classActivity.getScheduleItems()
                                for scheduleItem in scheduleItems:
                                    schedulDateTime = scheduleItem.getDateTime() # schedule date time
                                    schedulDateTime = backEnd.convertToLocal(backEnd.formatAsDatetime(schedulDateTime)) # convert string to datetime
                                    scheduleStartTime = backEnd.formatTime(schedulDateTime) # start time
                                    scheduleDate = backEnd.formatDate(schedulDateTime)
                                    # schedules
                                    self.classLabel = Label(self.scheduleListFrame, text=str(scheduleStartTime) +  ": " , background="white", font="bold")
                                    self.classLabel.grid(row=rowIndex,column=0, sticky=W)
                                    self.classEntry = Entry(self.scheduleListFrame, width=70)
                                    self.classEntry.grid(row=rowIndex,column=1, padx=(20, 0), pady=10)
                                    self.classEntry.insert(0, "[" + className + "]: " + activityName)
                                    self.editButtonOne= Button(self.scheduleListFrame, width=10, text = "Edit", background="white", font="bold" ,command = lambda child = child, studentClass = studentClass, classActivity = classActivity: editButtonClick(child.getID(), studentClass.getName(), classActivity.getName()))
                                    self.editButtonOne.grid(row=rowIndex,column=2, padx=(10, 0), pady=10)
                                    rowIndex = rowIndex + 1
                                    classActivityIndex = classActivityIndex + 1
                            classIndex = classIndex + 1
     

                   

            self.buttomFrame = Frame(mainClass.rightFrame, width=self.rightFrameWidth*0.2, height=250, bd=0)
            self.buttomFrame.configure(background='white')
            self.buttomFrame.pack(side=RIGHT, fill=X, expand=1, anchor=NE, pady=(30))
            self.buttomFrame.pack_propagate(0)  

            self.addClassButton = Button(self.buttomFrame, width=20, text="Add Class", background="white",command = lambda: addClassButtonClick())
            self.addClassButton.pack(padx=(3,0), pady=(0,5), anchor=W)

            self.cancelButton= Button(self.buttomFrame, width=20, text = "Go Back", background="white",command = lambda: cancelButtonClick())
            self.cancelButton.pack(padx=(3,0), pady=(0,3), anchor=W)   

            
        displayManageStudentSchedule()





