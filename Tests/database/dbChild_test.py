import pytest
# import os, sys
# sys.path.insert(0, os.path.abspath("database"))

from dbConnect import dbConnect
from dbParent import Parent
from dbChild import Child
from dbUserType import UserType
from dbUser import User

import pdb

class TestDbChild:
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

    pid = -1
    cid = -1
    fields = []

    #### SETUP ####
    def setup_method(self):
        self.db = dbConnect()
        self.db.useDB()
        self.child = Child(self.db.cnx())
        self.parent = Parent(self.db.cnx())
        self.user = User(self.db.cnx())
        self.addParent()
        self.addChild()
        self.asList()

    #### TEARDOWN ####
    def teardown_method(self):
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

    def getID(self):
        return self.child.getID( (self.name, self.age, self.pid) )

    def asList(self):
        self.fields = [self.cid, self.name, self.age, self.raised_hand, self.skill_level, self.pid, self.child.getUserID(self.cid)]
        return self.fields
    def asTuple(self):
        return tuple(self.fields)

    def getFieldByID(self):
        return self.child.getFieldsByID(self.cid)

    def getAll(self):
        return self.child.getAll()
        
    #### TESTS ####

    def testAdd(self):
        assert self.cid == self.getID()

        expected = self.asTuple()
        actual = self.getFieldByID()

        assert expected == actual
        assert len(self.getAll()) == 1

    def testAdd_NoParent(self):
        self.child.remove(self.cid)
        self.parent.remove(self.pid)
        cid = self.addChild()

        assert cid == -1
    
    def testSet_Name(self):
        self.child.setName(self.cid, "New")
        assert self.child.getName(self.cid) == "New"
        
    def testSet_Age(self):
        self.child.setAge(self.cid, 100)
        assert self.child.getAge(self.cid) == 100

    def testSet_Raised_Hand(self):
        self.child.setRaisedHand(self.cid, 1)
        assert self.child.getRaisedHand(self.cid) == 1
    
    def testSet_Skill_Level(self):
        self.child.setSkillLevel(self.cid, 100)
        assert self.child.getSkillLevel(self.cid) == 100

    def testGet_FirstName(self):
        assert self.child.getName(self.cid) == self.name

    def testGet_Age(self):
        assert self.child.getAge(self.cid) == self.age

    def testGet_RaisedHand(self):
        assert self.child.getRaisedHand(self.cid) == self.raised_hand

    def testGet_SkillLevel(self):
        assert self.child.getSkillLevel(self.cid) == self.skill_level

    def testGet_ParentID(self):
        assert self.child.getParentID(self.cid) == self.pid

    def testGetByParent(self):
        assert len(self.child.getByParent(self.pid)) == 1

    def testGetUserID(self):
        assert self.child.getUserID(self.cid) > 0

    def testGetByUserID(self):
        return len(self.child.getByUserID(self.child.getUserID(self.cid))) == 1

    def testRemoveByUserID(self):
        self.child.removeByUserID(self.child.getUserID(self.cid))
        assert self.child.getAll() == []

    def testGet(self):
        assert len(self.child.get(self.name, self.age, self.pid)) == 7

    def testRemoveByParent(self):
        self.child.removeByParent(self.pid)
        assert self.child.getAll() == []
    
    def testRemove(self):
        self.child.remove(self.cid)
        assert self.child.getAll() == []
        assert len(self.user.getAll()) == 1
    def testRemoveAll(self):
        self.child.removeAll()
        assert self.child.getAll() == []
        assert len(self.user.getAll()) == 1