import pytest
# import os, sys
# sys.path.insert(0, os.path.abspath("database"))

from dbConnect import dbConnect
from dbNavElemType import NavElemType

import pdb

class TestDbNavType:
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

    typeName = "Button"

    pid = -1
    cid = -1
    clid = -1
    ID = -1
    fields = []

    #### SETUP ####
    def setup_method(self):
        self.db = dbConnect()
        self.db.useDB()
        self.currentTable = NavElemType(self.db.cnx())
        self.addcurrentTable()
        self.asList()

    #### TEARDOWN ####
    def teardown_method(self):
        self.currentTable.removeAll()
        self.db.close()

    #### HELPERS ####
 
    def addcurrentTable(self):
        try:
            self.ID = self.currentTable.add(self.typeName)
        except:
            return -1

        return self.ID

    def getID(self):
        return self.currentTable.getID( (self.typeName, ) )

    def asList(self):
        self.fields = [self.ID, self.typeName]
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
    
    def testSet_TypeName(self):
        self.currentTable.setTypeName(self.ID, "New")
        assert self.currentTable.getTypeName(self.ID) == "New"

    def testGet_TypeName(self):
        assert self.currentTable.getTypeName(self.ID) == self.typeName

    def testGet(self):
        assert len(self.currentTable.get(self.typeName)) == 2


    


