import pytest
# import os, sys
# sys.path.insert(0, os.path.abspath("database"))

from dbConnect import dbConnect
from dbParent import Parent
from dbChild import Child
from dbInputData import InputData

import datetime as dt
import pdb

class TestDBInputData:
    db = dbConnect()
    db.createTestDB()
    
    username = "testParent"
    password = "testPW"
    email = "testEmail"
    firstName = "testFName"
    lastName = "testLName"

    name = "testChild"
    age = 100
    raised_hand = 0
    skill_level = 1

    className = "Math"
    teacherName = "Sue Bird"

    dateTime = None
    mouseX = 50
    mouseY = 40
    keyboard = "Text"

    pid = -1
    cid = -1
    clid = -1
    ID = -1
    fields = []

    #### SETUP ####
    def setup_method(self):
        self.db = dbConnect()
        self.db.useDB()
        self.child = Child(self.db.cnx())
        self.parent = Parent(self.db.cnx())
        self.currentTable = InputData(self.db.cnx())
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
            self.ID = self.currentTable.add(self.dateTime, self.cid, self.mouseX, self.mouseY, self.keyboard)
        except:
            return -1

        return self.ID

    def getID(self):
        return self.currentTable.getID( (self.dateTime, self.cid) )

    def asList(self):
        self.fields = [self.ID, self.dateTime, self.cid, self.mouseX, self.mouseY, self.keyboard]
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

    def testGet_DateTime(self):
        assert self.currentTable.getDateTime(self.ID) == self.dateTime

    def testGet_ChildID(self):
        assert self.currentTable.getChildID(self.ID) == self.cid

    def testGetMouseX(self):
       assert self.currentTable.getMouseX(self.ID) == self.mouseX
        
    def testGetMouseY(self):
       assert self.currentTable.getMouseY(self.ID) == self.mouseY

    def testGetKeyboard(self):
       assert self.currentTable.getKeyboard(self.ID) == self.keyboard


    def testGetByChild(self):
        assert len(self.currentTable.getByChild(self.cid)) == 1

    def testGet(self):
        assert len(self.currentTable.get(self.dateTime, self.cid)) == 6

    def testRemoveByChild(self):
        self.currentTable.removeByChild(self.cid)
        assert self.currentTable.getAll() == []
        



