from tkinter import *
import tkinter as tk
from tkinter import font as tkFont
import ctypes, sys
import os
import platform
from PIL import ImageTk,Image
import webbrowser

from Macro.ExecuteMacro import *
from Macro.Containers import *
from time import strftime 
from datetime import datetime, timedelta
from datetime import date
from student.frontEnd.ChildEmbeddedBrowser import MainFrame



sys.path.insert(0, os.path.abspath("./student/frontEnd/"))
from childDashboard import *

class GoToClass():
    def __init__(self, dashboard,root,backend):
        print('Entering GoToClass.py')
        
        self.parent = dashboard
        self.root = root
        self.backend = backend
        self.child = Child()

        #get child info
        children = backend.parent.getChildren()
        ch = children[self.backend.currChild]
        cid = children[self.backend.currChild].id
        self.child.setup(backend, cid)
        self.currentItems = []

        #todays date
        today = datetime.today()
        self.today = today.strftime("%m/%d/%y")
        print("self.today =", self.today)

        #current time
        now = datetime.now()
        tempNow = now.strftime("%H:%M:%S")
        self.currentTime = datetime.strptime(tempNow,"%H:%M:%S")
        self.currentHour = self.currentTime.hour
        self.currentMinute = self.currentTime.minute
        print('self.currentTime =',self.currentHour, 'min',self.currentMinute)

        #reset browser
        self.parent.show_browser(MainFrame)

        self.getTodaysItems()
        self.currentScheduleItem = self.determineCurrentActivity()
        if self.currentScheduleItem is not None:
            self.navigateToActivity()
        else:
            print('no activtity at this time')
            #notify student
            self.notifyNoActivity()

        
    def notifyNoActivity(self):
        self.font = font.Font(family="montserrat",size="16",weight="bold")
        self.window = tk.Toplevel()
        self.window.attributes('-topmost','true')
        self.window.configure(bg='white')
        self.rootX = self.parent.topFrame.winfo_x()
        self.rootY = self.parent.topFrame.winfo_y()
        self.window.geometry("+%d+%d" % (self.rootX + 350, self.rootY + 350))

        self.noActivityLabel = Label(self.window, font=self.font,text="There is no activity scheduled at this time.",borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff')
        self.noActivityLabel.grid(row=0,column=0,padx=10,pady=10)

        photo = Image.open('student/frontEnd/images/okay.png') #open image
        resized = photo.resize((100, 35), Image.ANTIALIAS) #resize
        self.okImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage

        self.okButton = Button(self.window, image=self.okImage, borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff',command=lambda:self.window.destroy())
        self.okButton.grid(row=1,column=0, pady=10)

    def getTodaysItems(self):
        date = None
        time = None
        ampm = None

        allItems = []
        
        for s in self.child.scheduleItems:
            scheduleDateTime = s.getDateTime() # schedule date time
            scheduleDateTime = self.backend.convertToLocal(self.backend.formatAsDatetime(scheduleDateTime))
            scheduleDateTime = self.backend.formatAsString(scheduleDateTime)
            date,time,ampm = scheduleDateTime.split()
            time = time + ' ' + ampm
            tempItem = ScheduledItemContainer()
            tempItem.id = s.id
            tempItem.date = date
            tempItem.time = time
            tempItem.hour,tempItem.minute = self.convertTo24(time)
            tempItem.ampm = ampm
            tempItem.activityId = s.activityID
            tempItem.duration = 30
            tempItem.dateTime = s.dateTime
            #tempItem.print()
            allItems.append(tempItem)

        for s in allItems:
            #if s.date == '04/23/21': #for testing - remove this#########################################################################################################3
             #   s.date = '04/24/21'
            for a in self.child.activities:
                if s.activityId == a.id:
                    s.activityName = a.name
            #s.print()

        
        #add only items for today
        print('All activities:')
        for item in allItems:
            item.print()
            if self.today == item.date:
                self.currentItems.append(item)
        print('---------------------------------------------------')
        

       # print("Today's Activities")
        #for item in self.currentItems:
         #   item.print()
        #print("end today's activities")
            


        #sort by time
        self.currentItems.sort(key=lambda x: (x.hour, x.minute))
        print("Today's activities (sorted by time)")
        for item in self.currentItems:
            item.print()
        print("---------------------------------------------------")
                

    def convertTo24(self,time):
        
        in_time = datetime.strptime(time, "%I:%M:%S %p")
        out_time = datetime.strftime(in_time, "%H:%M:%S")
        time = datetime.strptime(out_time,"%H:%M:%S")
        print("hour %s min %s" % (time.hour, time.minute))
        return int(time.hour), int(time.minute)

    def determineCurrentActivity(self):
        currentItem = None
        now = datetime.now()
        curTime = datetime.strptime(str(self.currentHour)+':'+str(self.currentMinute), '%H:%M')

        print("comparing current time to times of today's activities:")
        for i in range(0,len(self.currentItems)):
            itime = datetime.strptime(str(self.currentItems[i].hour)+':'+str(self.currentItems[i].minute), '%H:%M')
            #check items after current time
            if curTime < itime:
                difference = itime - curTime
                print('ahead difference: ',int((difference.total_seconds())/60),'minutes')
                #if 5 mins or less before activity start time, return activity
                if int((difference.total_seconds())/60) <= 5:
                    return self.currentItems[i]
            #check items before current time
            else:
                difference = curTime - itime
                print('behind difference',int((difference.total_seconds())/60),'minutes')
                #if <30 mins since activity started, set as current activity
                if int((difference.total_seconds())/60) < 30:
                    currentItem = self.currentItems[i]
        return currentItem


    def navigateToActivity(self):
        for a in self.child.activities:
            if self.currentScheduleItem.activityId == a.id:
                print('activity',a.name,'url:',a.url)
                print(a.hasMacro)
                hasMacro = a.hasMacro
                link = a.url
                name = a.name
                actid = a.id
                break

        print('activity name',name,actid)
        if hasMacro:
            print('Navigating With Macro')
            ####from parent class
            for macro in self.child.macros:
                if macro.activityId == actid:
                    self.child.currentMacro = macro
                    break
                else:
                    print(macro.activityId)

            self.child.parentPlayback = False
            print("Playing Macro:",self.child.currentMacro.name)
        
            self.root.after(500,lambda:ExecuteMacro(self.parent,self.child.currentMacro.elements,self.backend,self.child, False))

        else:
            print('Navigating With Link')
            print('incoming:',link)
            if 'zoom.us' in link:
                webbrowser.open(link, new=2)
            elif 'Zoom.us' in link:
                webbrowser.open(link, new=2)
            elif 'bit.ly' in link:
                webbrowser.open(link, new=2)
            else:
                self.root.after(500,lambda:self.parent.centerFrame.navigate(link))


        


class ScheduledItemContainer:
    def __init__(self):
        
        self.id = None
        self.activityId = None
        self.activityName = None
        self.dateTime = None
        self.date = None
        self.time = None
        self.hour = None
        self.minute = None
        self.ampm = None
        self.duration = None
        self.url = None
    
        

    def print(self):
        print("id:",self.id,
              "activity id:",self.activityId,
              "activity name:",self.activityName,
              "dateTime:", self.dateTime,
              "date",self.date,
              "time",self.time,
              "ampm",self.ampm,
              "duration",self.duration,
              "hour",self.hour,
              "minute",self.minute)
             







