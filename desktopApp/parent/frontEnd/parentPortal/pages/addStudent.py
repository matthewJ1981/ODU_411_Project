import math
from tkinter import *
from tkinter import font as tkFont
from tkinter import messagebox

class AddStudent:
    def __init__(self, mainClass, backEnd, onclickMenu):
        print("      Entering Parent - Add new student screen - /parent/frontEnd/dashboard/pages/addStudent.py")

        def addButtonClick():

            backEnd.parent.addChild(self.firstNameEntry.get(), self.ageEntry.get())
            children = backEnd.parent.getChildren()
            x = 0
            for child in children:
                x = x + 1
            children[0].setSkillLevel(self.skillLevelEntry.get)


            messagebox.showinfo(None, "New student added successfully")

        def cancelButtonClick():
            onclickMenu(2)
            

        def displayAddStudent():     
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

            self.manageAccountTitle = Label(self.accountInformationFrame, text="Add New Student", background="white", font="bold")
            self.manageAccountTitle.pack()

            self.accountInformationEntriesFrame = Frame(self.accountInformationFrame, height=self.rightFrameHeight - 100, bd=0, relief="groove")  
            self.accountInformationEntriesFrame.configure(background='white')
            self.accountInformationEntriesFrame.pack(side=LEFT, fill=BOTH, padx=(20), pady=(30))
            self.accountInformationEntriesFrame.pack_propagate(0)

            self.firstNameLabel = Label(self.accountInformationEntriesFrame, text="First Name: ", background="white", font="bold")
            self.firstNameLabel.grid(row=0,column=0, sticky=W)
            self.firstNameEntry = Entry(self.accountInformationEntriesFrame, width=30)
            self.firstNameEntry.grid(row=0,column=1, padx=(20, 0), pady=10)

            self.ageLabel = Label(self.accountInformationEntriesFrame, text="Age: ", background="white", font="bold")
            self.ageLabel.grid(row=1,column=0, sticky=W)
            self.ageEntry = Entry(self.accountInformationEntriesFrame, width=30)
            self.ageEntry.grid(row=1,column=1, padx=(20, 0), pady=10)
            # self.firstNameEntry.insert(0, self.parentFirstName)
        
            self.skillLevelLabel = Label(self.accountInformationEntriesFrame, text="Skill Level: ", background="white", font="bold")
            self.skillLevelLabel.grid(row=2,column=0, sticky=W)
            self.skillLevelEntry = Entry(self.accountInformationEntriesFrame, width=30)
            self.skillLevelEntry.grid(row=2,column=1, padx=(20, 0), pady=10)
            # self.lastNameEntry.insert(0, self.parentLastName)

            # self.schoolLabel = Label(self.accountInformationEntriesFrame, text="School: ", background="white", font="bold")
            # self.schoolLabel.grid(row=3,column=0, sticky=W)
            # self.schoolEntry = Entry(self.accountInformationEntriesFrame, width=30)
            # self.schoolEntry.grid(row=3,column=1, padx=(20, 0), pady=10)
            # # self.phoneNumberEntry.insert(0, self.parentPhoneNumber)

            # self.schoolEmailLabel = Label(self.accountInformationEntriesFrame, text="School Email: ", background="white", font="bold")
            # self.schoolEmailLabel.grid(row=4,column=0, sticky=W)
            # self.schoolEmailEntry = Entry(self.accountInformationEntriesFrame, width=30)
            # self.schoolEmailEntry.grid(row=4,column=1, padx=(20, 0), pady=10)
            # # self.emailEntry.insert(0, self.parentEmail)

            # self.teacherLabel = Label(self.accountInformationEntriesFrame, text="Teacher: ", background="white", font="bold")
            # self.teacherLabel.grid(row=5,column=0, sticky=W)
            # self.teacherEntry = Entry(self.accountInformationEntriesFrame, width=30)
            # self.teacherEntry.grid(row=5,column=1, padx=(20, 0), pady=10)
            # # self.firstNameEntry.insert(0, self.parentFirstName)
        
            # self.teacherEmailLabel = Label(self.accountInformationEntriesFrame, text="Teacher Email: ", background="white", font="bold")
            # self.teacherEmailLabel.grid(row=6,column=0, sticky=W)
            # self.teacherEmailEntry = Entry(self.accountInformationEntriesFrame, width=30)
            # self.teacherEmailEntry.grid(row=6,column=1, padx=(20, 0), pady=10)
            # # self.lastNameEntry.insert(0, self.parentLastName)
          

            self.addButton= Button(self.accountInformationFrame, width=20, text = "ADD", background="white", font="bold" ,command = lambda: addButtonClick())
            self.addButton.pack(side=BOTTOM, padx=(20), pady=(30))

            self.cancelButton= Button(self.accountInformationFrame, width=20, text = "CANCEL", background="white", font="bold" ,command = lambda: cancelButtonClick())
            self.cancelButton.pack(side=BOTTOM, padx=(20), pady=(30))  

        displayAddStudent()





