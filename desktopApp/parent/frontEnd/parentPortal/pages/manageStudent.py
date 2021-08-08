import math
import datetime as dt
from tkinter import *
from tkinter import font as tkFont
from PIL import ImageTk,Image 

class ManageStudent:
    def __init__(self, mainClass, backEnd, onclickMenu):
        print("      Entering Parent - manage stduent screen - /parent/frontEnd/dashboard/pages/manageStudent.py")

        def newStudentClick():
            onclickMenu(10)

        def editStudentInfoClick(x):
            onclickMenu.childIndex = x
            onclickMenu(8)
            
        
        def editStudentScheduleClick(x):
            onclickMenu.childIndex = x
            onclickMenu(7)

        def manageMacrosClick(x):
            onclickMenu.childIndex = x
            onclickMenu(13)

        def addCalendarClick(x):
            onclickMenu.childIndex= x
            onclickMenu(11)

        def displayManageStudent():           
            self.fontSize = tkFont.Font(size=18)
            self.now = backEnd.localNow()
            today = self.now.strftime("%A %B %d, %Y")
            todayDateLabel = Label(mainClass.rightFrame, text=today, font=self.fontSize, background="white")
            todayDateLabel.pack(padx=(20,0), pady=(2,0), anchor=W)

            mainClass.rightFrame.update_idletasks() # Calls all pending idle tasks to get frame sizes
            
            # display students (left):  displayStudentLists() -> displayEachStudent()
            displayStudentLists()

            # account information (top right): displayAccountInformation()
            displayAccountInformation()

        def displayStudentLists():
            global newImg1, newImg2 
            self.rightFrameWidth = mainClass.rightFrame.winfo_width()
            self.rightFrameHeight = mainClass.rightFrame.winfo_height()

            # student list frame (left)
            studentListFrame = Frame(mainClass.rightFrame, width=self.rightFrameWidth*0.7, height=self.rightFrameHeight - 100, bd=1, relief="groove")  
            studentListFrame.configure(background='white')
            studentListFrame.pack(side=LEFT, fill=BOTH, padx=(20), pady=(5,30))
            studentListFrame.pack_propagate(0)

            studenListTileLabel = Label(studentListFrame, text="Student List", background="white", font="bold")
            studenListTileLabel.pack()

            imageIndex = 0
            onclickMenu.index = 0
            onclickMenu.childIndex = 0
            children = backEnd.parent.getChildren()
            for child in children:
                imageIndex += 1
                studentName = child.getName()
                # print(child.getID())

                ### student frame
                studentFrame = Frame(studentListFrame, width=self.rightFrameWidth*0.7, height=315, bd=2, relief="groove")  
                studentFrame.configure(background='white')
                studentFrame.pack(anchor=W, padx=(10), pady=(10))
                studentFrame.pack_propagate(0)

                #### avatar frame (left)
                avatarFrame = Frame(studentFrame, width=self.rightFrameWidth*0.7*0.2, height=300, bd=0, relief="groove")  
                avatarFrame.configure(background='white')
                avatarFrame.pack(side=LEFT, anchor=W, padx=(10), pady=(20))
                avatarFrame.pack_propagate(0)

                ##### avatar image
                img = Image.open(child.image)
                resizedImg = img.resize((105,125), Image.ANTIALIAS)

                if imageIndex == 1:
                    newImg1 = ImageTk.PhotoImage(resizedImg)
                    logo = Label(avatarFrame, image=newImg1, width=105, height=125, bd=0) 
                    logo.pack(anchor=W, padx=(10), pady=(5))
                elif imageIndex == 2:
                    newImg2 = ImageTk.PhotoImage(resizedImg)
                    logo = Label(avatarFrame, image=newImg2, width=105, height=125, bd=0) 
                    logo.pack(anchor=W, padx=(10), pady=(5))
                

                editStudentInfoButton = Button(avatarFrame, text="Edit Info", background="white",command = lambda child=child: editStudentInfoClick(child.getID()))
                editStudentInfoButton.pack(padx=(3,0), pady=(0,2), anchor=W)

                editStudentScheduleButton = Button(avatarFrame, text="Edit Schedule", background="white",command = lambda child=child: editStudentScheduleClick(child.getID()))
                editStudentScheduleButton.pack(padx=(3,0), pady=(0,2), anchor=W)

                manageMacrosButton = Button(avatarFrame, text="Manage Macros", background="white",command = lambda child=child: manageMacrosClick(child.getID()))
                manageMacrosButton.pack(padx=(3,0), pady=(0,2), anchor=W)

                #addCalendarButton=Button(avatarFrame, text="Manage Classes", background="white",command = lambda child=child: addCalendarClick(child.getID()))
                #addCalendarButton.pack(padx=(3,0), pady=(0,2), anchor=W)


                #### student info frame (right)
                studentInfoFrame = Frame(studentFrame, width=self.rightFrameWidth*0.7*0.8, height=250, bd=0, relief="groove")  
                studentInfoFrame.configure(background='white')
                studentInfoFrame.pack(side=RIGHT, anchor=W, pady=(10))
                studentInfoFrame.pack_propagate(0)

                ##### student info labels
                studentLabel = Label(studentInfoFrame, text="Name: " + studentName, background="white")
                studentLabel.pack(padx=(3,0), pady=(10, 3), anchor=W)

                displayEachStudent(child, studentInfoFrame)
                onclickMenu.index = onclickMenu.index + 1

        def displayEachStudent(child, studentInfoFrame):
            # acivities frame
            activitiesFrame = Frame(studentInfoFrame, width=self.rightFrameWidth*0.7*0.8, bd=0, relief="groove")  
            activitiesFrame.configure(background='white')
            activitiesFrame.pack(anchor=W)

            # classes
            studentClasses = child.getClasses()
            if studentClasses != []:                
                for studentClass in studentClasses:
                    className = studentClass.getName()
                    # classTeacher = studentClass.getTeacherName()

                    # activities
                    classActivities = studentClass.getActivities()
                    for classActivity in classActivities:
                        activityName = classActivity.getName()
                        # schedules
                        scheduleItems = classActivity.getScheduleItems()                
                        for scheduleItem in scheduleItems:
                            schedulDateTime = scheduleItem.getDateTime() # schedule date time
                            schedulDateTime = backEnd.convertToLocal(backEnd.formatAsDatetime(schedulDateTime)) # convert string to datetime

                            scheduleStartTime = backEnd.formatTime(schedulDateTime) # start time
                            
                            nowDate = backEnd.formatDate(self.now) # now date
                            scheduleEndDate = backEnd.formatDate(schedulDateTime) # end date

                            if nowDate == scheduleEndDate:
                                studentLabel = Label(activitiesFrame, text=" - [" + className + "]: " + activityName + " starts at " + str(scheduleStartTime) , background="white")
                                studentLabel.pack(padx=(3,0), pady=(7, 3), anchor=W)
                        # end for loop ( for classActivity in classActivities: )
                    # end for loop ( for classActivity in classActivities: )
                # end for loop (for studentClass in studentClasses:)
            # end of if (if studentClasses != []:)
            else: # no class enrolled
                studentLabel = Label(studentInfoFrame, text="   - No class enrolled", background="white")
                studentLabel.pack(padx=(3,0), pady=(10, 3), anchor=W)

        def displayAccountInformation():
            self.rightFrameHeight = mainClass.rightFrame.winfo_height()

           

            accountInformationFrame = Frame(mainClass.rightFrame, width=self.rightFrameWidth*0.3, height=250, bd=1, relief="groove")
            accountInformationFrame.configure(background='white')
            accountInformationFrame.pack(side=TOP, fill=X, expand=1, anchor=NE, padx=(10), pady=(5))
            accountInformationFrame.pack_propagate(0)


            newStudentButton = Button(accountInformationFrame, text="Add New Student", background="white",command = lambda: newStudentClick())
            newStudentButton.pack(padx=(3,0), pady=(0,3), anchor=W)
        
        displayManageStudent()
