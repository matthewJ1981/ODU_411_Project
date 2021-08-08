from tkinter import *
from tkinter import font as tkFont

class EventLog:
    def __init__(self, mainClass, backEnd):
        print("      Entering Parent - event log screen - /parent/frontEnd/dashboard/pages/eventLog.py")

        def displayAbout():     
            #pageTitle = Label(mainClass.rightFrame, font=('arial', 20, 'bold'), text="Event Log", background="white")
            mainClass.rightFrame.update_idletasks() # Calls all pending idle tasks to get frame sizes
            self.rightFrameWidth = mainClass.rightFrame.winfo_width()
            self.rightFrameHeight = mainClass.rightFrame.winfo_height()
            
            # account information frame (left)
            self.aboutInformationFrame = Frame(mainClass.rightFrame, width=self.rightFrameWidth*0.9, height=self.rightFrameHeight - 100, bd=1, relief="groove")  
            self.aboutInformationFrame.configure(background='white')
            self.aboutInformationFrame.pack(side=LEFT, fill=BOTH, padx=(20), pady=(30))
            self.aboutInformationFrame.pack_propagate(0)

            self.manageAccountTitle = Label(self.aboutInformationFrame, text="Navigation History", background="white", font="bold")
            self.manageAccountTitle.pack()

            self.aboutInformationEntriesFrame = Frame(self.aboutInformationFrame, height=self.rightFrameHeight - 100, bd=0, relief="groove")  
            self.aboutInformationEntriesFrame.configure(background='white')
            self.aboutInformationEntriesFrame.pack(side=LEFT, fill=BOTH, padx=(20), pady=(30))
            self.aboutInformationEntriesFrame.pack_propagate(0)

            #Message
            self.messageLabel = Label(self.aboutInformationEntriesFrame, background="white", font="bold")
            self.messageLabel.grid(row=5,column=0, sticky=W)
            self.text = Text(self.aboutInformationEntriesFrame, height = 20, width=200)
            self.text.grid(row=5,column=1, padx=(20, 0), pady=10)

            def insert(text):
                self.text.insert(END, text + '\n')

            def convert(state):
                if state == 0:
                    return "Failed"
                else:
                    return "Successful"

            for child in backEnd.parent.children:
                insert("Name: " + child.name + "\n")
                #for id, dateTime, navState in child.getLogEntries():
                entries = child.getLogEntries()
                if entries == []:
                    insert("No navigation history for " + child.name + "\n")
                else:
                    for entry in child.getLogEntries():
                        insert(entry.getDateTime() + ", " + convert(entry.getNavState()))
                    insert("")
                    
            # for n, dt, st in backEnd.getLogEntries():
            #     t = str(n) + ", " + str(dt) + ", " + str(st)
            #     print(t)
            #     self.text.insert(END, t + '\n') 

            #text.config(state=DISABLED)

            #pageTitle.pack()
            #self.text.pack()
        
        displayAbout()
