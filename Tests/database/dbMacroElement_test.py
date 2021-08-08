import pytest
# import os, sys
# sys.path.insert(0, os.path.abspath("database"))

from dbConnect import dbConnect
from dbClass import Class
from dbActivity import Activity
from dbMacroElement import MacroElement
import datetime as dt

import pdb

class TestDBMacroElement:
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


    aid = -1
    activityName = "Writing"

    orderNum = 1
    macroName = "Name"
    url = "www.google.com"
    hasInput = True
    _input = "Input"
    imgPath = "C:\\images"
    img = b'0'
    x = 10
    y = 15

    #### SETUP ####
    def setup_method(self):
        self.db = dbConnect()
        self.db.useDB()
        self._class = Class(self.db.cnx())
        self.activity = Activity(self.db.cnx())
        self.currentTable = MacroElement(self.db.cnx())
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
            self.ID = self.currentTable.add(self.orderNum, self.aid, self.macroName, self.url, self.hasInput, self._input,
                                            self.imgPath, self.img, self.x, self.y)
        except Exception as e:
            print(e)
            return -1

        return self.ID

    def getID(self):
        return self.currentTable.getID( (self.orderNum, self.aid) )

    def asList(self):
        self.fields = [self.ID, self.orderNum, self.aid, self.macroName, self.url, self.hasInput, self._input,
                                            self.imgPath, self.img, self.x, self.y]
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
        
    def testSet_MacroName(self):
        self.currentTable.setMacroName(self.ID, "New")
        assert self.currentTable.getMacroName(self.ID) == "New"
    
    def testSet_URL(self):
        self.currentTable.setURL(self.ID, "www.new.com")
        assert self.currentTable.getURL(self.ID) == "www.new.com"

    def testSet_HasInput(self):
        self.currentTable.setHasInput(self.ID, 0)
        assert self.currentTable.getHasInput(self.ID) == 0

    def testSet_Input(self):
        self.currentTable.setInput(self.ID, "New")
        assert self.currentTable.getInput(self.ID) == "New"

    def testSet_ImagePath(self):
        self.currentTable.setImagePath(self.ID, "C:\\New")
        assert self.currentTable.getImagePath(self.ID) == "C:\\New"

    def testSet_Img(self):
        self.currentTable.setImage(self.ID, b'100')
        assert self.currentTable.getImage(self.ID) == b'100'

    def testSet_X(self):
        self.currentTable.setX(self.ID, 100)
        assert self.currentTable.getX(self.ID) == 100

    def testSet_Y(self):
        self.currentTable.setY(self.ID, 100)
        assert self.currentTable.getY(self.ID) == 100

    def testGet_OrderNum(self):
        assert self.currentTable.getOrderNum(self.ID) == self.orderNum

    def testGet_ActivityID(self):
        assert self.currentTable.getActivityID(self.ID)  == self.aid
    
    def testGet_MacroName(self):
        assert self.currentTable.getMacroName(self.ID)  == self.macroName

    def testGet_URL(self):
        assert self.currentTable.getURL(self.ID)  == self.url
        
    def testGet_Img(self):
        assert self.currentTable.getImage(self.ID)  == self.img

    def testGet_ImagePath(self):
        assert self.currentTable.getImagePath(self.ID)  == self.imgPath

    def testGet_HasInput(self):
        assert self.currentTable.getHasInput(self.ID)  == self.hasInput

    def testGet_Input(self):
        assert self.currentTable.getInput(self.ID)  == self._input

    def testGet_X(self):
        assert self.currentTable.getX(self.ID)  == self.x

    def testGetYg(self):
        assert self.currentTable.getY(self.ID)  == self.y


    def testGetByActivity(self):
        assert len(self.currentTable.getByActivity(self.aid)) == 1

    def testGet(self):
        assert len(self.currentTable.get(self.orderNum, self.aid)) == 11

    def testRemoveByActivity(self):
        self.currentTable.removeByActivity(self.aid)
        assert self.currentTable.getAll() == []


