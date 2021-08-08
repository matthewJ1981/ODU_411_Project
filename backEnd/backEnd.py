from __future__ import print_function
# System path stuff
import os, sys
sys.path.insert(0, os.path.abspath("../database"))
sys.path.insert(0, os.path.abspath("../Macro"))

# google
import datetime
from datetime import date, timedelta
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Database
from database import database

# Datetime
import datetime as dt

# Date utilities, pytz, and tzlocal. I can't remember which we are using at this point
from dateutil import tz
import pytz
from tzlocal import get_localzone

# Input listener for data input.  - This part may need to be done in the input listener in the front end.
from InputListener import *

# Parent and child classes
from cParent import Parent
from cChild import Child
from cMessage import Message
from reports import Reports

class BackEnd():
    # Enter and exit are used for the Python 'with' statement
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self.delete
        except:
            pass

    def __init__(self):
        # Create database object.  This just initiates the connection and tables
        self.db = database()
        # This just executes the mysql command 'use littlelearners'.  It is necessary during development when creating or resetting the tables
        self.db.useDB()
        #local data structure starts with the parent
        self.parent = None
        #store the index of the current logged in child
        self.currChild = None
        # Format of the date string
        self.dateFormat = "%m/%d/%y"
        # Format of the time string
        self.timeFormat = "%I:%M:%S %p"
        # Format of entire string stored in the db
        self.dtFormat = self.dateFormat + " " + self.timeFormat

        self.dtFormatMicro = self.dateFormat + " " + "%I:%M:%S:%f %p"
        # listener for input data tracking
        self.listener = None
        #Chat messages
        self.messages = []
        self.newMessages = []
        self.reports = Reports(self)

    #This reads the parent id stored in the .ll file and recursivley pulls everythinfg from the database for this parent and their children
    #Structure is
    #Parent
    #   Child
    #       Class
    #           Activity
    #               Schedule items
    #       Help request    
    #       Macro element
    #       Log entry
    #       Input data
    #   Help response
    #
    # Database is updated via the pushupates method.
    # This data is upated with database data with the update method 
    #
    # Not sure about bubbles atm

    def init(self):
        file = open(".ll", "r")
        id = file.readline()
        file.close()
        #print(self.db.parent.getByID(id))
        self.parent = Parent(self.db.parent.getByID(id), self.db)

        #This clears the hasUpdate table
        self.db.remUpdate()

        #print("Tables with changes: " + str(self.db.getUpdate()))

    # Do this when the backend object is destroyed
    def delete(self):
        os.remove(".ll") # This is useful when running init a lot and creating new parent ids
        self.parent = None
        self.currChild = None
        self.listener.stop()
        self.listener = None

    #set the current child index, and start the input data listener
    def initChild(self, index):
        self.currChild = index
        self.listener = Listener(self) ##################### input data Listener
        #print('the child listener is commented out. backend.py line 111')

######################## MESSAGES ###################################################################

    #Get help requests and responses with the name 'You' for the child
    def getMessagesAsChild(self):
        self.getMessages(self.parent.firstName, 'You', self.currChild)

    #Get help requests and responses with the name 'You' for the parent
    def getMessagesAsParent(self, childIndex):
        self.getMessages('You', self.parent.children[childIndex].name, childIndex)

    #Get help requests and responses, sort them by datetime, and return, name, msg, and datetime as string
    def getMessages(self, pName, cName, childIndex):
        #sort by 3rd value in the tuple, which is datetime
        def sortBy(res):
            return res[2]
        temp = []
        result = []

        #Get parent responses
        for x in self.parent.helpResponses:
            dt = self.formatAsDatetime(x.dateTime)
            temp.append((pName, x.msg, self.convertToLocal(dt)))
        
        #Get child requests
        for x in self.parent.children[childIndex].helpRequests:
            dt = self.formatAsDatetime(x.dateTime)
            temp.append((cName, x.msg, self.convertToLocal(dt)))

        temp.sort(key = sortBy)

        #format datetimes back to string
        for x in temp:
            result.append((x[0], x[1], self.formatAsString(x[2])))

        #debug
        # print("DEBUG")
        # for x in result:
        #     print(x)

        return result
        
    #Add new help request for current child
    def addHelpRequest(self, msg):
        self.parent.children[self.currChild].addHelpRequest(msg, self.formatAsString(self.UTCNow()))

    def addHelpResponse(self, msg, id):
        self.parent.addHelpResponse(msg, self.formatAsString(self.UTCNow()), id)


################## RAISE HAND AND NAVIGATION #####################################################################3

    #Set the raised hand attribute to 1 for the current logged in child
    def raiseHand(self):
        self.parent.children[self.currChild].setRaisedHand(1)
    # Set the raised hand attribute to 0 for the current logged in child.
    def unraiseHand(self):
        self.parent.children[self.currChild].setRaisedHand(0)
        
    # Get all the log entry records for the current child to display them on the navigation history page in the parent portal
    def getLogEntries(self):
        print("Getting Log Entries")
        result = []
        convert = {0: "Failure", 1: "Success"}
        for child in self.parent.getChildren():
            for entry in child.getLogEntries():
                tup = (child.getName(), entry.getDateTime(), convert[entry.getNavState()])
                result.append(tup)

        return result

    #Add a log entry when navigation is successful
    def navSuccess(self):
        child = self.parent.getChildren()[self.currChild]
        child.addLogEntry(self.UTCNow(), True)

    #Add a log entry when navigation is unsuccessful, also alert the parent
    def navFailed(self):
        child = self.parent.getChildren()[self.currChild]
        child.addLogEntry(self.UTCNow(), False)
        child.setNavFailed(1)

################ DATE TIME STUFF #########################################################################

    #Create datetime object with local timezone
    def createDateTime(self, month, day, year, hour, minute):
        return dt.datetime(year, month, day, hour, minute, 0, 0, get_localzone())

    #Convert local datetime object to utc time
    def convertToUtc(self, dateTime):
        return dateTime.replace(tzinfo = dt.timezone.utc)

    #Convert utc datetime object to local time
    def convertToLocal(self, dateTime):
        return dateTime.astimezone(get_localzone())

    #Convert datetime object to string
    def formatAsString(self, dateTime):
        return dateTime.strftime(self.dtFormat)

    def formatAsStringMicro(self, dateTime):
        return dateTime.strftime(self.dtFormatMicro)

    #Remove seconds from the datetime object
    def stripSeconds(self, dateTime):
        return dateTime.replace(second = 0, microsecond = 0)

    #Remove microseconds from the datetime object
    def stripMicro(self, dateTime):
        return dateTime.replace(microsecond = 0)

    #returns datetime object in local time zone 
    def localNow(self):
        return self.convertToLocal(self.UTCNow())

    #returns datetime object in UTC time without microseconds
    def UTCNow(self):
        return self.stripMicro(self.convertToUtc(dt.datetime.utcnow()))
        
    def UTCNowMicro(self):
        return self.convertToUtc(dt.datetime.utcnow())

    #Convert string to datetime
    def formatAsDatetime(self, string):
        temp = dt.datetime.strptime(string, self.dtFormat)
        return temp.replace(tzinfo = dt.timezone.utc)

    def formatAsDatetimeMicro(self, string):
        temp = dt.datetime.strptime(string, self.dtFormatMicro)
        return temp.replace(tzinfo = dt.timezone.utc)
        
    #convert datetime to time as string
    def formatTime(self, dateTime):
        return dateTime.strftime(self.timeFormat)
    
    #convert datetime to date as string
    def formatDate(self, dateTime):
        return dateTime.strftime(self.dateFormat)


################# UPDATES ##############################################################################3
    
    def checkCalendarUpdate(self):
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        
        service = build('calendar', 'v3', credentials=creds)

        children = self.parent.getChildren()
        for child in children:
            childName=child.getName()
            print(childName)
            studentClasses = child.getClasses()
            if studentClasses != []: 
                for studentClass in studentClasses:
                    className = studentClass.getName()
                    print(className)
                    classTeacherName= studentClass.getTeacherName()
                    calendarID=studentClass.getCalendarID()

                    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
                    next_monday = self.next_weekday()
                    nextWeek=str(next_monday) + str(now)[10:]
                    #try:
                    events_result = service.events().list(calendarId=calendarID, 
                                            timeMin=now,
                                            timeMax=nextWeek,
                                            maxResults=25,
                                            singleEvents=True,
                                            orderBy='startTime'
                                            ).execute()
                    events = events_result.get('items', [])

                    googleEventIDList=[]
                    eventList=[]
                    eventIDList=[]

                    for event in events:
                        start = event['start'].get('dateTime', event['start'].get('date'))
                        scheduleInfo=str(start + " " + event['summary'])
                        
                        start1 = str(str(event['start'].get('dateTime', event['start'].get('date'))).replace('T',' ',1))[0:19]
                        timeZone=str(start[19:]).replace(':','',1)
                        hourOffSet=int(timeZone[1:3])
                        minOffSet=int(timeZone[3:6])

                        datetimeGoogle=start1 + timeZone

                        classTime_obj = dt.datetime.strptime(datetimeGoogle , '%Y-%m-%d %H:%M:%S%z')
                        classTime_obj1=classTime_obj + timedelta(minutes=minOffSet, hours=hourOffSet)
                        googleSchedulDateTime=self.convertToLocal(classTime_obj1)
                        googleStartTime = self.formatTime(googleSchedulDateTime)
                        googleDate = self.formatDate(googleSchedulDateTime)

                        googleActivityTime = googleDate + " " + googleStartTime
                        googleActivityName=event.get('summary')
                        googleURL=event.get('description')
                        googleEventID=event.get('htmlLink')[42:]
                        googleEventIDList.append(googleEventID)
                
                        classActivities = studentClass.getActivities()
                        if classActivities != []:
                            for classActivity in classActivities:
                                activityName = classActivity.getName()
                                scheduleItems = classActivity.getScheduleItems()
                                for scheduleItem in scheduleItems:
                                    schedulDateTime = scheduleItem.getDateTime() # schedule date time
                                    
                                    linkName = classActivity.getURL()
                                    eventID=classActivity.getEventID()
                                    
                                    eventList.append(eventID)

                                    if(eventID==googleEventID):
                                        if(activityName!=googleActivityName):
                                            print("activity names do not match")
                                            print(activityName)
                                            print(googleActivityName)
                                            classActivity.setName(googleActivityName)
                                        #I took this out so we can change the url during presentation and google wont overwrite it
                                        #elif(linkName!=googleURL):
                                        #    print("URL does not match")
                                        #    print(activityName)
                                        #    print(linkName)
                                        #    print(googleActivityName)
                                        #    print(googleURL)
                                        #    classActivity.setURL(googleURL)
                                        elif(schedulDateTime!=googleActivityTime):
                                            print("time does not match")
                                            print(activityName)
                                            print(scheduleItem.getDateTime())
                                            print(googleActivityName)
                                            print(googleActivityTime)
                                            scheduleItem.setDateTIme(googleActivityTime)

                    #looking for an event google found that is not in littleLearners
                    print(len(googleEventIDList))
                    for item in eventList:
                        if not item in eventIDList:
                            eventIDList.append(item)

                    if not (all(x in eventIDList for x in googleEventIDList)):
                        for x in googleEventIDList:
                            if (x in eventIDList):
                                continue
                            else:
                                newEventId=x
                                for event in events:
                                    if(newEventId==event.get('htmlLink')[42:]):
                                        start = event['start'].get('dateTime', event['start'].get('date'))
                                        scheduleInfo=str(start + " " + event['summary'])
                                        description=event.get('description')
                                        
                                        start1 = str(str(event['start'].get('dateTime', event['start'].get('date'))).replace('T',' ',1))[0:19]
                                        timeZone=str(start[19:]).replace(':','',1)
                                        hourOffSet=int(timeZone[1:3])
                                        minOffSet=int(timeZone[3:6])

                                        datetimeGoogle=start1 + timeZone

                                        classTime_obj = dt.datetime.strptime(datetimeGoogle , '%Y-%m-%d %H:%M:%S%z')
                                        classTime_obj1=classTime_obj + timedelta(minutes=minOffSet, hours=hourOffSet)


                                        if(str(description)=="None"):
                                            activitie=self.db.activity.add(str(event.get('summary')),studentClass.getID(),False,"None",newEventId)
                                            eventIDList.append(newEventId)
                                        else:
                                            activitie=self.db.activity.add(str(event.get('summary')),studentClass.getID(),False,description,newEventId)
                                            eventIDList.append(newEventId)

                                        self.db.scheduleItem.add(self.formatAsString(classTime_obj1), "30", activitie)


                    print(len(eventIDList))


                    #except:
                        #print("Current Class is not google")


    #Check the hasUpdate table and update the local data structure if there are changes
    def update(self, user):
        self.pushUpdates()
        tables = self.db.getUpdate()
        # print("Updating from tables: " + str(tables))
        for t in tables:
            if t == "Parent":
                self.parent.update()

            elif t == "HelpResponse":
                self.parent.initHelpResponses()

            elif t == "Child":
                self.parent.initChildren()


            elif t == "Class":
                for c in self.parent.getChildren():
                    c.initClasses()

            elif t == "Activity":
                for c in self.parent.getChildren():
                    for cl in c.getClasses():
                        cl.initActivities()

            elif t == "ScheduleItem":
                for c in self.parent.getChildren():
                    for cl in c.getClasses():
                        for a in cl.getActivities():
                            a.initScheduleItems()

            elif t == "HelpRequest":
                for c in self.parent.getChildren():
                    c.initHelpRequests()

            elif t == "MacroElement":
                for c in self.parent.getChildren():
                    c.initMacroElements()
            
            elif t == "LogEntry":
                for c in self.parent.getChildren():
                    c.initLogEntries()

            elif t == "InputData":
                for c in self.parent.getChildren():
                    c.initInputData()

            elif t == "EnrolledIn":
                for c in self.parent.getChildren():
                    c.initClasses()

            else:
                continue

            self.db.remUpdate(t, user)
            
        #debug output
        #self.parent.print()

    #Push local changes to the database
    def pushUpdates(self):
        # print("Pushing updates")
        self.parent.pushUpdates()
        for child in self.parent.getChildren():
            child.pushUpdates()
            for _class in child.getClasses():
                _class.pushUpdates()
                for activity in _class.getActivities():
                    activity.pushUpdates()
                    for item in activity.getScheduleItems():
                        item.pushUpdates()

            for help in child.getHelpRequests():
                help.pushUpdates()
            for elem in child.getMacroElements():
                elem.pushUpdates()
            for log in child.getLogEntries():
                log.pushUpdates()
            for data in child.getInputData():
                data.pushUpdates()
        for response in self.parent.getHelpResponses():
            response.pushUpdates()


########################## EVERYTHING ELSE ##################################################

    #Console output
    def print(self):
        self.parent.print()

    #Remove the .ll when parent logs out
    def logOut(self):
        try:
            os.remove(".ll")
        except:
            print("Error in parentBackEnd.py, trying to remove .ll file.")
            
    def login(self, username, password):
        returnCode = ""
        returnMessage = ""

        if not self.db.userExists(username):
            returnCode = "001"
            returnMessage = "username does not exist"
        #Incorrect password
        elif not self.db.verifyPassword(username, password):    
            returnCode = "002"
            returnMessage = "Password does not match user"
        #Log in  
        else:
            id = self.db.parent.getID((username,))
            returnCode = "000"
            returnMessage = "Success"

            file = open(".ll", "w")
            file.write(str(id))
            file.close()
            self.init()
            #self.parent.print()

        return (returnCode, returnMessage)
        

    def register(self, username, password, email, firstName, lastName, phoneNumber):
        returnCode = ""
        returnMessage = ""

        #username already exists
        if self.db.userExists(username):
            returnCode = "011"
            returnMessage = "username already exists"

        #password not long enough
        elif not self.db.strongPassword(password):
            returnCode = "012"
            returnMessage = "Password must be at least 8 characters"

        #Add user
        else:
            self.db.parent.add(username, password, email, firstName, lastName, phoneNumber)
            returnCode = "000"
            returnMessage = "New user created"

        return (returnCode, returnMessage)

    #helper function for newClass
    def next_weekday(self):
        days_ahead = date.today().weekday() - date.today().weekday()
        if days_ahead <= 0: # Target day already happened this week
            days_ahead += 7
        return date.today() + datetime.timedelta(days_ahead)

    #Makes a new class after adding a Calenda
    def newClass(self,className,teacherName,calendarID,student):
        dbNewClass=self.db._class.add(className,teacherName,calendarID)
        self.db.enrolledIn.add(student, dbNewClass)
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

        d = date.today()
        next_monday = self.next_weekday()
        nextWeek=str(next_monday) + str(now)[10:]

        events_result = service.events().list(calendarId=calendarID, 
                                              timeMin=now,
                                              timeMax=nextWeek,
                                              maxResults=25,
                                              singleEvents=True,
                                              orderBy='startTime'
                                             ).execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            start1 = str(str(event['start'].get('dateTime', event['start'].get('date'))).replace('T',' ',1))[0:19]
            timeZone=str(start[19:]).replace(':','',1)
            hourOffSet=int(timeZone[1:3])
            minOffSet=int(timeZone[3:6])

            datetimeGoogle=start1 + timeZone
            description=event.get('description')
            scheduleInfo=str(start + " " + event['summary'])
            eventId=event.get('htmlLink')[42:]

            classTime_obj = dt.datetime.strptime(datetimeGoogle , '%Y-%m-%d %H:%M:%S%z')
            classTime_obj1=classTime_obj + timedelta(minutes=minOffSet, hours=hourOffSet)
            print(classTime_obj1)


            try:
                if(str(description)=="None"):
                    activitie=self.db.activity.add(str(event.get('summary')),dbNewClass,False,"None",eventId)
                else:
                    activitie=self.db.activity.add(str(event.get('summary')),dbNewClass,False,description,eventId)
            except:
                activitie=self.db.getByActivity()

            self.db.scheduleItem.add(self.formatAsString(classTime_obj1), "30", activitie)

        
    def checkRaisedHand(self):

        # print("Checking raised hand")
        result = []
        for child in self.parent.getChildren():
            if child.getRaisedHand() == 1:
                child.setRaisedHand(0)
                reqs = child.getHelpRequests()
                if reqs != []:
                    result.append((child.id, child.getName(), reqs[0].getMsg()))

        #print("needHelp: " + str(result))
        return result

    def checkHelpResponses(self):
        if self.parent.helpResponses != [] and self.parent.helpResponses[0].getNew() == 1:
            self.parent.helpResponses[0].setNew(0)
            return self.parent.helpResponses[0].getMsg()
        
        return None

    #Check if any of the current parent's children navigation has failed and returns their names if so
    def checkNavFailed(self):

        result = []
        for child in self.parent.getChildren():
            if child.getNavFailed() == 1:
                child.setNavFailed(0)
                result.append(child.getName())

        return result