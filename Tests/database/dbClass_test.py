import pytest
# import os, sys
# sys.path.insert(0, os.path.abspath("database"))

from dbConnect import dbConnect
from dbParent import Parent
from dbChild import Child
from dbClass import Class

import pdb


class TestDbClass:
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

    pid = -1
    cid = -1
    clid = -1
    fields = []
    
    #### SETUP ####
    def setup_method(self):
        # self.pid = -1
        # self.cid = -1
        # self.clid = -1
        # self.fields = []
        self.db = dbConnect()
        self.db.useDB()
        self.child = Child(self.db.cnx())
        self.parent = Parent(self.db.cnx())
        self._class = Class(self.db.cnx())
        self.addParent()
        self.addChild()
        self.addClass()
        self.asList()

    #### TEARDOWN ####
    def teardown_method(self):
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

    def getID(self):
        return self._class.getID( (self.className, self.teacherName) )

    def asList(self):
        self.fields = [self.clid, self.className, self.teacherName]
        return self.fields
    def asTuple(self):
        return tuple(self.fields)

    def getFieldByID(self):
        return self._class.getFieldsByID(self.clid)

    def getAll(self):
        return self._class.getAll()
        
    #### TESTS ####

    def testAdd(self):
        print(self.clid)
        assert self.clid == self.getID()

        expected = self.asTuple()
        actual = self.getFieldByID()

        assert expected == actual
        assert len(self.getAll()) == 1
    
    def testSet_ClassName(self):
        self._class.setClassName(self.clid, "New")
        assert self._class.getClassName(self.clid) == "New"
        
    def testSet_TeacherName(self):
        self._class.setTeacherName(self.clid, "New")
        assert self._class.getTeacherName(self.clid) == "New"

    def testGet_ClassName(self):
        assert self._class.getClassName(self.clid) == self.className

    def testGet_TeacherName(self):
        assert self._class.getTeacherName(self.clid) == self.teacherName
    
    def testGet(self):
        assert len(self._class.get(self.className, self.teacherName)) == 3


    


