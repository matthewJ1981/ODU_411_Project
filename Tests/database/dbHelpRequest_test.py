import pytest
# import os, sys
# sys.path.insert(0, os.path.abspath("database"))

from dbConnect import dbConnect
from dbParent import Parent
from dbChild import Child
from dbHelpRequest import HelpRequest
import datetime as dt

class TestDbHelpRequest:
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
    cid = -1
    fields = []

    #### SETUP ####
    def setup_method(self):
        self.db = dbConnect()
        self.db.useDB()
        self.parent = Parent(self.db.cnx())
        self.child = Child(self.db.cnx())
        self.currentTable = HelpRequest(self.db.cnx())
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

    def addcurrentTable(self):
        try:
            self.dateTime = self.currentTable.formatDateTime(dt.datetime.now())
            self.ID = self.currentTable.add(self.dateTime, self.cid, self.msg, self.videoMsg)
        except Exception as e:
            print(e)
            return -1

        return self.ID

    def getID(self):
        return self.currentTable.getID( (self.dateTime, self.cid) )

    def asList(self):
        self.fields = [self.ID, self.dateTime, self.msg, self.videoMsg, self.cid]
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



    def testGet_dateTime(self):
        assert self.currentTable.getDateTime(self.ID) == self.dateTime

    def testGet_Msg(self):
        assert self.currentTable.getMsg(self.ID)  == self.msg
    
    def testGet_VideoMsg(self):
        assert self.currentTable.getVideoMsg(self.ID)  == self.videoMsg

    def testGet_ChildID(self):
        assert self.currentTable.getChildID(self.ID)  == self.cid

    def testGetByChild(self):
        assert len(self.currentTable.getByChild(self.cid)) == 1

    def testGet(self):
        assert len(self.currentTable.get(self.dateTime, self.cid)) == 5

    def testRemoveByChild(self):
        self.currentTable.removeByChild(self.cid)
        assert self.currentTable.getAll() == []


