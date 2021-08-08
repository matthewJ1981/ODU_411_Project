import pytest
# import os, sys
# sys.path.insert(0, os.path.abspath("database"))

from dbConnect import dbConnect
from dbUser import User
from dbErrorCode import ErrorCode
from dbLogEntry import LogEntry

import datetime as dt
import pdb

class TestDbLogEntry:
    db = dbConnect()
    db.createTestDB()
    
    uType = "Parent"
    code = 0
    msg = "Help"

    dateTime = None
    navState = False
    screenshot = b'0'
    nsid = None

    uid = -1
    tid = -1
    ecid = -1
    ID = -1
    fields = []

    #### SETUP ####
    def setup_method(self):
        self.db = dbConnect()
        self.db.useDB()
        self.errorCode = ErrorCode(self.db.cnx())
        self.currentTable = LogEntry(self.db.cnx())
        self.user = User(self.db.cnx())
        self.addErrorCode()
        self.addUser()
        self.addcurrentTable()
        self.asList()

    #### TEARDOWN ####
    def teardown_method(self):
        self.currentTable.removeAll()
        self.user.removeAll()
        self.errorCode.removeAll()
        self.db.close()

    #### HELPERS ####
    
    def addUser(self):
        try:
            self.uid = self.user.add(self.uType, self.uid)
        except Exception as e:
            print(e)
            return -1

        return self.uid

    def addErrorCode(self):
        try:
            self.ecid = self.errorCode.add(self.code, self.msg)
        except Exception as e:
            print(e)
            return -1

        return self.ecid

    def addcurrentTable(self):
        try:
            self.dateTime = self.currentTable.formatDateTime(dt.datetime.now())
            self.ID = self.currentTable.add(self.uid, self.dateTime, self.navState, self.screenshot, self.code, self.nsid)
        except Exception as e:
            print(e)
            return -1

        return self.ID

    def getID(self):
        return self.currentTable.getID( (self.uid, self.dateTime) )

    def asList(self):
        self.fields = [self.ID, self.uid, self.dateTime, self.navState, self.screenshot, self.code, self.nsid]
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

    def testGet_userID(self):
        assert self.currentTable.getUserID(self.ID) == self.uid

    def testGet_datetime(self):
        assert self.currentTable.getDateTime(self.ID)  == self.dateTime
    
    def testGet_screenshot(self):
        assert self.currentTable.getScreenshot(self.ID)  == self.screenshot

    def testGet_errorCode(self):
        assert self.currentTable.getErrorCode(self.ID)  == self.code
        
    def testGet_navStepID(self):
        assert self.currentTable.getNavStepID(self.ID)  == self.nsid
        
    def testGet_navState(self):
        assert self.currentTable.getNavState(self.ID)  == self.navState

    def testGet(self):
        assert len(self.currentTable.get(self.uid, self.dateTime)) == 7

    def testGetByUser(self):
        assert len(self.currentTable.getByUser(self.uid)) == 1

    def testGetByErrorCode(self):
        assert len(self.currentTable.getByErrorCode(self.code)) == 1

    def testGetByNavStep(self):
        assert len(self.currentTable.getByNavStep(self.nsid)) == 0

    def testRemoveByUser(self):
        self.currentTable.removeByUser(self.uid)
        assert self.currentTable.getAll() == []

    def testRemoveByErrorCode(self):
        self.currentTable.removeByErrorCode(self.code)
        assert self.currentTable.getAll() == []

    def testRemoveByNavStepID(self):
        self.currentTable.removeByNavStepID(self.nsid)
        assert len(self.currentTable.getAll()) == 1

