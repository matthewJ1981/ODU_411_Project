import math
from tkinter import *
from tkinter import font as tkFont
from tkinter import messagebox
from PIL import ImageTk,Image

class ManageStudentInfo:
    def __init__(self, mainClass, backEnd, onclickMenu):
        print("      Entering Parent - Manage student info screen - /parent/frontEnd/dashboard/pages/manageStudentInfo.py")

        def updateButtonClick():
            firstName = self.firstNameEntry.get()
            age = self.ageEntry.get()
            skillLevel = self.skillLevelEntry.get()
            pictureFile = self.profilePicEntry.get()
            if(self.profilePicEntry.get()==""):
                pictureFile="student/frontEnd/images/avatar.png"

            children = backEnd.parent.getChildren()
            for child in children:
                if child.getID() == onclickMenu.childIndex:
                    child.setName(firstName)
                    child.setAge(age)
                    child.setSkillLevel(skillLevel)
                    child.setImage(pictureFile)
                    # if self.profilePicEntry.get() == "1":
                    #     # print('student/frontEnd/images/Erin.jpg') 
                    #     child.setImage('student/frontEnd/images/Erin.jpg')
                    # elif self.profilePicEntry.get() == "2":
                    #     # print('student/frontEnd/images/timmy.jpg')
                    #     child.setImage('student/frontEnd/images/timmy.jpg')

            

            messagebox.showinfo(None, "Student information saved successfully")

        def cancelButtonClick():
            onclickMenu(2)

        def deleteButtonClick():
            children = backEnd.parent.getChildren()
            index = 0
            for child in children:
                if child.getID() == onclickMenu.childIndex:
                    backEnd.db.child.remove(child.getID())

            messagebox.showinfo(None, "Student deleted successfully")
            
            

        def displayManageStudentInfo():     
            # backend init
            # backEnd.init()

            # getting parent information
            children = backEnd.parent.getChildren()
            for child in children:
                if child.getID() == onclickMenu.childIndex:
                    self.childName = child.getName()
                    self.childAge = child.getAge()
                    self.childSkillLevel = child.getSkillLevel()


            mainClass.rightFrame.update_idletasks() # Calls all pending idle tasks to get frame sizes
            self.rightFrameWidth = mainClass.rightFrame.winfo_width()
            self.rightFrameHeight = mainClass.rightFrame.winfo_height()
            
            # account information frame (left)
            self.accountInformationFrame = Frame(mainClass.rightFrame, width=self.rightFrameWidth*0.7, height=self.rightFrameHeight - 100, bd=1, relief="groove")  
            self.accountInformationFrame.configure(background='white')
            self.accountInformationFrame.pack(side=LEFT, fill=BOTH, padx=(20), pady=(30))
            self.accountInformationFrame.pack_propagate(0)

            self.manageAccountTitle = Label(self.accountInformationFrame, text="Manage Student Info", background="white", font="bold")
            self.manageAccountTitle.pack()

            self.accountInformationEntriesFrame = Frame(self.accountInformationFrame, height=self.rightFrameHeight - 100, bd=0, relief="groove")  
            self.accountInformationEntriesFrame.configure(background='white')
            self.accountInformationEntriesFrame.pack(side=LEFT, fill=BOTH, padx=(20), pady=(30))
            self.accountInformationEntriesFrame.pack_propagate(0)

            self.firstNameLabel = Label(self.accountInformationEntriesFrame, text="First Name: ", background="white", font="bold")
            self.firstNameLabel.grid(row=0,column=0, sticky=W)
            self.firstNameEntry = Entry(self.accountInformationEntriesFrame, width=30)
            self.firstNameEntry.grid(row=0,column=1, padx=(20, 0), pady=10)
            self.firstNameEntry.insert(0, self.childName)

            self.lastNameLabel = Label(self.accountInformationEntriesFrame, text="Last Name: ", background="white", font="bold")
            self.lastNameLabel.grid(row=1,column=0, sticky=W)
            self.lastNameEntry = Entry(self.accountInformationEntriesFrame, width=30)
            self.lastNameEntry.grid(row=1,column=1, padx=(20, 0), pady=10)
            self.lastNameEntry.insert(0, backEnd.parent.getLastName())

            self.ageLabel = Label(self.accountInformationEntriesFrame, text="Age: ", background="white", font="bold")
            self.ageLabel.grid(row=2,column=0, sticky=W)
            self.ageEntry = Entry(self.accountInformationEntriesFrame, width=30)
            self.ageEntry.grid(row=2,column=1, padx=(20, 0), pady=10)
            self.ageEntry.insert(0, self.childAge)
        
            self.skillLevelLabel = Label(self.accountInformationEntriesFrame, text="Skill Level: ", background="white", font="bold")
            self.skillLevelLabel.grid(row=3,column=0, sticky=W)
            self.skillLevelEntry = Entry(self.accountInformationEntriesFrame, width=30)
            self.skillLevelEntry.grid(row=3,column=1, padx=(20, 0), pady=10)
            self.skillLevelEntry.insert(0, self.childSkillLevel)

            self.profilePicLabel = Label(self.accountInformationEntriesFrame, text="Profile Image: ", background="white", font="bold")
            self.profilePicLabel.grid(row=4,column=0, sticky=W)
            self.profilePicEntry = Entry(self.accountInformationEntriesFrame, width=30)
            self.profilePicEntry.grid(row=4,column=1, padx=(20, 0), pady=10)

            # photo = Image.open('student/frontEnd/images/Erin.jpg') #open image
            # resized = photo.resize((175, 175), Image.ANTIALIAS) #resize
            # correctedImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage        
            # self.pictureFrame = Label(self.accountInformationEntriesFrame, text="#1", image=correctedImage, anchor=NE, bg="white")
            # self.pictureFrame.image = correctedImage #do this so image isnt lost in garbage collection
            # self.pictureFrame.grid(row = 5, column = 1, sticky="W")
            # self.pictureFrameLabel = Label(self.accountInformationEntriesFrame, text="Option #1: ", background="white", font="bold")
            # self.pictureFrameLabel.grid(row=7,column=1, sticky=W)

            # photo = Image.open('student/frontEnd/images/timmy.jpg') #open image
            # resized = photo.resize((175, 175), Image.ANTIALIAS) #resize
            # correctedImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage        
            # self.pictureFrame2 = Label(self.accountInformationEntriesFrame, text="#2", image=correctedImage, anchor=NE, bg="white")
            # self.pictureFrame2.image = correctedImage #do this so image isnt lost in garbage collection
            # self.pictureFrame2.grid(row = 9, column = 1, sticky="W")
            # self.pictureFrame2Label = Label(self.accountInformationEntriesFrame, text="Option #2: ", background="white", font="bold")
            # self.pictureFrame2Label.grid(row=11,column=1, sticky=W)
         

            self.updateButton= Button(self.accountInformationFrame, width=20, text = "UPDATE", background="white", font="bold" ,command = lambda: updateButtonClick())
            self.updateButton.pack(side=BOTTOM, padx=(20), pady=(30))

            self.cancelButton= Button(self.accountInformationFrame, width=20, text = "CANCEL", background="white", font="bold" ,command = lambda: cancelButtonClick())
            self.cancelButton.pack(side=BOTTOM, padx=(20), pady=(30))  

            self.deleteButton= Button(self.accountInformationFrame, width=20, text = "DELETE STUDENT", background="white", font="bold" ,command = lambda: deleteButtonClick())
            self.deleteButton.pack(side=BOTTOM, padx=(20), pady=(30))

        displayManageStudentInfo()





