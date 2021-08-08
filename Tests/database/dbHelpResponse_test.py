import pytest
# import os, sys
# sys.path.insert(0, os.path.abspath("database"))

from dbConnect import dbConnect
from dbUserType import UserType
from dbParent import Parent
from dbChild import Child
from dbHelpResponse import HelpResponse
import datetime as dt

class TestDbHelpResonse:
    db = dbConnect()
    db.createTestDB()
    
    name = "Chris"
    age = 8

    username = "testParent"
    password = "testPW"
    email = "testEmail"
    firstName = "testFName"
    lastName = "testLName"
    pid = -1

    dateTime = None
    msg = "Help"
    videoMsg = b'Help'
    url = None

    cid = -1
    fields = []

    #### SETUP ####
    def setup_method(self):
        self.db = dbConnect()
        self.db.useDB()
        self.parent = Parent(self.db.cnx())
        self.child = Child(self.db.cnx())
        self.userType = UserType(self.db.cnx())
        self.currentTable = HelpResponse(self.db.cnx())
        self.addParent()
        self.addChild()
        self.addcurrentTable()
        self.asList()

    #### TEARDOWN ####
    def teardown_method(self):
        self.currentTable.removeAll()
        self.child.removeAll()
        self.parent.removeAll()
        self.db.close()

    #### HELPERS ####
    
    def addParent(self):
        try:
            self.pid = self.parent.add(self.username, self.password, self.email, self.firstName, self.lastName)
        except:
            return -1
        return self.pid

    def addChild(self):
        try:
            self.cid = self.child.add(self.name, self.age, self.pid)
        except:
            return -1

        return self.cid

    def addUserType(self):
        try:
            self.ID = self.userType.add("Parent")
            self.ID = self.userType.add("Child")
        except Exception as e:
            print(e)
            return -1

        return self.ID

    def addcurrentTable(self):
        try:
            self.dateTime = self.currentTable.formatDateTime(dt.datetime.now())
            self.ID = self.currentTable.add(self.dateTime, self.pid, self.cid, self.msg, self.videoMsg, self.url)
        except Exception as e:
            print(e)
            return -1

        return self.ID

    def getID(self):
        return self.currentTable.getID( (self.dateTime, self.pid) )

    def asList(self):
        self.fields = [self.ID, self.dateTime, self.msg, self.videoMsg, self.pid, self.url, self.cid]
        return self.fields

    def asTuple(self):
        return tuple(self.fields)

    def getFieldByID(self):
        return self.currentTable.getFieldsByID(self.ID)

    def getAll(self):
        return self.currentTable.getAll()
        
    #### TESTS ####

    def testAdd(self):
        assert self.ID == self.getID()

        expected = self.asTuple()
        actual = self.getFieldByID()

        assert expected == actual
        assert len(self.getAll()) == 1
        
    def testSet_Msg(self):
        self.currentTable.setMsg(self.ID, "New")
        assert self.currentTable.getMsg(self.ID) == "New"
    
    def testSet_VideoMsg(self):
        self.currentTable.setVideoMsg(self.ID, b'New')
        assert self.currentTable.getVideoMsg(self.ID) == b'New'

    def testSet_URL(self):
        self.currentTable.setMeetingURL(self.ID, "New")
        assert self.currentTable.getMeetingURL(self.ID) == 'New'

    def testGet_dateTime(self):
        assert self.currentTable.getDateTime(self.ID) == self.dateTime

    def testGet_Msg(self):
        assert self.currentTable.getMsg(self.ID)  == self.msg
    
    def testGet_VideoMsg(self):
        assert self.currentTable.getVideoMsg(self.ID)  == self.videoMsg

    def testGet_ChildID(self):
        assert self.currentTable.getChildID(self.ID)  == self.cid
        
    def testGet_ResponderID(self):
        assert self.currentTable.getResponderID(self.ID)  == self.pid

    def testGet_URL(self):
        assert self.currentTable.getMeetingURL(self.ID)  == self.url

    def testGetByChild(self):
        assert len(self.currentTable.getByChild(self.cid)) == 1

    def testGetByResponder(self):
        assert len(self.currentTable.getByResponder(self.pid)) == 1

    def testGet(self):
        assert len(self.currentTable.get(self.dateTime, self.pid)) == 7

    def testRemoveByChild(self):
        self.currentTable.removeByChild(self.cid)
        assert self.currentTable.getAll() == []

    def testRemoveByResponder(self):
        self.currentTable.removeByResponder(self.pid)
        assert self.currentTable.getAll() == []


