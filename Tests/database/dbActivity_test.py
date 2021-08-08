import pytest
# import os, sys
# sys.path.insert(0, os.path.abspath("database"))

from dbConnect import dbConnect
from dbParent import Parent
from dbChild import Child
from dbClass import Class
# from dbUser import User
# from dbUserType import UserType
from dbActivity import Activity

import pdb

class TestDbActivity:
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

    activityName = "Spelling"

    className = "Math"
    teacherName = "Sue Bird"

    pid = -1
    cid = -1
    clid = -1
    ID = -1
    fields = []

    #### SETUP ####
    def setup_method(self):
        self.db = dbConnect()
        self.db.useDB()
        # self.user = User(self.db.cnx())
        self.child = Child(self.db.cnx())
        self.parent = Parent(self.db.cnx())
        self._class = Class(self.db.cnx())
        self.currentTable = Activity(self.db.cnx())
        self.addParent()
        self.addChild()
        self.addClass()
        self.addcurrentTable()
        self.asList()

    #### TEARDOWN ####
    def teardown_method(self):
        self.currentTable.removeAll()
        self.child.removeAll()
        self.parent.removeAll()
        self._class.removeAll()
        self.db.close()

    #### HELPERS ####
    def addParent(self):
        try:
            self.pid = self.parent.add(self.username, self.password, self.email, self.firstName, self.lastName)
        except:
            return -1
            
        return self.pid

    # def addUserType(self):
    #     try:
    #         self.ID = self.userType.add("Parent")
    #         self.ID = self.userType.add("Child")
    #     except Exception as e:
    #         print(e)
    #         return -1

    #     return self.ID

    def addChild(self):
        try:
            self.cid = self.child.add(self.name, self.age, self.pid)
        except:
            return -1

        return self.cid
    
    def addClass(self):
        try:
            self.clid = self._class.add(self.className, self.teacherName)
        except:
            return -1

        return self.clid

    def addcurrentTable(self):
        try:
            self.ID = self.currentTable.add(self.activityName, self.clid)
        except:
            return -1

        return self.ID

    def getID(self):
        return self.currentTable.getID( (self.activityName, self.clid) )

    def asList(self):
        self.fields = [self.ID, self.activityName, self.clid]
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

    def testSet_Name(self):
        self.currentTable.setName(self.ID, "New")
        assert self.currentTable.getName(self.ID) == "New"

    def testGet_ClassID(self):
        assert self.currentTable.getClassID(self.ID) == self.clid

    def testGet_Name(self):
        assert self.currentTable.getName(self.ID) == self.activityName

    def testGetActivitiesByClass(self):
        assert len(self.currentTable.getByClass(self.clid)) == 1

    def testGet(self):
        assert len(self.currentTable.get(self.activityName, self.clid)) == 3

    def testRemoveByClass(self):
        self.currentTable.removeByClass(self.clid)
        assert self.currentTable.getAll() == []
    


