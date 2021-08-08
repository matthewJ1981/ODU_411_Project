import sys
from tkinter import *
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
import ctypes, sys
import os
import platform
import logging as _logging
from time import strftime
from PIL import ImageTk,Image
from datetime import datetime, timedelta
from datetime import date

import pytz


class ChangeTime():
    def __init__(self, root):
        root.title("littleLEARNERS - Change System Time")
        self.fm = Frame(root)
        self.fm.configure(background='white', padx=25, pady=25) 
        self.fm.pack(fill=BOTH, expand=True)
        self.fm.columnconfigure((0, 1), weight=1)     
        self.fm.rowconfigure((0, 1, 2, 3, 4), weight=1)

        def setup_icon():          
            p1 = PhotoImage(file = 'student/frontEnd/images/icon.png')
            root.iconphoto(False, p1) 

        
        def time_entry():
            self.timeLabel= Label(self.fm, text="Change System Time", bg='#ffffff', pady=10, padx=10, font = ('montserrat', 20, 'bold'))
            self.timeLabel.grid(row=0,column=0, columnspan=2)

            self.hourLabel= Label(self.fm, text="Enter Desired Hour", bg='#ffffff', font = ('montserrat', 14, 'bold'))
            self.hourLabel.grid(row=1,column=0)
            self.hourEntry = Entry(self.fm)
            self.hourEntry.grid(row=1,column=1)

            self.minuteLabel= Label(self.fm, text="Enter Desired Minute", bg='#ffffff', font = ('montserrat', 14, 'bold'))
            self.minuteLabel.grid(row=2,column=0, sticky="N")
            self.minuteEntry = Entry(self.fm)
            self.minuteEntry.grid(row=2,column=1, sticky="N")

            photo = Image.open('student/frontEnd/images/enter.png') #open image
            resized = photo.resize((100, 35), Image.ANTIALIAS) #resize
            correctedImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage
            self.enter=Button(self.fm, image=correctedImage, borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff', command=lambda: changeTime(self.hourEntry.get(), self.minuteEntry.get()))
            self.enter.image = correctedImage
            self.enter.grid(row=3, column =1)

            photo = Image.open('student/frontEnd/images/exit.png') #open image
            resized = photo.resize((100, 34), Image.ANTIALIAS) #resize
            correctedImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage
            self.enter=Button(self.fm, image=correctedImage, borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff', command=lambda: root.destroy())
            self.enter.image = correctedImage
            self.enter.grid(row=4, column = 1, sticky="N")


        def _win_set_time(time_tuple):
            import win32api
            f=open("../timezone")

            utc_now = pytz.utc.localize(datetime.utcnow())
            pst_now = utc_now.astimezone(pytz.timezone(f.read()))
            upDown=str(pst_now.isoformat())[26:27]
            hourOffSet=int(str(pst_now.isoformat())[27:29])
            minuteOffSet=int(str(pst_now.isoformat())[30:])

            today = date.today()
            if(time_tuple[3]<=9):
                newHour="0"+str(time_tuple[3])
            else:
                newHour=str(time_tuple[3])
            
            if(time_tuple[4]<=9):
                newMinute="0"+str(time_tuple[4])
            else:
                newMinute=str(time_tuple[4])
            newDateTime=today.strftime("%m")+"/"+today.strftime("%d")+"/"+today.strftime("%Y")+ " " +  newHour + ":" + newMinute

            newDateTimeUTC_obj = datetime.strptime(newDateTime , '%m/%d/%Y %H:%M')

            if(upDown=='-'):
                newDateTimeLocal_obj = newDateTimeUTC_obj + timedelta(minutes=minuteOffSet, hours=hourOffSet)
            else:
                newDateTimeLocal_obj = newDateTimeUTC_obj - timedelta(minutes=minuteOffSet, hours=hourOffSet)

            newTime_tuple = (int(newDateTimeLocal_obj.strftime("%Y")),  # Year
                          int(newDateTimeLocal_obj.strftime("%m")),  # Month
                          int(newDateTimeLocal_obj.strftime("%d")),  # Day
                          int(newDateTimeLocal_obj.strftime("%H")),  # Hour
                          int(newDateTimeLocal_obj.strftime("%M")),  # Minute
                          0,  # Second
                          0,  # Millisecond
                          )

            print(str(newDateTimeLocal_obj))
            dayOfWeek = datetime(*newTime_tuple).isocalendar()[2]
            t = newTime_tuple[:2] + (dayOfWeek,) + newTime_tuple[2:]
            win32api.SetSystemTime(*t)

        def _linux_set_time(time_tuple):
            import subprocess
            import shlex
            
            time_string = datetime(*time_tuple).isoformat()

            subprocess.call(shlex.split("timedatectl set-ntp false"))  # May be necessary
            subprocess.call(shlex.split("sudo date -s '%s'" % time_string))
            subprocess.call(shlex.split("sudo hwclock -w"))


        def changeTime(hour, minute):
            today = date.today()
            time_tuple = (int(today.strftime("%Y")),  # Year
                          int(today.strftime("%m")),  # Month
                          int(today.strftime("%d")),  # Day
                          int(hour),  # Hour
                          int(minute),  # Minute
                          0,  # Second
                          0,  # Millisecond
                          )
            
            if sys.platform == 'linux' or sys.platform == 'darwin':
                _linux_set_time(time_tuple)
            elif sys.platform == 'win32' or sys.platform == 'cygwin':
                _win_set_time(time_tuple)

        setup_icon()
        time_entry()       
      
