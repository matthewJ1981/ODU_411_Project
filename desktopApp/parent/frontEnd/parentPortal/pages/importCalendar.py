import math
from tkinter import *
from tkinter import font as tkFont
from tkinter import messagebox


class ImportCalendar:
    def __init__(self, mainClass, backEnd, onclickMenu):
        print("      Entering Parent - Add new student screen - /parent/frontEnd/dashboard/pages/importCalendar.py")

        def addButtonClick(className,teacherName,calendarID):
            children = backEnd.parent.getChildren()
            for child in children:
                if child.getID() == onclickMenu.childIndex:
                    self.studnet=child.getID()
                    
            backEnd.newClass(className,teacherName,calendarID,self.studnet)
            messagebox.showinfo(None, "Class information saved successfully")

        def cancelButtonClick():
            onclickMenu(2)

        def displayStuff():
            mainClass.rightFrame.update_idletasks() # Calls all pending idle tasks to get frame sizes
            self.rightFrameWidth = mainClass.rightFrame.winfo_width()
            self.rightFrameHeight = mainClass.rightFrame.winfo_height()

            # account information frame (left)
            self.accountInformationFrame = Frame(mainClass.rightFrame, width=self.rightFrameWidth*0.7, height=self.rightFrameHeight - 100, bd=1, relief="groove")  
            self.accountInformationFrame.configure(background='white')
            self.accountInformationFrame.pack(side=LEFT, fill=BOTH, padx=(20), pady=(30))
            self.accountInformationFrame.pack_propagate(0)
            self.cancelButton= Button(self.accountInformationFrame, width=20, text = "CANCEL", background="white", font="bold" ,command = lambda: cancelButtonClick())
            self.cancelButton.pack(side=BOTTOM, padx=(20), pady=(30))

            
            self.calendarInformationEntriesFrame = Frame(self.accountInformationFrame, height=self.rightFrameHeight - 100, bd=0, relief="groove")  
            self.calendarInformationEntriesFrame.configure(background='white')
            self.calendarInformationEntriesFrame.pack(side=LEFT, fill=BOTH, padx=(20), pady=(30))
            self.calendarInformationEntriesFrame.pack_propagate(0)


            self.classNameLabel = Label(self.calendarInformationEntriesFrame, text="Class Name: ", background="white", font="bold")
            self.classNameLabel.grid(row=0,column=0, sticky=W)
            self.classNameEntry = Entry(self.calendarInformationEntriesFrame, width=30)
            self.classNameEntry.grid(row=0,column=1, padx=(20, 0), pady=10)

            self.teacherNameLabel = Label(self.calendarInformationEntriesFrame, text="Teacher Name: ", background="white", font="bold")
            self.teacherNameLabel.grid(row=2,column=0, sticky=W)
            self.teacherNameEntry = Entry(self.calendarInformationEntriesFrame, width=30)
            self.teacherNameEntry.grid(row=2,column=1, padx=(20, 0), pady=10)

            self.calendarIDLabel = Label(self.calendarInformationEntriesFrame, text="Calendar ID: ", background="white", font="bold")
            self.calendarIDLabel.grid(row=3,column=0, sticky=W)
            self.calendarIDEntry = Entry(self.calendarInformationEntriesFrame, width=30)
            self.calendarIDEntry.grid(row=3,column=1, padx=(20, 0), pady=10)


            self.addButton= Button(self.calendarInformationEntriesFrame, width=10, text = "Add", background="white", font="bold" ,command = lambda: addButtonClick(self.classNameEntry.get(),self.teacherNameEntry.get(),self.calendarIDEntry.get()))
            self.addButton.grid(row=4,column=0, padx=(10, 0), pady=10)
    
        displayStuff()