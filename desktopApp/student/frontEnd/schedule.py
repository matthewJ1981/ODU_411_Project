from tkinter import *
import sys
import os
from PIL import ImageTk,Image
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
from time import strftime
from datetime import datetime

class Schedule(tk.Frame):

   #def __init__(self, *args, **kwargs):
   def __init__(self, root, backend):           

        tk.Frame.__init__(self, root)

        #self.rowconfigure((0,1,2,3,4), weight=1)
        self.columnconfigure((0, 1, 2), weight=1)
        self.configure(bg="white")     
        
        now = datetime.now()
        td = datetime.today()
        today = td.strftime("%m/%d/%y")
        self.title = Label(self, font = ('montserrat', 35, 'bold'), text=("Today's Date is " + now.strftime("%a %B %d, %y")), foreground="#1B1B1B", background="#ffffff")
        self.title.grid(row=0, column = 0, columnspan=3, sticky="nsew")
        self.scheduleActivities = []
        #self.title2 = Label(self, font = ('montserrat', 35, 'bold'), text=(backend.parent.children[backend.currChild].name), foreground="#1B1B1B", background="#ffffff")
        #self.title2.grid(row=1, column = 1, columnspan=3, sticky="N")
        

        # studentInfoFrame = Frame(self, width=600, height=250)  
        # studentInfoFrame.configure(background='green')
        # studentInfoFrame.grid(row=1, column=1, columnspan=3, sticky="nsew")
        # studentInfoFrame.pack_propagate(0)


        backend.checkCalendarUpdate()

        child = backend.parent.children[backend.currChild]
        rowIndex = 2 
        studentClasses = backend.parent.children[backend.currChild].getClasses()
        if studentClasses != []:   
            classIndex = 0          
            for studentClass in studentClasses:
                className = studentClass.getName()
                # activities
                classActivityIndex = 0 
                classActivities = studentClass.getActivities()
                for classActivity in classActivities:
                    activityName = classActivity.getName()
                    # schedules
                    scheduleItemIndex = 0
                    scheduleItems = classActivity.getScheduleItems()                
                    for scheduleItem in scheduleItems:
                        schedulDateTime = scheduleItem.getDateTime() # schedule date time
                        tempUTC = backend.formatAsDatetime(schedulDateTime)
                        tempUTC = tempUTC.strftime("%H:%M:%S")
                        utcTime = datetime.strptime(tempUTC,"%H:%M:%S")
                        schedulDateTime = backend.convertToLocal(backend.formatAsDatetime(schedulDateTime)) # convert string to datetime
                        #schedulDateTime = backend.formatAsDatetime(schedulDateTime)
                        scheduleStartTime = backend.formatTime(schedulDateTime) # start time
                        scheduleDate = backend.formatDate(schedulDateTime)

                        #*********test date below - comment line 68/69 and uncomment 70 for real date
                        #testscheduleDate = '04/18/21'
                        #if testscheduleDate == scheduleDate:
                        if today == scheduleDate:
                            tempItem = ActivityItem()
                            tempItem.cName = className
                            tempItem.aName = activityName
                            tempItem.startTime = scheduleStartTime
                            tempItem.utcStart = utcTime
                            self.scheduleActivities.append(tempItem)
                                                 

                        rowIndex = rowIndex + 1
                        scheduleItemIndex = scheduleItemIndex + 1
                    classActivityIndex = classActivityIndex + 1
                classIndex = classIndex + 1

            self.scheduleActivities.sort(key=lambda x: x.utcStart)
            self.displaySchedule()

   def displaySchedule(self):
       for i,s in enumerate(self.scheduleActivities):
           print(s.cName,s.aName,s.startTime)
           self.classTime = Label(self, text=str(s.startTime) +  ": " , background="white", font = ('montserrat', 20, 'bold'))
           self.classTime.grid(row=i+2,column=0, sticky=N, pady=10)
           self.classDetails = Label(self, text= s.cName +  ": " + s.aName, background="white", font = ('montserrat', 20, 'bold'))
           self.classDetails.grid(row=i+2, column=1, padx=(20, 0), sticky=N, pady=10)

        

class ActivityItem:
    def __init__(self):
        self.cName = None
        self.aName = None
        self.startTime = None
        self.utcStart = None



 
        
        