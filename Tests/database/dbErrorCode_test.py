import pytest
# import os, sys
# sys.path.insert(0, os.path.abspath("database"))

from dbConnect import dbConnect
from dbErrorCode import ErrorCode

class TestDbErrorCode:
    db = dbConnect()
    db.createTestDB()
    
    code = 0
    msg = "Navigation Error"

    ID = -1
    fields = []

    #### SETUP ####
    def setup_method(self):
        self.db = dbConnect()
        self.db.useDB()
        self.currentTable = ErrorCode(self.db.cnx())
        self.addcurrentTable()
        self.asList()

    #### TEARDOWN ####
    def teardown_method(self):
        self.currentTable.removeAll()
        self.db.close()

    #### HELPERS ####

    def addcurrentTable(self):
        try:
            self.ID = self.currentTable.add(self.code, self.msg)
        except Exception as e:
            print(e)
            return -1

        return self.ID

    def getID(self):
        return self.currentTable.getID( (self.code,))

    def asList(self):
        self.fields = [self.ID, self.code, self.msg]
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

    def testGet_Code(self):
        assert self.currentTable.getCode(self.ID) == self.code

    def testGet_Msg(self):
        assert self.currentTable.getMsg(self.ID) == self.msg

    def testGet(self):
        assert len(self.currentTable.get(self.code)) == 3