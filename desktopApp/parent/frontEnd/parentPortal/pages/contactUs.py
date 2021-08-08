import math
import smtplib
import ssl
from tkinter import *
from tkinter import font as tkFont
from tkinter import messagebox
from email.mime.text import MIMEText

class ContactUs:
    def __init__(self, mainClass, backEnd):
        print("      Entering Parent - Contact Us screen - /parent/frontEnd/dashboard/pages/contactUs.py")

        def saveButtonClick():
            string = '\n\n\n' + self.messageEntry.get(1.0, 'end-1c') + '\n\n\nParent Name: ' + self.firstNameEntry.get() + ' ' + self.lastNameEntry.get() + '\nParent Email: ' + self.emailEntry.get() + '\nParent Phone #: ' + self.phoneNumberEntry.get() 
            msg = MIMEText(string, 'plain')
            msg['Subject'] = 'Message from littleLEARNERs Parent: ' + self.firstNameEntry.get() + ' ' + self.lastNameEntry.get()

            #login
            port = 465
            my_mail = 'littlelearners411@gmail.com'
            my_password = '!!littleLEARNERS!!'
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
                server.login(my_mail, my_password)
                server.sendmail(self.emailEntry.get(), my_mail, msg.as_string())

        
            
        
        def displayContactUs():     
            # pageTitle = Label(mainClass.rightFrame, font=('arial', 70, 'bold'), text="About", background="white")
            # pageTitle.pack()    
            # backend init
            # backEnd.init()

            mainClass.rightFrame.update_idletasks() # Calls all pending idle tasks to get frame sizes
            self.rightFrameWidth = mainClass.rightFrame.winfo_width()
            self.rightFrameHeight = mainClass.rightFrame.winfo_height()
            
            # account information frame (left)
            self.aboutInformationFrame = Frame(mainClass.rightFrame, width=self.rightFrameWidth*0.7, height=self.rightFrameHeight - 100, bd=1, relief="groove")  
            self.aboutInformationFrame.configure(background='white')
            self.aboutInformationFrame.pack(side=LEFT, fill=BOTH, padx=(20), pady=(30))
            self.aboutInformationFrame.pack_propagate(0)

            self.manageAccountTitle = Label(self.aboutInformationFrame, text="Contact Us", background="white", font="bold")
            self.manageAccountTitle.pack()

            self.aboutInformationEntriesFrame = Frame(self.aboutInformationFrame, height=self.rightFrameHeight - 100, bd=0, relief="groove")  
            self.aboutInformationEntriesFrame.configure(background='white')
            self.aboutInformationEntriesFrame.pack(side=LEFT, fill=BOTH, padx=(20), pady=(30))
            self.aboutInformationEntriesFrame.pack_propagate(0)

            #Email
            self.emailLabel = Label(self.aboutInformationEntriesFrame, text="Email: ", background="white", font="bold")
            self.emailLabel.grid(row=1,column=0, sticky=W)
            self.emailEntry = Entry(self.aboutInformationEntriesFrame, width=30)
            self.emailEntry.grid(row=1,column=1, padx=(20, 0), pady=10)

            #First Name
            self.firstNameLabel = Label(self.aboutInformationEntriesFrame, text="First Name: ", background="white", font="bold")
            self.firstNameLabel.grid(row=2,column=0, sticky=W)
            self.firstNameEntry = Entry(self.aboutInformationEntriesFrame, width=30)
            self.firstNameEntry.grid(row=2,column=1, padx=(20, 0), pady=10)
        
            #Last Name
            self.lastNameLabel = Label(self.aboutInformationEntriesFrame, text="Last Name: ", background="white", font="bold")
            self.lastNameLabel.grid(row=3,column=0, sticky=W)
            self.lastNameEntry = Entry(self.aboutInformationEntriesFrame, width=30)
            self.lastNameEntry.grid(row=3,column=1, padx=(20, 0), pady=10)

            #Phone Number
            self.phoneNumberLabel = Label(self.aboutInformationEntriesFrame, text="Phone Number: ", background="white", font="bold")
            self.phoneNumberLabel.grid(row=4,column=0, sticky=W)
            self.phoneNumberEntry = Entry(self.aboutInformationEntriesFrame, width=30)
            self.phoneNumberEntry.grid(row=4,column=1, padx=(20, 0), pady=10)

            #Message
            self.messageLabel = Label(self.aboutInformationEntriesFrame, text="Message: ", background="white", font="bold")
            self.messageLabel.grid(row=5,column=0, sticky=W)
            self.messageEntry = Text(self.aboutInformationEntriesFrame, height = 10, width=60, bd=1, relief="groove")
            self.messageEntry.grid(row=5,column=1, padx=(20, 0), pady=10)

            #Send Button
            self.sendButton= Button(self.aboutInformationFrame, width=20, text = "SEND", background="white", font="bold" ,command = lambda: saveButtonClick())
            self.sendButton.pack(side=BOTTOM, padx=(20), pady=(30))

        displayContactUs()





