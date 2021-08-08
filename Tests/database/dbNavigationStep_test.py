import pytest
# import os, sys
# sys.path.insert(0, os.path.abspath("database"))

from dbConnect import dbConnect
from dbClass import Class
from dbActivity import Activity
from dbNavigationStep import NavigationStep
from dbNavElemType import NavElemType
import datetime as dt

import pdb

class TestDbNavStep:
    db = dbConnect()
    db.createTestDB()
    
    className = "Math"
    teacherName = "Sue Bird"

    duration = 30
    dateTime = None

    elemName = "www.google.com"
    elemType = "URL"
    index = 1
    img = b'0'

    typeName0 = "URL"
    typeName1 = "Button"

    clid = -1
    sid = -1
    eid = -1
    ID = -1
    fields = []

    activityName = "Writing"
    aid = -1

    #### SETUP ####
    def setup_method(self):
        self.db = dbConnect()
        self.db.useDB()
        self._class = Class(self.db.cnx())
        self.activity = Activity(self.db.cnx())
        self.navElemType = NavElemType(self.db.cnx())
        self.currentTable = NavigationStep(self.db.cnx())
        self.addClass()
        self.addActivity()
        self.addNavElemType()
        self.addcurrentTable()
        self.asList()

    #### TEARDOWN ####
    def teardown_method(self):
        self.currentTable.removeAll()
        self.navElemType.removeAll()
        self.activity.removeAll()
        self._class.removeAll()
        self.db.close()

    #### HELPERS ####
    
    def addClass(self):
        try:
            self.clid = self._class.add(self.className, self.teacherName)
        except:
            return -1

        return self.clid

    def addActivity(self):
        try:
            self.aid = self.activity.add(self.activityName, self.clid)
        except:
            return -1

        return self.aid

    def addNavElemType(self):
        try:
            self.netid = self.navElemType.add(self.typeName0)
        except:
            return -1

        return self.netid

    def addcurrentTable(self):
        try:
            self.ID = self.currentTable.add(self.elemName, self.elemType, self.index, self.aid, self.img)
        except Exception as e:
            print(e)
            return -1

        return self.ID

    def getID(self):
        return self.currentTable.getID( (self.elemName, self.elemType, self.aid) )

    def asList(self):
        self.fields = [self.ID, self.elemName, self.elemType, self.index, self.aid, self.img]
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
        
    def testSet_ElemName(self):
        self.currentTable.setElemName(self.ID, "New")
        assert self.currentTable.getElemName(self.ID) == "New"
    
    def testSet_ElemType(self):
        self.navElemType.add(self.typeName1)
        self.currentTable.setElemType(self.ID, self.typeName1)
        assert self.currentTable.getElemType(self.ID) == self.typeName1

    def testSet_Index(self):
        self.currentTable.setIndex(self.ID, 100)
        assert self.currentTable.getIndex(self.ID) == 100

    def testSet_Img(self):
        self.currentTable.setImage(self.ID, b'100')
        assert self.currentTable.getImage(self.ID) == b'100'

    def testGet_ElemName(self):
        assert self.currentTable.getElemName(self.ID) == self.elemName

    def testGet_ElemType(self):
        assert self.currentTable.getElemType(self.ID)  == self.typeName0
    
    def testGet_Index(self):
        assert self.currentTable.getIndex(self.ID)  == self.index

    def testGet_ActivityID(self):
        assert self.currentTable.getActivityID(self.ID)  == self.aid
        
    def testGet_Img(self):
        assert self.currentTable.getImage(self.ID)  == self.img

    def testGetStepByActivityID(self):
        assert len(self.currentTable.getByActivity(self.aid)) == 1

    def testGet(self):
        assert len(self.currentTable.get(self.elemName, self.elemType, self.aid)) == 6

    def testRemoveByActivity(self):
        self.currentTable.removeByActivity(self.aid)
        assert self.currentTable.getAll() == []


