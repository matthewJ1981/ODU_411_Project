import pytest
# import os, sys
# sys.path.insert(0, os.path.abspath("database"))

from dbConnect import dbConnect
from dbParent import Parent
from dbBubble import Bubble
from dbMemberOf import MemberOf
from dbUserType import UserType

import pdb

class TestDnMemberOF:
    db = dbConnect()
    db.createTestDB()
    
    username = "testParent"
    password = "testPW"
    email = "testEmail"
    firstName = "testFName"
    lastName = "testLName"

    bubbleName = "Bubble"

    pid = -1
    bid = -1
    ID = -1
    fields = []

    #### SETUP ####
    def setup_method(self):
        self.db = dbConnect()
        self.db.useDB()
        self.parent = Parent(self.db.cnx())
        self.bubble = Bubble(self.db.cnx())
        self.currentTable = MemberOf(self.db.cnx())
        self.addParent()
        self.addBubble()
        self.addcurrentTable()
        self.asList()

    #### TEARDOWN ####
    def teardown_method(self):
        self.currentTable.removeAll()
        self.parent.removeAll()
        self.bubble.removeAll()
        self.db.close()

    #### HELPERS ####
    def addParent(self):
        try:
            self.pid = self.parent.add(self.username, self.password, self.email, self.firstName, self.lastName)
        except:
            return -1
            
        return self.pid
    
    def addBubble(self):
        try:
            self.bid = self.bubble.add(self.bubbleName)
        except:
            return -1

        return self.bid

    def addUserType(self):
        try:
            self.ID = self.userType.add("Parent")
            self.ID = self.userType.add("Child")
        except Exception as e:
            print(e)
            return -1
            
    def addcurrentTable(self):
        try:
            self.ID = self.currentTable.add(self.pid, self.bid)
        except:
            return -1

        return self.ID

    def getID(self):
        return self.currentTable.getID( (self.pid, self.bid) )

    def asList(self):
        self.fields = [self.ID, self.pid, self.bid]
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

    def testGet_ParentID(self):
        assert self.currentTable.getParentID(self.ID) == self.pid

    def testGet_BubbleID(self):
        assert self.currentTable.getBubbleID(self.ID) == self.bid
        
    def testGetParentsInBubble(self):
        assert len(self.currentTable.getByBubble(self.bid)) == 1

    def testGetBubblesForParent(self):
        assert len(self.currentTable.getByParent(self.pid)) == 1

    def testGet(self):
        assert len(self.currentTable.get(self.pid, self.bid)) == 3

    def testRemoveByParent(self):
        self.currentTable.removeByParent(self.pid)
        assert self.currentTable.getAll() == []

    def testRemoveByBubble(self):
        self.currentTable.removeByBubble(self.bid)
        assert self.currentTable.getAll() == []

    


