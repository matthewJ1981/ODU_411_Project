import math
from tkinter import *
from tkinter import font as tkFont
from tkinter import messagebox
from datetime import datetime, timedelta, date

class ManageStudentClass:
    def __init__(self, mainClass, backEnd, onclickMenu):
        print("      Entering Parent - Manage student class screen - /parent/frontEnd/dashboard/pages/manageStudentClass.py")

        
        def updateButtonClick():
            
            title = self.titleEntry.get()
            activity = self.activityEntry.get()
            link = self.linkEntry.get()
            print(link)
            #time = self.timeEntry.get()
            time="1:30:00 PM"
            a=datetime.strptime(time,'%I:%M:%S %p')
            now=datetime.utcnow().isoformat()
            newTime=now[:10]+str(a)[10:]+"-0400"
            newTimeDateTime=datetime.strptime(newTime, '%Y-%m-%d %H:%M:%S%z')

            children = backEnd.parent.getChildren()
            for child in children:
                if child.getID() == onclickMenu.childIndex:
                    studentClasses = child.getClasses()
                    if studentClasses != []:                
                        for studentClass in studentClasses:
                            if(studentClass.getName() == onclickMenu.classIndex):
                                studentClass.setName(title)
                                classActivities = studentClass.getActivities()
                                for classActivity in classActivities:
                                    if(classActivity.getName() == onclickMenu.classActivityIndex):
                                        classActivity.setName(activity)
                                        classActivity.setURL(link)
                                        scheduleItems = classActivity.getScheduleItems()                
                                        for scheduleItem in scheduleItems:
                                            scheduleItem.setDateTIme(backEnd.formatAsString(newTimeDateTime))
                                            

            messagebox.showinfo(None, "Class information saved successfully")

        def cancelButtonClick():
            onclickMenu(7)
            

        def displayManageStudentClass():
            # backend init
            # backEnd.init()

            # getting parent information
            # self.parentUserName = backEnd.parent.getUserName()
            # self.parentEmail = backEnd.parent.getEmail()
            # self.parentFirstName = backEnd.parent.getFirstName()
            # self.parentLastName = backEnd.parent.getLastName()
            # self.parentPhoneNumber = backEnd.parent.getPhoneNumber()

            mainClass.rightFrame.update_idletasks() # Calls all pending idle tasks to get frame sizes
            self.rightFrameWidth = mainClass.rightFrame.winfo_width()
            self.rightFrameHeight = mainClass.rightFrame.winfo_height()
            
            # account information frame (left)
            self.accountInformationFrame = Frame(mainClass.rightFrame, width=self.rightFrameWidth*0.7, height=self.rightFrameHeight - 100, bd=1, relief="groove")
            self.accountInformationFrame.configure(background='white')
            self.accountInformationFrame.pack(side=LEFT, fill=BOTH, padx=(20), pady=(30))
            self.accountInformationFrame.pack_propagate(0)

            self.manageAccountTitle = Label(self.accountInformationFrame, text="Manage Student Class", background="white", font="bold")
            self.manageAccountTitle.pack()

            self.accountInformationEntriesFrame = Frame(self.accountInformationFrame, height=self.rightFrameHeight - 100, bd=0, relief="groove")
            self.accountInformationEntriesFrame.configure(background='white')
            self.accountInformationEntriesFrame.pack(side=LEFT, fill=BOTH, padx=(20), pady=(30))
            self.accountInformationEntriesFrame.pack_propagate(0)

            children = backEnd.parent.getChildren()
            className = ""
            activityName = ""
            linkName = ""
            activityTime = ""
            for child in children:
                if child.getID() == onclickMenu.childIndex:
                    studentClasses = child.getClasses()
                    if studentClasses != []:                
                        for studentClass in studentClasses:
                            if(studentClass.getName() == onclickMenu.classIndex):
                                className = studentClass.getName()
                                # activities
                                classActivities = studentClass.getActivities() 
                                for classActivity in classActivities:
                                    scheduleItems = classActivity.getScheduleItems() 
                                    for scheduleItem in scheduleItems:
                                        schedulDateTime = scheduleItem.getDateTime()
                                        schedulDateTime = backEnd.convertToLocal(backEnd.formatAsDatetime(schedulDateTime))
                                        scheduleStartTime = backEnd.formatTime(schedulDateTime)
                                        if(classActivity.getName() == onclickMenu.classActivityIndex):
                                            activityName = classActivity.getName()
                                            linkName = classActivity.getURL()
                                            activityTime=scheduleStartTime

                                        
            

            self.rightFrameHeight = mainClass.rightFrame.winfo_height()

            self.titleLabel = Label(self.accountInformationEntriesFrame, text="Title: ", background="white", font="bold")
            self.titleLabel.grid(row=0,column=0, sticky=W)
            self.titleEntry = Entry(self.accountInformationEntriesFrame, width=100)
            self.titleEntry.grid(row=0,column=1, padx=(20, 0), pady=10)
            self.titleEntry.insert(0, className)

            self.activityLabel = Label(self.accountInformationEntriesFrame, text="Activity: ", background="white", font="bold")
            self.activityLabel.grid(row=1,column=0, sticky=W)
            self.activityEntry = Entry(self.accountInformationEntriesFrame, width=100)
            self.activityEntry.grid(row=1,column=1, padx=(20, 0), pady=10)
            self.activityEntry.insert(0, activityName)

            self.linkLabel = Label(self.accountInformationEntriesFrame, text="Link: ", background="white", font="bold")
            self.linkLabel.grid(row=2,column=0, sticky=W)
            self.linkEntry = Entry(self.accountInformationEntriesFrame, width=100)
            self.linkEntry.grid(row=2,column=1, padx=(20, 0), pady=10)

            self.linkEntry.insert(0, linkName)


            self.timeLabel = Label(self.accountInformationEntriesFrame, text="Time: ", background="white", font="bold")
            self.timeLabel.grid(row=3,column=0, sticky=W)
            self.timeEntry = Entry(self.accountInformationEntriesFrame, width=100)
            self.timeEntry.grid(row=3,column=1, padx=(20, 0), pady=10)
            self.timeEntry.insert(0, activityTime)


            self.rightFrameHeight = mainClass.rightFrame.winfo_height()

           

            self.accountInformationFrameRight = Frame(mainClass.rightFrame, width=self.rightFrameWidth*0.3, height=250, bd=1, relief="groove")
            self.accountInformationFrameRight.configure(background='white')
            self.accountInformationFrameRight.pack(side=TOP, fill=X, expand=1, anchor=NE, padx=(10), pady=(5))
            self.accountInformationFrameRight.pack_propagate(0)



            cancelButton = Button(self.accountInformationFrameRight, text="CANCEL", background="white",command = lambda: cancelButtonClick())
            cancelButton.pack(padx=(3,0), pady=(0,2), anchor=W)
            
            updateButton = Button(self.accountInformationFrameRight, text="UPDATE", background="white",command = lambda: updateButtonClick())
            updateButton.pack(padx=(3,0), pady=(0,2), anchor=W)


            
        displayManageStudentClass()
