import pytest
# import os, sys
# sys.path.insert(0, os.path.abspath("database"))

from dbConnect import dbConnect
from dbUserType import UserType

class TestDbUserType:
    db = dbConnect()
    db.createTestDB()
    
    userType = "Test"

    ID = -1
    tid = -1
    fields = []

    #### SETUP ####
    def setup_method(self):
        self.db = dbConnect()
        self.db.useDB()
        self.currentTable = UserType(self.db.cnx())
        #self.currentTable.removeAll()
        self.addcurrentTable()
        self.asList()

    #### TEARDOWN ####
    def teardown_method(self):
        self.currentTable.remove(self.ID)
        self.db.close()

    #### HELPERS ####

    def addcurrentTable(self):
        try:
            self.ID = self.currentTable.add(self.userType)
        except Exception as e:
            print(e)
            return -1

        return self.ID

    def getID(self):
        return self.currentTable.getID( (self.userType,))

    def asList(self):
        self.fields = [self.ID, self.userType]
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
        assert len(self.getAll()) == 3
        
    def testSet_Type(self):
        self.currentTable.setType(self.ID, "New")
        assert self.currentTable.getType(self.ID) == "New"

    def testGet_Type(self):
        assert self.currentTable.getType(self.ID) == self.userType

    def testGet(self):
        assert len(self.currentTable.get(self.userType)) == 2