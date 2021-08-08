import math
import webbrowser
from tkinter import *
from tkinter import font as tkFont
from tkinter import messagebox
from PIL import ImageTk,Image 
from functools import partial
import os,sys

from parent.frontEnd.parentPortal.pages.dashboard import Dashboard
from parent.frontEnd.parentPortal.pages.manageStudent import ManageStudent
from parent.frontEnd.parentPortal.pages.manageAccount import ManageAccount
from parent.frontEnd.parentPortal.pages.parentsBoard import ParentsBoard
from parent.frontEnd.parentPortal.pages.contactUs import ContactUs
from parent.frontEnd.parentPortal.pages.eventLog import EventLog
from parent.frontEnd.parentPortal.pages.manageStudentSchedule import ManageStudentSchedule
from parent.frontEnd.parentPortal.pages.manageStudentInfo import ManageStudentInfo
from parent.frontEnd.parentPortal.pages.manageStudentClass import ManageStudentClass
from parent.frontEnd.parentPortal.pages.addStudentClass import AddStudentClass
from parent.frontEnd.parentPortal.pages.addStudent import AddStudent
from parent.frontEnd.parentPortal.pages.importCalendar import ImportCalendar
from parent.frontEnd.parentPortal.pages.report import Report
from parent.frontEnd.parentPortal.pages.ManageMacros import *
from parent.frontEnd.parentPortal.pages import *

from parent.frontEnd.parentPortal.pages import *

class PreviousButton: 
    def __init__(self, previousButton = None): 
         self._previousButton = previousButton 
      
    # getter method 
    def getPreviousButton(self): 
        return self._previousButton 
      
    # setter method 
    def setPreviousButton(self, selectedButton): 
        self._previousButton = selectedButton 
        

class ParentPortalMain:
    def __init__(self, root, backEnd):
        self.root = root
        root.title("littleLEARNERS - Parent Portal")
        print("    Entering Parent Portal Main screen - /parent/frontEnd/dashboard/parentPortalMain.py")
        root.geometry("1400x800")
        def setup_icon():          
            p1 = PhotoImage(file = 'student/frontEnd/images/icon.png')
            root.iconphoto(False, p1)       

        def checkDatabase():
            # print("Checking database")
            backEnd.update('parent') # Update local data structure with data from DB  

            for childID, name, msg in backEnd.checkRaisedHand():
                messagebox.showinfo(name +" needs help", name + " says:\n\n" + msg)
                # backEnd.addHelpResponse("Default response", childID)

            for name in backEnd.checkNavFailed():
                messagebox.showinfo(name +" needs help", "Navigation failed")

            self._job = root.after(2000, checkDatabase)
        
        def displayRightFrame(menuId):
            #if menuId != 4:
            for widget in self.rightFrame.winfo_children():
                widget.destroy()

            if menuId == 1:
                root.title("littleLEARNERS - Parent Portal - Dashboard")
                Dashboard(self, backEnd, onclickMenu)
            elif menuId == 2:
                root.title("littleLEARNERS - Parent Portal - Manage Student")
                ManageStudent(self, backEnd, onclickMenu)
            elif menuId == 3:
                root.title("littleLEARNERS - Parent Portal - Manage Account")
                ManageAccount(self, backEnd)
            elif menuId == 4:
                root.title("littleLEARNERS - Parent Portal - Parents Board")
                ParentsBoard(self, backEnd,onclickMenu)
                #webbrowser.open('http://411orang.cpi.cs.odu.edu/', new=2)
            elif menuId == 5:
                root.title("littleLEARNERS - Parent Portal - Contact Us")
                ContactUs(self, backEnd)
            elif menuId == 6:
                root.title("littleLEARNERS - Parent Portal - Event Log")
                EventLog(self, backEnd)
            elif menuId == 7:
                root.title("littleLEARNERS - Parent Portal - Manage Student Schedule")
                ManageStudentSchedule(self, backEnd, onclickMenu)
            elif menuId == 8:
                root.title("littleLEARNERS - Parent Portal - Manage Student Info")
                ManageStudentInfo(self, backEnd, onclickMenu)
            elif menuId == 9:
                root.title("littleLEARNERS - Parent Portal - Manage Student Class")
                ManageStudentClass(self, backEnd, onclickMenu)
            elif menuId == 10:
                root.title("littleLEARNERS - Parent Portal - Add New Student")
                AddStudent(self, backEnd, onclickMenu)
            elif menuId == 11:
                root.title("littleLEARNERS - Parent Portal - Add New Calendar")
                ImportCalendar(self, backEnd, onclickMenu)
            elif menuId == 12:
                root.title("littleLEARNERS - Parent Portal - Add New Class")
                AddStudentClass(self, backEnd, onclickMenu)
            elif menuId == 13:
                root.title("littleLEARNERS - Parent Portal - Manage Student Macros")
                ManageMacros.ManageMacros(self, self.root, backEnd, onclickMenu)
            elif menuId == 14:
                root.title("littleLEARNERS - Parent Portal - Report")
                Report(self, backEnd)

        def onclickMenu(menuId):
            if menuId == 1:
                selectedButton = self.dashBoardButton
            elif menuId == 2:
                selectedButton = self.manageStudentButton
            elif menuId == 3:
                selectedButton = self.manageAccountButton
            elif menuId == 4:
                selectedButton = self.parentsBoardButton
            elif menuId == 5:
                selectedButton = self.contactUsButton
            elif menuId == 6:
                selectedButton = self.eventLogButton
            elif menuId == 7:
                selectedButton = self.studentScheduleButton
            elif menuId == 8:
                selectedButton = self.studentInfoButton
            elif menuId == 9:
                selectedButton = self.studentClassButton
            elif menuId == 10:
                selectedButton = self.addStudentButton
            elif menuId == 11:
                selectedButton = self.calendarButton
            elif menuId == 12:
                selectedButton = self.addStudentClassButton
            elif menuId == 13:####################################################################
                selectedButton = self.manageMacrosButton
            elif menuId == 14:####################################################################
                selectedButton = self.reportButton

            previousButton = self.previousButtonClass.getPreviousButton()
            previousButton["background"] = "white"
            self.previousButtonClass.setPreviousButton(selectedButton)
            selectedButton["background"] = "orange"
            global index
            global childIndex
            global classIndex
            global scheduleItemIndex
            displayRightFrame(menuId)

        def chatGetNewMessage(list1, list2):
            return list(set(list1).symmetric_difference(set(list2)))  

        def chatStartCheckingDatabase(studentName, childIndex):
            self.newMessages = chatGetNewMessage(backEnd.getMessages(backEnd.parent.firstName, studentName, childIndex), self._messages)
     
            if self.newMessages:
                print("New message: " + str(self.newMessages))
                for message in self.newMessages:
                    messageName = message[0]
                    messageString = message[1]
                    messageDate = message[2]
                    self.messagesText.insert(END, messageName + ": " + messageString + "\n")
                    self.messagesText.insert(END, "      " + messageDate + "\n\n")
                    self._messages.append(message)

                self.messagesText.yview(END)
                backEnd.pushUpdates()

            self._job2 = root.after(100, chatStartCheckingDatabase, studentName, childIndex)

        def chatStopCheckingDatabase():
            if self._job2 is not None:
                root.after_cancel(self._job2)
                self._job2 = None
                print("chatStopCheckingDatabase")

        def chatSendClick(msg, childID):
            backEnd.addHelpResponse(msg, childID)

        def chatBackButtonClick():
            self.chatMessageFrame.destroy()
            chatDisplayStudentSelection()
            chatStopCheckingDatabase()

        def chatSelectStudent(childIndex, studentName, childID):
            self.chatMessageFrame.destroy()
            chatDisplayMessage(childIndex, studentName, childID)

        def chatDisplayStudentSelection():
            self.chatMessageFrame = Frame(self.chatFrame, height=350, bd=1, relief="groove")
            self.chatMessageFrame.pack()

            self.chatStudentSelectFrame = Frame(self.chatMessageFrame)
            self.chatStudentSelectFrame.pack()
 
            self.children = backEnd.parent.getChildren()
            self.childIndex = 0
            for child in self.children:
                self.studentName = child.getName()
                self.studentNameLabel = Button(
                    self.chatStudentSelectFrame, 
                    text=self.studentName, 
                    width=math.ceil(self.currentAppWith*0.17 - 30), 
                    height=3, 
                    bd=1, 
                    relief="groove", 
                    background="white", 
                    font="bold", 
                    command=partial(chatSelectStudent, self.childIndex, self.studentName, child.getID()))
                self.studentNameLabel.pack(padx=(5), pady=(5))
                self.childIndex += 1

        def chatDisplayMessage(childIndex, studentName, childID):
            self.chatMessageFrame = Frame(self.chatFrame, height=350, bd=1, relief="groove")
            self.chatMessageFrame.pack()

            self.chatBackButton = Button(self.chatMessageFrame, text="BACK", background="white", command = lambda: chatBackButtonClick())
            self.chatBackButton.pack(anchor=W)

            self.messageFrame = Frame(self.chatMessageFrame, height=270, bd=1, relief="groove")
            self.messageFrame.configure(background='white')
            self.messageFrame.pack(fill=BOTH, expand=1, padx=(2), pady=(0,5))
            self.messageFrame.pack_propagate(0)

            verticalScrollBar = Scrollbar(self.messageFrame)
            verticalScrollBar.pack(side = RIGHT, fill = Y)

            self.messagesText = Text(self.messageFrame, yscrollcommand = verticalScrollBar.set)
            self.messagesText.pack()
            print("chatDisplayMessage student name: " + studentName)
            self._messages = backEnd.getMessages("John", studentName, childIndex)
            for message in self._messages:
                messageName = message[0]
                messageString = message[1]
                messageDate = message[2]
                self.messagesText.insert(END, messageName + ": " + messageString + "\n")
                self.messagesText.insert(END, "      " + messageDate + "\n\n")

            chatStartCheckingDatabase(studentName, childIndex)

            verticalScrollBar.config(command = self.messagesText.yview)
            self.messagesText.yview(END)

            self.chatInputFrame = Frame(self.chatMessageFrame, width=math.ceil(self.currentAppWith*0.17 - 30), height=30, relief="groove")
            self.chatInputFrame.configure(background='white')
            self.chatInputFrame.pack(side=LEFT, anchor=S, padx=(2), pady=(0,2))
            self.chatInputFrame.pack_propagate(0)

            self.inputEntry = Entry(self.chatInputFrame)
            self.inputEntry.pack()

            self.chatSendButtonFrame = Frame(self.chatMessageFrame)
            self.chatSendButtonFrame.configure(background='white')
            self.chatSendButtonFrame.pack(side=RIGHT, anchor=S, pady=(0,6))
            
            self.sendButton = Button(self.chatSendButtonFrame, text="SEND", background="white", command=lambda:[chatSendClick(self.inputEntry.get(), childID), self.inputEntry.delete(0, "end")])
            self.sendButton.pack()

        def dispChat():
            self.chatFrame = Frame(self.leftFrame, height=350, bd=1, relief="groove")
            self.chatFrame.configure(background='white')
            self.chatFrame.pack(side=BOTTOM, fill=X, expand=1, anchor=S, padx=(5), pady=(5))
            self.chatFrame.pack_propagate(0)

            self.title = Label(self.chatFrame, text="CHAT", background="white", font="bold")
            self.title.pack()

            chatDisplayStudentSelection()

        def displayDashBoardMain():   
            # start checking database for raise hand
            checkDatabase()  
            # pushUpdates()
            
            root.update_idletasks() # Calls all pending idle tasks to get frame sizes
            # global newImg
            self.currentAppWith = root.winfo_width()
            self.currentAppHeight = root.winfo_height()

            # left frame (logo + menu)
            self.leftFrame = Frame(root, width=self.currentAppWith*0.2, height=self.currentAppHeight, bd=4, relief="ridge")  
            self.leftFrame.configure(background='white')
            self.leftFrame.pack(side=LEFT, fill=BOTH)
            self.leftFrame.pack_propagate(0)
            
            ## display logo
            self.img = Image.open("student/frontEnd/images/orangePic3.png")
            self.resizedImg = self.img.resize((math.ceil(self.currentAppWith*0.17),100), Image.ANTIALIAS)
            self.newImg = ImageTk.PhotoImage(self.resizedImg)
            self.logo = Label(self.leftFrame, image=self.newImg, width=math.ceil(self.currentAppWith*0.17), height=100, bd=0, background='#ffffff') 
            self.logo.pack(pady=25)

            ## menu frame
            self.menuFrame = Frame(self.leftFrame, width=self.currentAppWith*0.2, height=self.currentAppHeight-100, bd=0, relief="ridge")
            self.menuFrame.configure(background='white')
            self.menuFrame.pack(pady=(0, 0))

            ### menu list
            self.previousButtonClass = PreviousButton()
            self.dashBoardButton = Button(self.menuFrame, text="Dashboard", width=math.ceil(self.currentAppWith*0.17), highlightthickness = 0, background="orange", bd=0, activebackground='orange', command=lambda:onclickMenu(1))
            self.dashBoardButton.pack()
            self.previousButtonClass.setPreviousButton(self.dashBoardButton) #dashboard will be disaplayed initially

            self.manageStudentButton = Button(self.menuFrame, text="Manage Students", width=math.ceil(self.currentAppWith*0.17), highlightthickness = 0, background="white", bd=0, activebackground='orange', command=lambda:onclickMenu(2))
            self.manageStudentButton.pack(pady=3)

            self.manageAccountButton = Button(self.menuFrame, text="Manage Account", width=math.ceil(self.currentAppWith*0.27), highlightthickness = 0, background="white", bd=0, activebackground='orange', command=lambda:onclickMenu(3))
            self.manageAccountButton.pack(pady=3)

            self.contactUsButton = Button(self.menuFrame, text="Contact Us", width=math.ceil(self.currentAppWith*0.17), highlightthickness = 0, background="white", bd=0, activebackground='orange', command=lambda:onclickMenu(5))
            self.contactUsButton.pack(pady=3)

            self.eventLogButton = Button(self.menuFrame, text="Event Log", width=math.ceil(self.currentAppWith*0.17), highlightthickness = 0, background="white", bd=0, activebackground='orange', command=lambda:onclickMenu(6))
            self.eventLogButton.pack(pady=3)

            self.studentScheduleButton = Button(self.menuFrame, text=" Manage Student Schedule", width=math.ceil(self.currentAppWith*0.17), highlightthickness = 0, background="white", bd=0, activebackground='orange', command=lambda:onclickMenu(7))

            self.studentInfoButton = Button(self.menuFrame, text=" Manage Student Info", width=math.ceil(self.currentAppWith*0.17), highlightthickness = 0, background="white", bd=0, activebackground='orange', command=lambda:onclickMenu(8))

            self.studentClassButton = Button(self.menuFrame, text="Manage Student Class", width=math.ceil(self.currentAppWith*0.17), highlightthickness = 0, background="white", bd=0, activebackground='orange', command=lambda:onclickMenu(9))

            self.addStudentButton = Button(self.menuFrame, text="Add New Student", width=math.ceil(self.currentAppWith*0.17), highlightthickness = 0, background="white", bd=0, activebackground='orange', command=lambda:onclickMenu(10))

            self.calendarButton = Button(self.menuFrame, text="Calendar", width=math.ceil(self.currentAppWith*0.17), highlightthickness = 0, background="white", bd=0, activebackground='orange', command=lambda:onclickMenu(11))

            self.addStudentClassButton = Button(self.menuFrame, text="Add Class", width=math.ceil(self.currentAppWith*0.17), highlightthickness = 0, background="white", bd=0, activebackground='orange', command=lambda:onclickMenu(12))

            self.parentsBoardButton = Button(self.menuFrame, text="Parents Board", width=math.ceil(self.currentAppWith*0.17), highlightthickness = 0, background="white", bd=0, activebackground='orange', command=lambda:onclickMenu(4))
            self.parentsBoardButton.pack(pady=(10,0))

            self.reportButton = Button(self.menuFrame, text="Report", width=math.ceil(self.currentAppWith*0.17), highlightthickness = 0, background="white", bd=0, activebackground='orange', command=lambda:onclickMenu(14))
            self.reportButton.pack(pady=(10,0))

            self.manageMacrosButton = Button(self.menuFrame, text="Manage Student Macros", width=math.ceil(self.currentAppWith*0.17), highlightthickness = 0, background="white", bd=0, activebackground='orange', command=lambda:onclickMenu(13))

            # text chat
            dispChat()

            # right frame
            self.rightFrame = Frame(root, width=self.currentAppWith*0.8, height=self.currentAppHeight, bd=4, relief="ridge")
            self.rightFrame.configure(background='white')
            self.rightFrame.pack(side=RIGHT, fill=BOTH, expand=1, anchor=E)
            self.rightFrame.pack_propagate(0)

            setup_icon()

            displayRightFrame(1)

     

        displayDashBoardMain()

   