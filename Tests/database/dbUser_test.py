import pytest
# import os, sys
# sys.path.insert(0, os.path.abspath("database"))

from dbConnect import dbConnect
from dbUser import User

class TestDbUser:
    db = dbConnect()
    db.createTestDB()
    
    uType = "Parent"

    userID = 10
    ID = -1
    tid = -1
    fields = []

    #### SETUP ####
    def setup_method(self):
        self.db = dbConnect()
        self.db.useDB()
        self.currentTable = User(self.db.cnx())
        self.addcurrentTable()
        self.asList()

    #### TEARDOWN ####
    def teardown_method(self):
        self.currentTable.removeAll()
        self.db.close()

    #### HELPERS ####

    def addcurrentTable(self):
        try:
            self.ID = self.currentTable.add(self.uType, self.userID)
        except Exception as e:
            print(e)
            return -1

        return self.ID

    def getID(self):
        return self.currentTable.getID( (self.uType, self.userID))

    def asList(self):
        self.fields = [self.ID, self.uType, self.userID]
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
        
    def testGet_Type(self):
        assert self.currentTable.getType(self.ID) == self.uType

    def testGet_userID(self):
        assert self.currentTable.getUserID(self.ID) == self.userID

    def testGetByType(self):
        assert len(self.currentTable.getByType(self.uType)) == 1

    def testRemoveByType(self):
        self.currentTable.removeByType(self.uType)
        assert self.currentTable.getAll() == []

    def testGet(self):
        assert len(self.currentTable.get(self.uType, self.userID)) == 3