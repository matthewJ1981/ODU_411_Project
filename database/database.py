import mysql.connector
import os
import sys

from dbConnect import dbConnect
from dbParent import Parent
from dbChild import Child
from dbClass import Class
from dbEnrolledIn import EnrolledIn
from dbScheduleItem import ScheduleItem
from dbNavElemType import NavElemType
from dbNavigationStep import NavigationStep
from dbBubble import Bubble
from dbMemberOf import MemberOf
from dbHelpRequest import HelpRequest
from dbHelpResponse import HelpResponse
from dbUserType import UserType
from dbUser import User
from dbErrorCode import ErrorCode
from dbLogEntry import LogEntry
from dbInputData import InputData
from dbActivity import Activity
from dbMacroElement import MacroElement
from dbMessage import Message

import datetime as dt
import time

from dbTestInit import dbInit

class database:
    def __init__(self, _host = "default"):
        self.db = dbConnect(_host)
        self.parent = Parent(self.db.cnx())
        self.child = Child(self.db.cnx())
        self._class = Class(self.db.cnx())
        self.enrolledIn = EnrolledIn(self.db.cnx())
        self.scheduleItem = ScheduleItem(self.db.cnx())
        #self.navElemType = NavElemType(self.db.cnx())
        #self.navigationStep = NavigationStep(self.db.cnx())
        self.bubble = Bubble(self.db.cnx())
        self.memberOf = MemberOf(self.db.cnx())
        self.helpRequest = HelpRequest(self.db.cnx())
        self.helpResponse = HelpResponse(self.db.cnx())
        #self.userType = UserType(self.db.cnx())
        #self.user = User(self.db.cnx())
        #self.errorCode = ErrorCode(self.db.cnx())
        self.logEntry = LogEntry(self.db.cnx())
        self.inputData = InputData(self.db.cnx())
        self.activity = Activity(self.db.cnx())
        self.macroElement = MacroElement(self.db.cnx())
        self.message = Message(self.db.cnx())

    def close(self):
        self.db.close()

    def getUpdate(self):
        result = []
        # convert = {"Bubble": "bubble",
        #             "Child": "Child",
        #             "Class": "class",
        #             "EnrolledIn": "enrolled_in",
        #             "HelpRequest": "help_request",
        #             "HelpResponse": "help_response",
        #             "InputData": "input_data",
        #             "LogEntry": "log_entry",
        #             "MacroElement": "macro_element",
        #             "MemberOf": "member_of",
        #             "Parent": "parent",
        #             "ScheduleItem": "schedule_item",
        #             "Activity": "activity"
        #             }
        for t in self.parent.getUpdate():
            #result.append(convert[t[0]])
            result.append(t[0])

        return result

    #Reset hasUpdate table
    def remUpdate(self, table = None, user = None):
        self.parent.remUpdate(table, user)

    ### Methods to create and use a database for testing
    #Create test database
    def createTestDB(self):
        self.db.createTestDB()

    #Use test database
    def useDB(self):
        self.db.useDB()

    #check if user exists, returns true if username is in parent database
    def userExists(self, username):
        #See if username exists in parent table
        return self.parent.getID((username,)) != None
    
    #Check entered password against stored hash
    def verifyPassword(self, username, password):
        return self.parent.verifyPassword(username, password)

    #checks password strength, returns true or false
    def strongPassword(self, password):
        #Just check length for now
        return len(password) > 7

    #formats python datetime as string D/M/Y H:M:S
    def formatDateTime(self, dateTime):
        return self.parent.formatDateTime(dateTime)

    #### SPECIFIC QUERIES AND GET BY FOREIGN KEYS ####

    #Get all children by parent username
    def getChildren(self, username):
        return self.child.getByParent(self.parent.getID((username,)))

    #Get all children by parent id
    def getChildrenByID(self, pid):
        return self.child.getByParent(pid)

    #Get all schedule items for a specific child
    def getItemsForChild(self, cid):
        result = []
        for child in self.enrolledIn.getByChild(cid):
            for act in self.activity.getByClass(child[0]):
                for schedule_item in self.scheduleItem.getByActivity(act[0]):
                    result.append(schedule_item)
        
        return result

    def getClassesForChild(self, cid):
        result = []
        for e in self.enrolledIn.getByChild(cid):
            result.append(self._class.getByID(e[2]))

        return result

    def getChildrenInClass(self, clid):
        result = []
        for e in self.enrolledIn.getByClass(clid):
            result.append(self.child.getByID(e[2]))

        return result
    
    def getChildrenInClasses(self):
        result = []
        for e in self.enrolledIn.getAll():
            temp = []
            for attr in self.child.getByID(e[1]):
                temp.append(attr)
            for attr in self._class.getByID(e[2]):
                temp.append(attr)
            result.append(tuple(temp))

        return result

    #### REMOVE ALL ####

    #remove everything from the database
    def removeAll(self):
        return (
        self.scheduleItem.removeAll() and 
        self.enrolledIn.removeAll() and 
        self.activity.removeAll() and
        self.helpRequest.removeAll() and
        self.helpResponse.removeAll() and
        self.inputData.removeAll() and
        self.logEntry.removeAll() and
        self._class.removeAll() and
        self.child.removeAll() and
        self.memberOf.removeAll() and
        self.parent.removeAll() and
        self.bubble.removeAll() and
        self.macroElement.removeAll() and
        self.message.removeAll()
        )
        
    def customQuery(self, query, values):
        try:
            self.db.cursor().execute(query, values)
        except Exception as e:
            print(e)
            pass

        return self.db.cursor().fetchall()

if __name__ == "__main__":
    try:
        print("Connecting to database")
        db = database()
        print("Creating database")
        db.createTestDB()
        print("Using database")
        db.useDB()
    except Exception as e:
        print(e)
    else:  
        print("Adding bubble")
        b1 = db.bubble.add("b1")

        # try:
        #     print("Adding user types")
        #     t1 = db.userType.add("Parent")
        #     t2 = db.userType.add("Child")
        # except:
        #     print("User types already added")

        print("Adding Parents")
        p1 = db.parent.add("p1", "12345678", "a@b", "A", "B")
        p2 = db.parent.add("p2", "12345678", "b@a", "A", "B")

        print("Adding Parents to bubble")
        db.memberOf.add(p1, b1)
        db.memberOf.add(p2, b1)

        print("Adding children")
        ch1 = db.child.add("Bob", 4, p1)
        ch2 = db.child.add("John", 4, p2)
        ch3 = db.child.add("Alice", 4, p2)

        # print("Adding error codes")
        # e1 = db.errorCode.add(0, "Navigation error")
        # e2 = db.errorCode.add(1, "Some other error")

        print("Adding Classes")
        cl1 = db._class.add("Math", "Mary")
        cl2 = db._class.add("French", "Tom")

        print("Adding Activities")
        a1 = db.activity.add("Writing", cl1, True)
        a2 = db.activity.add("Reading", cl2, False, "www.google.com")

        print("Adding children to classes")
        db.enrolledIn.add(ch1, cl1)
        db.enrolledIn.add(ch1, cl2)
        db.enrolledIn.add(ch2, cl2)

        print("Adding Schedule items")
        s1 = db.scheduleItem.add(db.formatDateTime(dt.datetime.now()), "60", a1)
        time.sleep(1)
        s2 = db.scheduleItem.add(db.formatDateTime(dt.datetime.now()), "30", a2)

        # print("Adding Navigation steps for schedule items")
        # db.navElemType.add("URL")
        # n1 = db.navigationStep.add("Element", "URL", 1, s1, None)
        # n2 = db.navigationStep.add("Elem", "URL", 2, s1, None)
        # n3 = db.navigationStep.add("More", "URL", 1, s2, None)

        print("Adding macro elements")
        me1 = db.macroElement.add(1, ch1, a1, "Name", "www.google.com", False, "", "", b'100', 50, 60)
        me1 = db.macroElement.add(2, ch1, a1, "Name", "www.google.com", False, "", "", b'120', 80, 100)

        print("Adding log entries")
        db.logEntry.add(ch1, db.formatDateTime(dt.datetime.now()), False)
        time.sleep(1)
        db.logEntry.add(ch2, db.formatDateTime(dt.datetime.now()), True)

        print("Adding data input")
        db.inputData.add(db.formatDateTime(dt.datetime.now()), ch1, 78, 98, "Text")
        time.sleep(1)
        db.inputData.add(db.formatDateTime(dt.datetime.now()), ch1, 334, 124, None)

        print("Adding help request")
        db.helpRequest.add(db.formatDateTime(dt.datetime.now()), ch1, "Help")

        print("Adding help reponse")
        db.helpResponse.add(db.formatDateTime(dt.datetime.now()), p1, ch1, "Go Away")

        print("Bubbles:")
        for b in db.bubble.getAll():
            print(b)

        print("Parents:")
        for p in db.parent.getAll():
            print(p)

        print("Parent in Bubbles")
        for p in db.memberOf.getAll():
            print(p)

        print("Chilren:")
        for c in db.child.getAll():
            print(c)

        # print("Users:")
        # for u in db.user.getAll():
        #     print(u)

        print("Classes:")
        for c in db._class.getAll():
            print(c)  

        print("Acitivities:")
        for a in db.activity.getAll():
            print(a)

        # print("User types")
        # for t in db.userType.getAll():
        #     print(t)

        # print("Error Codes")
        # for e in db.errorCode.getAll():
        #     print(e)

        print("Log entries")
        for e in db.logEntry.getAll():
            print(e)

        print("Input data")
        for d in db.inputData.getAll():
            print(d)

        print("Children in class: ")
        for h in db.enrolledIn.getAll():
            print(h)

        print("Schedule items")
        for s in db.scheduleItem.getAll():
            print(s)

        # print("Navigation Steps")
        # for s in db.navigationStep.getAll():
        #     print(s)

        print("Macro Elements")
        for m in db.macroElement.getAll():
            print(m)

        # print("Navigation Element Types:")
        # for t in db.navElemType.getAll():
        #     print(t)
        
        print("Help requests")
        for r in db.helpRequest.getAll():
            print(r)

        print("Help responses")
        for r in db.helpResponse.getAll():
            print(r)

        print("Classes child " + str(ch1)  +  " is in:")
        for c in db.getClassesForChild(ch1):
            print(c)

        print("Children in class " + str(cl1) + ":")
        for c in db.getChildrenInClass(cl1):
            print(c)    
        
        print("Schedule items for class " + str(cl1) + ":")
        for a in db.activity.getByClass(cl1):
            for s in db.scheduleItem.getByActivity(a[0]):
                print(s)

        print("Schedule items for child " + str(ch1) + ":")
        for s in db.getItemsForChild(ch1):
            print(s)
    
        # print("Navigation steps for Activity " + str(a1) + ":")
        # for s in db.navigationStep.getByActivity(a1):
        #     print(s)

        print("Macro Elements for Activity " + str(a1) + ":")
        for s in db.macroElement.getByActivity(a1):
            print(s)

        print("Macro Elements for Child " + str(ch1) + ":")
        for s in db.macroElement.getByChild(ch1):
            print(s)

        # print("Remove children for parent p1")
        # db.child.removeByParent(p1)
        print("Children in class: ")
        for cc in db.getChildrenInClasses():
            print(cc)

        db.close()