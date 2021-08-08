import pytest
# import os, sys
# sys.path.insert(0, os.path.abspath("database"))

from dbConnect import dbConnect
from dbBubble import Bubble

import pdb

class TestDbBubble:
    db = dbConnect()
    db.createTestDB()
    
    bubbleName = "Bubble"

    pid = -1
    bid = -1

    fields = []

    #### SETUP ####
    def setup_method(self):
        self.db = dbConnect()
        self.db.useDB()
        self.bubble = Bubble(self.db.cnx())
        self.addBubble()
        self.asList()

    #### TEARDOWN ####
    def teardown_method(self):
        self.bubble.removeAll()
        self.db.close()

    #### WRAPPERS ####

    def addBubble(self):
        try:
            self.bid = self.bubble.add(self.bubbleName)
        except:
            return -1

        return self.bid
    
    def getID(self):
        return self.bubble.getID( (self.bubbleName,) )

    def asList(self):
        self.fields = [self.bid, self.bubbleName]
        return self.fields

    def asTuple(self):
        return tuple(self.fields)

    def getFieldByID(self):
        return self.bubble.getFieldsByID(self.bid)

    def getAll(self):
        return self.bubble.getAll()
        
    #### TESTS ####

    def testAdd(self):
        assert self.bid == self.getID()

        expected = self.asTuple()
        actual = self.getFieldByID()

        assert expected == actual
        assert len(self.getAll()) == 1

    def testSet_Name(self):
        self.bubble.setName(self.bid, "New")
        assert self.bubble.getName(self.bid) == "New"

    def testGet_Name(self):
        assert self.bubble.getName(self.bid) == self.bubbleName

    def testGet(self):
        assert len(self.bubble.get(self.bubbleName)) == 2 



    


