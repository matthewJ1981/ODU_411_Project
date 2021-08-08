import math
from tkinter import *
from tkinter import font as tkFont
from tkinter import messagebox

class ManageAccount:
    def __init__(self, mainClass, backEnd):
        print("      Entering Parent - Manage Account screen - /parent/frontEnd/dashboard/pages/manageAccount.py")

        def saveButtonClick():
            email = self.emailEntry.get()
            firstName = self.firstNameEntry.get()
            lastName = self.lastNameEntry.get()
            phoneNumber = self.phoneNumberEntry.get()

            backEnd.parent.setEmail(email)
            backEnd.parent.setFirstName(firstName)
            backEnd.parent.setLastName(lastName)
            backEnd.parent.setPhoneNumber(phoneNumber)

            messagebox.showinfo(None, "Account information saved successfully")
            

        def displayManageAccount():     
            # backend init
            # backEnd.init()

            # getting parent information
            self.parentUserName = backEnd.parent.getUserName()
            self.parentEmail = backEnd.parent.getEmail()
            self.parentFirstName = backEnd.parent.getFirstName()
            self.parentLastName = backEnd.parent.getLastName()
            self.parentPhoneNumber = backEnd.parent.getPhoneNumber()

            mainClass.rightFrame.update_idletasks() # Calls all pending idle tasks to get frame sizes
            self.rightFrameWidth = mainClass.rightFrame.winfo_width()
            self.rightFrameHeight = mainClass.rightFrame.winfo_height()
            
            # account information frame (left)
            self.accountInformationFrame = Frame(mainClass.rightFrame, width=self.rightFrameWidth*0.7, height=self.rightFrameHeight - 100, bd=1, relief="groove")  
            self.accountInformationFrame.configure(background='white')
            self.accountInformationFrame.pack(side=LEFT, fill=BOTH, padx=(20), pady=(30))
            self.accountInformationFrame.pack_propagate(0)

            self.manageAccountTitle = Label(self.accountInformationFrame, text="Manage Account", background="white", font="bold")
            self.manageAccountTitle.pack()

            self.accountInformationEntriesFrame = Frame(self.accountInformationFrame, height=self.rightFrameHeight - 100, bd=0, relief="groove")  
            self.accountInformationEntriesFrame.configure(background='white')
            self.accountInformationEntriesFrame.pack(side=LEFT, fill=BOTH, padx=(20), pady=(30))
            self.accountInformationEntriesFrame.pack_propagate(0)

            self.userNameLabel = Label(self.accountInformationEntriesFrame, text="User Name: ", background="white", font="bold")
            self.userNameLabel.grid(row=0,column=0, sticky=W)
            self.userNameLabel = Label(self.accountInformationEntriesFrame, text=self.parentUserName, background="white", font="bold")
            self.userNameLabel.grid(row=0,column=1, sticky=W, padx=(20, 0), pady=10)

            self.emailLabel = Label(self.accountInformationEntriesFrame, text="Email: ", background="white", font="bold")
            self.emailLabel.grid(row=1,column=0, sticky=W)
            self.emailEntry = Entry(self.accountInformationEntriesFrame, width=30)
            self.emailEntry.grid(row=1,column=1, padx=(20, 0), pady=10)
            self.emailEntry.insert(0, self.parentEmail)

            self.firstNameLabel = Label(self.accountInformationEntriesFrame, text="First Name: ", background="white", font="bold")
            self.firstNameLabel.grid(row=2,column=0, sticky=W)
            self.firstNameEntry = Entry(self.accountInformationEntriesFrame, width=30)
            self.firstNameEntry.grid(row=2,column=1, padx=(20, 0), pady=10)
            self.firstNameEntry.insert(0, self.parentFirstName)
        
            self.lastNameLabel = Label(self.accountInformationEntriesFrame, text="Last Name: ", background="white", font="bold")
            self.lastNameLabel.grid(row=3,column=0, sticky=W)
            self.lastNameEntry = Entry(self.accountInformationEntriesFrame, width=30)
            self.lastNameEntry.grid(row=3,column=1, padx=(20, 0), pady=10)
            self.lastNameEntry.insert(0, self.parentLastName)

            self.phoneNumberLabel = Label(self.accountInformationEntriesFrame, text="Phone Number: ", background="white", font="bold")
            self.phoneNumberLabel.grid(row=4,column=0, sticky=W)
            self.phoneNumberEntry = Entry(self.accountInformationEntriesFrame, width=30)
            self.phoneNumberEntry.grid(row=4,column=1, padx=(20, 0), pady=10)
            self.phoneNumberEntry.insert(0, self.parentPhoneNumber)

            self.saveButton= Button(self.accountInformationFrame, width=20, text = "SAVE", background="white", font="bold" ,command = lambda: saveButtonClick())
            self.saveButton.pack(side=BOTTOM, padx=(20), pady=(30))

        displayManageAccount()





