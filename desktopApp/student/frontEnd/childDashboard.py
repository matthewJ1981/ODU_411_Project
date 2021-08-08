from cefpython3 import cefpython as cef
import ctypes
from tkinter import *
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
import sys
import os
import platform
import logging as _logging
from PIL import ImageTk,Image
from time import strftime
from itertools import cycle
from datetime import datetime,timedelta
import pytz

sys.path.insert(0, os.path.abspath("/student/frontEnd/"))

#Needed for "from frontEnd.parentPortal.parentPortalMain import ParentPortalMain"
sys.path.insert(0, os.path.abspath("./parent"))

from student.frontEnd.studentClass import Student
from student.frontEnd.hallway import Hallway
from student.frontEnd.schedule import Schedule
from student.frontEnd.ChildEmbeddedBrowser import MainFrame

#This doesn't actually work without "sys.path.insert(0, os.path.abspath("./parent"))"
from frontEnd.parentPortal.parentPortalMain import ParentPortalMain

from student.frontEnd.changeTimeClass import ChangeTime
from student.frontEnd.parent_access import ParentAccess
from student.frontEnd.GotoClass import *




class ChildDashboard(tk.Frame):

   #def __init__(self, *args, **kwargs): 

   
   def __init__(self, root, backend):     
        #tk.Frame.__init__(self, *args, **kwargs)
        self.root = root
        self.backend = backend
        root.geometry("1400x800")
        root.configure(bg="white")        
        self.setup_icon()

        self.wHeight = self.root.winfo_height()
        self.wWidth = self.root.winfo_width()

        tk.Frame.__init__(self, root)       
        self.master.title("littleLEARNERS")

        self.topFrame = Frame(self, bg='white', height=50, pady=25, padx=40)
        self.topFrame.pack(side=TOP, fill=X)
        self.topFrame.columnconfigure((0, 1, 2, 3), weight=1)

        self.rightFrame = Frame(self, bg="white", padx=25)
        self.rightFrame.pack(side=RIGHT, fill=Y)
        self.rightFrame.rowconfigure((0, 1, 2, 3, 4), weight=1) 
        
        self.leftFrame = Frame(self, bg="white")
        self.leftFrame.pack(side=LEFT, fill=Y)
        self.leftFrame.rowconfigure((0, 1, 2, 3, 4), weight=1) 

        self.leftAvatarFrmae = Frame(self.leftFrame, bg="white", width=250, height=250)
        self.leftAvatarFrmae.pack(side=BOTTOM, fill=X, expand=1, anchor=S)
        self.leftAvatarFrmae.pack_propagate(0)

        self.leftChatFrmae = Frame(self.leftFrame,  width=250, height=350, bg="white", bd=1, relief="groove")
        self.leftChatFrmae.pack(side=TOP, fill=Y, expand=1, anchor=N)
        self.leftChatFrmae.pack_propagate(0)
               

        self.centerFrame = Frame(self, bg="white", padx=25,height=(self.wHeight*.75),width=(self.wWidth*.7))
        #self.centerFrame.pack(fill=BOTH, expand=True)
        self.centerFrame.pack(fill=BOTH, expand=False)
        self.centerFrame.pack_propagate(0)
        self.centerFrame.columnconfigure((0, 3), weight=1)
        self.centerFrame.columnconfigure((1, 2), weight=1)
        self.centerFrame.rowconfigure((0, 1), weight=1)
        
        self.show_browser(MainFrame)
           
        #buttons
        #self.button_setup(self.rightFrame, self.topFrame)
        
        #class picture
        self.classPic(self.topFrame)

        #banner photo
        self.bannerPhoto(self.topFrame)
        
        #clock
        self.displayTime(self.topFrame) 

        #litleAssistant prompts
        #self.prompt()

        #debug output
        print("Name of current child is: " + self.backend.parent.children[self.backend.currChild].getName())
        # self.updates() sangwoo 04.13.2021 - don't need this. replaced this with chat feature
        
        photo = Image.open('student/frontEnd/images/raiseHand.png') #open image
        resized = photo.resize((80, 100), Image.ANTIALIAS) #resize
        correctedImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage
        self.raiseHand=Button(self.rightFrame, image=correctedImage, borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff', command=self.onClickRaisedHand)
        self.raiseHand.image = correctedImage
        self.raiseHand.grid(row=0, column=0)

        photo = Image.open('student/frontEnd/images/goToClass.png')  # open image
        resized = photo.resize((80, 100), Image.ANTIALIAS) #resize
        correctedImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage
        self.goToClass=Button(self.rightFrame, image=correctedImage, borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff', command=self.onClickGoToClass)
        self.goToClass.image = correctedImage   
        self.goToClass.grid(row=1, column=0)

        photo = Image.open('student/frontEnd/images/parentAccess.png') #open image
        resized = photo.resize((120, 70), Image.ANTIALIAS) #resize
        correctedImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage
        self.parentBtn=Button(self.rightFrame, image=correctedImage, borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff', command=self.parentView)
        self.parentBtn.image = correctedImage
        self.parentBtn.grid(row=4, column = 0)
     #self.raiseHand.grid(row=0, rowspan=2, column=2)

        photo = Image.open('student/frontEnd/images/time_change.png') #open image
        resized = photo.resize((120, 70), Image.ANTIALIAS) #resize
        correctedImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage
        self.timeBtn=Button(self.rightFrame, image=correctedImage, borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff', command=self.changeTime)
        self.timeBtn.image = correctedImage
        self.timeBtn.grid(row=3, column = 0, sticky="S")

        photo = Image.open('student/frontEnd/images/schedule_gray.png') #open image
        resized = photo.resize((125, 55), Image.ANTIALIAS) #resize
        correctedImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage
        self.goToSchedule=Button(self.topFrame, image=correctedImage, borderwidth = 0, bg='#ffffff', padx=10, pady=15, highlightthickness=0, activebackground='#ffffff', command=lambda: self.show_schedule(Schedule))
        self.goToSchedule.image = correctedImage
        self.goToSchedule.grid(row=1, column=2, sticky="W")

        photo = Image.open('student/frontEnd/images/hallway_gray.png') #open image
        resized = photo.resize((125, 55), Image.ANTIALIAS) #resize
        correctedImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage
        self.goToHallway=Button(self.topFrame, image=correctedImage, borderwidth = 0, bg='#ffffff', padx=10, pady=15, highlightthickness=0, activebackground='#ffffff', command=lambda: self.show_hallway(Hallway))
        self.goToHallway.image = correctedImage
        self.goToHallway.grid(row=1, column=1, sticky="E")

        # chat start
        self.chatDisplay()

        mylist = os.listdir('student/frontEnd/images/wave')
        global count
        count = 0

        self.mylist2 = []
        for x in mylist:
            self.mylist2.append("student/frontEnd/images/wave/" + x)
        self.mylist2.sort()

        wave = []
        for x in self.mylist2:
            photo = Image.open(x)
            resized = photo.resize((250, 250), Image.ANTIALIAS) #resize
            wave.append(ImageTk.PhotoImage(resized))

        self.images = cycle(wave)
        self.wave=Button(self.leftAvatarFrmae, image=wave[0], borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff', command=self.onClickLittleAssistant)
        self.wave.grid(row=4, column=0)
        self.onClickLittleAssistant()

   def chatDisplay(self):
        #text chat
        self.chatMessageFrame = Frame(self.leftChatFrmae,  bd=1, relief="groove")
        self.chatMessageFrame.pack(fill=Y, expand=TRUE)

        self.messageFrame = Frame(self.chatMessageFrame, bd=1, relief="groove")
        self.messageFrame.configure(background='white')
        self.messageFrame.pack(fill=BOTH, expand=1, padx=(2), pady=(0,5))
        self.messageFrame.pack_propagate(0)

        verticalScrollBar = Scrollbar(self.messageFrame)
        verticalScrollBar.pack(side = RIGHT, fill = Y)

        self.messagesText = Text(self.messageFrame, yscrollcommand = verticalScrollBar.set)
        self.messagesText.pack()
        self.parentName = self.backend.parent.getFirstName()
        print("chatDisplayMessage on child side")
        self._messages = self.backend.getMessages(self.parentName, "Me", self.backend.currChild)
        for message in self._messages:
            messageName = message[0]
            messageString = message[1]
            messageDate = message[2]
            self.messagesText.insert(END, messageName + ": " + messageString + "\n")
            self.messagesText.insert(END, "      " + messageDate + "\n\n")
   
        self.chatStartCheckingDatabase(self.parentName, self.backend.currChild)

        verticalScrollBar.config(command = self.messagesText.yview)
        self.messagesText.yview(END)

        self.chatInputFrame = Frame(self.chatMessageFrame, width=210, height=30, relief="groove")
        self.chatInputFrame.configure(background='white')
        self.chatInputFrame.pack(side=LEFT, anchor=S)
        self.chatInputFrame.pack_propagate(0)

        self.inputEntry = Entry(self.chatInputFrame, width=210)
        self.inputEntry.pack()

        self.chatSendButtonFrame = Frame(self.chatMessageFrame)
        self.chatSendButtonFrame.configure(background='white')
        self.chatSendButtonFrame.pack(side=RIGHT, anchor=S, pady=(0,6))
        
        self.sendButton = Button(self.chatSendButtonFrame, text="SEND", background="white", command=lambda:[self.chatSendClick(self.inputEntry.get()), self.inputEntry.delete(0, "end")])
        self.sendButton.pack()
 
   def chatSendClick(self, msg):
       self.backend.addHelpRequest(msg)

   def chatGetNewMessage(self, list1, list2):
       return list(set(list1).symmetric_difference(set(list2)))  

   def chatStartCheckingDatabase(self, parentName, childIndex):     
       self.backend.update('child')
       self.backend.getMessagesAsChild()
       self.newMessages = self.chatGetNewMessage(self.backend.getMessages(parentName, "Me", childIndex), self._messages)

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
           self.backend.pushUpdates()

       self._job2 = self.root.after(2000, self.chatStartCheckingDatabase, parentName, childIndex)

   def setup_icon(self):          
        p1 = PhotoImage(file = 'student/frontEnd/images/icon.png')
        self.root.iconphoto(False, p1)        
         
   

  
   def displayTime(self, topFrame):        
        global bg2, bg, timeLeft

        def time(): 
            currentTime = strftime('%I:%M:%S %p') 
            self.clockTime.config(text=(self.getScheduledClass() + "     " + currentTime), image=bg, compound='center')
            #self.clockTime.config(text=currentTime, image=bg, compound='center')             
            self.clockTime.after(1000, time) 
                          

        #clock bar image
        photo = Image.open('student/frontEnd/images/timeBar.png') #open image
        resized = photo.resize((650, 65), Image.ANTIALIAS) #resize
        bg = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage
  
        
        self.clockTime = Label(topFrame, font = ('calibri', 30, 'bold'), padx=25, foreground="#ffffff", background="#ffffff", pady=10)
        self.clockTime.image=bg        
        self.clockTime.grid(column=1, row=0, columnspan=2)               
        time()

  #  sangwoo 04.13.2021 - don't need this. replaced this with chat feature
  #  def updates(self):
  #       self.backend.update('child')
  #       self.backend.getMessagesAsChild()

  #       response = self.backend.checkHelpResponses()
  #       if response != None:
  #            messagebox.showinfo("Help response", response)
             
  #       self.root.after(5000, self.updates)

   def getScheduledClass(self):
        now = datetime.now()
        td = datetime.today()
        today = td.strftime("%m/%d/%y")
        child = self.backend.parent.children[self.backend.currChild]
        studentClasses = self.backend.parent.children[self.backend.currChild].getClasses()
        if studentClasses != []:
            for studentClass in studentClasses:
                classActivities = studentClass.getActivities()
                for classActivity in classActivities:
                    activityName = classActivity.getName()
                    scheduleItems = classActivity.getScheduleItems()                
                    for scheduleItem in scheduleItems:
                        schedulDateTime = scheduleItem.getDateTime() # schedule date time
                        schedulDateTime = self.backend.convertToLocal(self.backend.formatAsDatetime(schedulDateTime)) # convert string to datetime
                        scheduleStartTime = self.backend.formatTime(schedulDateTime) # start time
                        scheduleDate = self.backend.formatDate(schedulDateTime)
                        if today == scheduleDate:
                            utc=pytz.UTC
                            scheduleEndTime = schedulDateTime + timedelta(minutes=int(scheduleItem.getDuration()))
                            flag=0
                            if self.backend.formatTime(schedulDateTime) <= self.backend.formatTime(scheduleEndTime):
                                flag = self.backend.formatTime(schedulDateTime) <= self.backend.formatTime(utc.localize(now)) <= self.backend.formatTime(scheduleEndTime)
                            else:
                                flag = self.backend.formatTime(schedulDateTime) <= self.backend.formatTime(utc.localize(now)) or self.backend.formatTime(utc.localize(now)) <= self.backend.formatTime(scheduleEndTime)
                            
                            if(flag):
                                return activityName






        return "Free Time"
    
   def onClickRaisedHand(self):
        #Open text box for help request
        #Get text from text box
        #Save helprequest in the database
        self.backend.addHelpRequest('I need help!')
        #Set raised hand flag
        self.backend.raiseHand()
        #self.backend.parent.children[self.backend.currChild].setRaisedHand(1)
        print('Raise Hand button clicked')
        self.onClickLittleAssistant()

   def prompt(self):
        now = datetime.now()
        td = datetime.today()
        today = td.strftime("%m/%d/%y")
        child = self.backend.parent.children[self.backend.currChild]
        studentClasses = self.backend.parent.children[self.backend.currChild].getClasses()
        if studentClasses != []:
            for studentClass in studentClasses:
                classActivities = studentClass.getActivities()
                for classActivity in classActivities:
                    activityName = classActivity.getName()
                    scheduleItems = classActivity.getScheduleItems()                
                    for scheduleItem in scheduleItems:
                        schedulDateTime = scheduleItem.getDateTime() # schedule date time
                        schedulDateTime = self.backend.convertToLocal(self.backend.formatAsDatetime(schedulDateTime)) # convert string to datetime
                        scheduleStartTime = self.backend.formatTime(schedulDateTime) # start time
                        scheduleDate = self.backend.formatDate(schedulDateTime)
                        if today == scheduleDate:
                            promptCurrentTime = strftime('%I:%M:%S %p')
                            format = '%I:%M:%S %p'
                            checkTime = timedelta(seconds = 300)

                            if (datetime.strptime(scheduleStartTime, format) - datetime.strptime(promptCurrentTime, format)).seconds < checkTime.seconds:
                                messagebox.showinfo(None, "Time for class!")
                                self.root.after(60000, self.prompt)
   
   def onClickLittleAssistant(self):
        global callback
        global count
        self.wave.config(image=next(self.images))
        count = count + 1
        if(count == 59):
            self.wave.after_cancel(callback)
            count = 0
        else:
            callback = self.wave.after(25, self.onClickLittleAssistant)

   def onClickGoToClass(self):
       self.onClickLittleAssistant()
       print('go to class method')
       GoToClass(self,self.root,self.backend)
       self.gray_schedule()
       self.gray_hallway()

   def classPic(self, topFrame):  
        #photo = Image.open('student/frontEnd/images/erin.jpg') #open image
        photo = Image.open(self.backend.parent.children[self.backend.currChild].image)
        
        resized = photo.resize((100, 120), Image.ANTIALIAS) #resize
        correctedImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage        
        self.pictureFrame = Label(topFrame, image=correctedImage, anchor=NE)
        self.pictureFrame.image = correctedImage #do this so image isnt lost in garbage collection
        self.pictureFrame.grid(column=3, row=0, rowspan=2, sticky="E")

   def bannerPhoto(self, topFrame):
        photo = Image.open('student/frontEnd/images/orangePic3.png') #open image
        resized = photo.resize((175, 75), Image.ANTIALIAS) #resize
        correctedImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage        
        self.pictureFrame = Label(topFrame, image=correctedImage, anchor=NE, bg="white")
        self.pictureFrame.image = correctedImage #do this so image isnt lost in garbage collection
        self.pictureFrame.grid(column=0, row=0, rowspan=2, sticky="W")

       
   #def button_setup(self, rightFrame, topFrame):  

               
   def show_hallway(self, frame_class):
        new_center = frame_class(self)
        if self.centerFrame is not None:
            self.centerFrame.destroy()
        self.centerFrame = new_center
        self.centerFrame.pack(fill=BOTH, expand=True)
        self.orange_hallway()
        self.gray_schedule()

   def show_schedule(self, frame_class):
        new_center = frame_class(self, self.backend)
        if self.centerFrame is not None:
            self.centerFrame.destroy()
        self.centerFrame = new_center
        self.centerFrame.pack(fill=BOTH, expand=True)
        self.orange_schedule()
        self.gray_hallway()

   def orange_hallway(self):
        photo = Image.open('student/frontEnd/images/hallway_orange.png') #open image
        resized = photo.resize((125, 50), Image.ANTIALIAS) #resize
        correctedImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage
        self.goToHallway.configure(image=correctedImage)       
        self.goToHallway.image = correctedImage
        
   def gray_hallway(self):
        photo = Image.open('student/frontEnd/images/hallway_gray.png') #open image
        resized = photo.resize((125, 50), Image.ANTIALIAS) #resize
        correctedImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage
        self.goToHallway.configure(image=correctedImage)       
        self.goToHallway.image = correctedImage

   def orange_schedule(self):
        photo = Image.open('student/frontEnd/images/schedule_orange.png') #open image
        resized = photo.resize((125, 50), Image.ANTIALIAS) #resize
        correctedImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage
        self.goToSchedule.configure(image=correctedImage)       
        self.goToSchedule.image = correctedImage

   def gray_schedule(self):        
        photo = Image.open('student/frontEnd/images/schedule_gray.png') #open image
        resized = photo.resize((125, 50), Image.ANTIALIAS) #resize
        correctedImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage
        self.goToSchedule.configure(image=correctedImage)       
        self.goToSchedule.image = correctedImage

   def show_browser(self, frame_class):  
        self.wHeight = self.root.winfo_height()
        self.wWidth = self.root.winfo_width()

        new_center = frame_class(self)
        if self.centerFrame is not None:
            self.centerFrame.destroy()
        self.centerFrame = new_center
        self.centerFrame.configure(height=int(self.wHeight*.75),width=int(self.wWidth*.7))
        self.centerFrame.pack(fill=BOTH, expand=False)
        self.centerFrame.pack_propagate(0)
        
        self.root.update()
        self.topFrame.update()
        self.centerFrame.update()

        self.wHeight = self.root.winfo_height()
        self.wWidth = self.root.winfo_width()
        print ('root size:',self.root.winfo_geometry())
        print ('topframe size:',self.topFrame.winfo_geometry())
        print ('centerFrame size:',self.centerFrame.winfo_geometry())
        
            
        
   def parentView(self):
        global win2
     #    try:
     #        if win2.state() == "normal": win2.focus()
     #    except NameError as e:
     #   print(e)
        win2 = Toplevel(self.root)
        win2.geometry("400x300")
        ParentAccess(win2, self.backend)  
               


   def changeTime(self):
        global win2
     #    try:
     #        if win2.state() == "normal": win2.focus()
     #    except NameError as e:
     #         print(e)    
        win2 = Toplevel(self.root)
        win2.geometry("600x400")       
        ChangeTime(win2)
