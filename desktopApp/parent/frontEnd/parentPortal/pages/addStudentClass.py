import math
from tkinter import *
from tkinter import font as tkFont
from tkinter import messagebox

class AddStudentClass:
    def __init__(self, mainClass, backEnd, onclickMenu):
        print("      Entering Parent - Add student class screen - /parent/frontEnd/dashboard/pages/addStudentClass.py")

        
        def saveButtonClick():
            
            title = self.titleEntry.get()
            teacher = self.teacherEntry.get()
            activity = self.activityEntry.get()
            link = self.linkEntry.get()
            time = self.timeEntry.get()
            duration = self.durationEntry.get()

            children = backEnd.parent.getChildren()
            for child in children:
                if child.getID() == onclickMenu.childIndex:
                    child.addClass(title, teacher)
                    #if studentClasses != []:                
                        #for studentClass in studentClasses:
                    for studentClass in child.getClasses():
                        if(studentClass.getName() == title and studentClass.getTeacherName() == teacher):
                            studentClass.addActivity(activity)
                            classActivities = studentClass.getActivities()
                            for classActivity in classActivities:
                                if(classActivity.getName() == activity):
                                    # classActivity.setURL(link)
                                    classActivity.addScheduleItem(time, duration)
                                            

            messagebox.showinfo(None, "Class added successfully")

        def cancelButtonClick():
            onclickMenu(7)
            

        def displayAddStudentClass():
            # backend init
            # backEnd.init()


            mainClass.rightFrame.update_idletasks() # Calls all pending idle tasks to get frame sizes
            self.rightFrameWidth = mainClass.rightFrame.winfo_width()
            self.rightFrameHeight = mainClass.rightFrame.winfo_height()
            
            # account information frame (left)
            self.accountInformationFrame = Frame(mainClass.rightFrame, width=self.rightFrameWidth*0.7, height=self.rightFrameHeight - 100, bd=1, relief="groove")
            self.accountInformationFrame.configure(background='white')
            self.accountInformationFrame.pack(side=LEFT, fill=BOTH, padx=(20), pady=(30))
            self.accountInformationFrame.pack_propagate(0)

            self.manageAccountTitle = Label(self.accountInformationFrame, text="Add Student Class", background="white", font="bold")
            self.manageAccountTitle.pack()

            self.accountInformationEntriesFrame = Frame(self.accountInformationFrame, height=self.rightFrameHeight - 100, bd=0, relief="groove")
            self.accountInformationEntriesFrame.configure(background='white')
            self.accountInformationEntriesFrame.pack(side=LEFT, fill=BOTH, padx=(20), pady=(30))
            self.accountInformationEntriesFrame.pack_propagate(0)

            self.titleLabel = Label(self.accountInformationEntriesFrame, text="Title: ", background="white", font="bold")
            self.titleLabel.grid(row=0,column=0, sticky=W)
            self.titleEntry = Entry(self.accountInformationEntriesFrame, width=30)
            self.titleEntry.grid(row=0,column=1, padx=(20, 0), pady=10)

            self.teacherLabel = Label(self.accountInformationEntriesFrame, text="Teacher Name: ", background="white", font="bold")
            self.teacherLabel.grid(row=1,column=0, sticky=W)
            self.teacherEntry = Entry(self.accountInformationEntriesFrame, width=30)
            self.teacherEntry.grid(row=1,column=1, padx=(20, 0), pady=10)

            self.activityLabel = Label(self.accountInformationEntriesFrame, text="Activity: ", background="white", font="bold")
            self.activityLabel.grid(row=2,column=0, sticky=W)
            self.activityEntry = Entry(self.accountInformationEntriesFrame, width=30)
            self.activityEntry.grid(row=2,column=1, padx=(20, 0), pady=10)

            self.linkLabel = Label(self.accountInformationEntriesFrame, text="Link: ", background="white", font="bold")
            self.linkLabel.grid(row=3,column=0, sticky=W)
            self.linkEntry = Entry(self.accountInformationEntriesFrame, width=30)
            self.linkEntry.grid(row=3 ,column=1, padx=(20, 0), pady=10)

            self.timeLabel = Label(self.accountInformationEntriesFrame, text="Time: ", background="white", font="bold")
            self.timeLabel.grid(row=4,column=0, sticky=W)
            self.timeEntry = Entry(self.accountInformationEntriesFrame, width=30)
            self.timeEntry.grid(row=4,column=1, padx=(20, 0), pady=10)
            
            self.durationLabel = Label(self.accountInformationEntriesFrame, text="Duration: ", background="white", font="bold")
            self.durationLabel.grid(row=5,column=0, sticky=W)
            self.durationEntry = Entry(self.accountInformationEntriesFrame, width=30)
            self.durationEntry.grid(row=5,column=1, padx=(20, 0), pady=10)

            
            

            self.rightFrameHeight = mainClass.rightFrame.winfo_height()

           

            accountInformationFrame = Frame(mainClass.rightFrame, width=self.rightFrameWidth*0.3, height=250, bd=1, relief="groove")
            accountInformationFrame.configure(background='white')
            accountInformationFrame.pack(side=TOP, fill=X, expand=1, anchor=NE, padx=(10), pady=(5))
            accountInformationFrame.pack_propagate(0)


            cancelButton = Button(accountInformationFrame, text="CANCEL", background="white",command = lambda: cancelButtonClick())
            cancelButton.pack(padx=(3,0), pady=(0,3), anchor=W)
            
            saveButton = Button(accountInformationFrame, text="SAVE", background="white",command = lambda: saveButtonClick())
            saveButton.pack(padx=(3,0), pady=(0,3), anchor=W)

            

            
        displayAddStudentClass()
