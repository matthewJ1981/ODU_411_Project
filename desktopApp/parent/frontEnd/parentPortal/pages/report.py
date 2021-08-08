import math
from tkinter import *
from tkinter import font as tkFont

class Report:
    def __init__(self, mainClass, backEnd):
        print("      Entering Parent - event log screen - /parent/frontEnd/dashboard/pages/report.py")

        def displayAbout():     
            mainClass.rightFrame.update_idletasks() # Calls all pending idle tasks to get frame sizes
            self.rightFrameWidth = mainClass.rightFrame.winfo_width()
            self.rightFrameHeight = mainClass.rightFrame.winfo_height()
            print(self.rightFrameWidth)
            print(self.rightFrameHeight)
            
            self.messageFrame = Frame(mainClass.rightFrame, width=self.rightFrameWidth*0.9, height=self.rightFrameHeight - 100, bd=1, relief="groove")  
            self.messageFrame.configure(background='white')
            self.messageFrame.pack(side=LEFT, fill=BOTH, padx=(20), pady=(30))
            self.messageFrame.pack_propagate(0)
            self.messageFrame.update_idletasks() # Calls all pending idle tasks to get frame sizes

            self.reportTitle = Label(self.messageFrame, text="Report", background="white", font="bold")
            self.reportTitle.pack()

            self.messageFrameWidth = self.messageFrame.winfo_width()
            self.messageFrameHeight = self.messageFrame.winfo_height()

            self.messageTextFrame = Frame(self.messageFrame, height=math.ceil(self.messageFrameHeight * 0.9), width=math.ceil(self.messageFrameWidth * 0.9), bd=0, relief="groove")  
            self.messageTextFrame.configure(background='white')
            self.messageTextFrame.pack(fill=BOTH, padx=(20), pady=(20))
            self.messageTextFrame.pack_propagate(0)
            self.messageTextFrame.update_idletasks() # Calls all pending idle tasks to get frame sizes

            self.messageTextFrameWidth = self.messageTextFrame.winfo_width()
            self.messageTextFrameHeight = self.messageTextFrame.winfo_height()

            #Message
            self.text = Text(self.messageTextFrame)
            self.text.grid()
            self.text.place(height=math.ceil(self.messageTextFrameHeight), width=math.ceil(self.messageTextFrameWidth))

            def insert(text):
                self.text.insert(END, text + '\n')

            # replace below to report
            for child in backEnd.parent.children:
                insert("Name: " + child.name + "\n")
                stats = backEnd.reports.childInactivity(child.id)
                if stats != None:
                    _min, _max, _avg, _dts = stats
                    insert("The minimum time between mouse clicks for " + child.name + " is: " + str(_min) + backEnd.reports.formatEnd(_min))
                    insert("The maximum time between mouse clicks for " + child.name + " is: " + str(_max) + backEnd.reports.formatEnd(_max))
                    insert("The average time between mouse clicks for " + child.name + " is: " + str(round(_avg, 2)) + backEnd.reports.formatEnd(_avg) + "\n")
                else:
                    insert("No input data for " + child.name + "\n")
                stats = backEnd.reports.childNavigation(child.id)   
                if stats != None:
                    _total, _succesful, _percent = stats
                    insert("The percentage of successful navigation for " + child.name + " is: " + str(_percent) + "%.\n")
                else:
                    insert("No navigation data for " + child.name + "\n")

        displayAbout()
