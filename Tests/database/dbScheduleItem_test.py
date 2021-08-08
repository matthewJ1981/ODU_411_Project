import pytest
# import os, sys
# sys.path.insert(0, os.path.abspath("database"))

from dbConnect import dbConnect
from dbClass import Class
from dbActivity import Activity
from dbScheduleItem import ScheduleItem
import datetime as dt

import pdb

class TestDbSchedItem:
    db = dbConnect()
    db.createTestDB()
    
    className = "Math"
    teacherName = "Sue Bird"

    dateTime = None
    duration = 60
    clid = -1
    ID = -1
    fields = []

    aid = -1
    activityName = "Writing"

    #### SETUP ####
    def setup_method(self):
        self.db = dbConnect()
        self.db.useDB()
        self._class = Class(self.db.cnx())
        self.activity = Activity(self.db.cnx())
        self.currentTable = ScheduleItem(self.db.cnx())
        self.addClass()
        self.addActivity()
        self.addcurrentTable()
        self.asList()

    #### TEARDOWN ####
    def teardown_method(self):
        self.currentTable.removeAll()
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

    def addcurrentTable(self):
        try:
            self.dateTime = self.currentTable.formatDateTime(dt.datetime.now())
            self.ID = self.currentTable.add(self.dateTime, self.duration, self.aid)
        except:
            return -1

        return self.ID

    def getID(self):
        return self.currentTable.getID( (self.dateTime, self.aid) )

    def asList(self):
        self.fields = [self.ID, self.dateTime, self.duration, self.aid]
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
        
    def testSet_DateTime(self):
        newValue = self.currentTable.formatDateTime(dt.datetime.now())
        self.currentTable.setDateTime(self.ID, newValue)
        assert self.currentTable.getDateTime(self.ID) == newValue

    def testGet_ActivityID(self):
        assert self.currentTable.getActivityID(self.ID) == self.aid

    def testGet_DateTime(self):
        assert self.currentTable.getDateTime(self.ID) == self.dateTime

    def testGet_Duration(self):
        assert self.currentTable.getDuration(self.ID) == self.duration

    def testSet_Duration(self):
        self.currentTable.setDuration(self.ID, 120)
        assert self.currentTable.getDuration(self.ID) == 120

    def getItemByActivity(self):
        assert len(self.currentTable.getByActivity(self.aid)) == 1

    def testGet(self):
        assert len(self.currentTable.get(self.dateTime, self.aid)) == 4

    def testRemoveByActivity(self):
        self.currentTable.removeByActivity(self.aid)
        assert self.currentTable.getAll() == []

    


