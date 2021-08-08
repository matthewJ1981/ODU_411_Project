import pytest
from datetime import datetime
# import os, sys
# sys.path.insert(0, os.path.abspath("database"))

from dbConnect import dbConnect
from dbTable import Table

class TestDbParent:
    db = dbConnect()
    db.createTestDB()

    tableName = "test"
    unmutables = ("id", "username")
    primaryKey = ("username",)
    foreignKey = []

    username = "testParent"
    password = "testPW"
    email = "testEmail"
    firstName = "testFName"
    lastName = "testLName"

    query = "INSERT INTO test(username, password, email_addr, first_name, last_name) VALUES(%s, %s, %s, %s, %s)"
    values = (username, password, email, firstName, lastName)

    ID = -1

    fields = []
    #### SETUP ####
    def setup_method(self):
        self.db = dbConnect()
        self.db.useDB()
        self.table = Table(self.db.cnx(), self.tableName, self.unmutables, self.primaryKey, self.foreignKey)
        #self.asList()

    #### TEARDOWN ####
    def teardown_method(self):
        self.table.removeAll()
        self.db.close()
       
    #### TESTS ####

    def testAdd(self):
        self.table.add(self.query, ("p1", "pw1", "email1", "fn1", "ln1"))
        id = self.table.getID(("p1",))

        assert (id, "p1", "pw1", "email1", "fn1", "ln1", ) == self.table.getFieldsByID(id)

    def testAddSame(self):
        self.table.add(self.query, ("p1", "pw1", "email1", "fn1", "ln1")) 
        id = self.table.getID(("p1",))
        try:
            self.table.add(self.query, ("p1", "pw2", "email2", "fn2", "ln2"))   
        except:
            assert True
        
        assert len(self.table.getAll()) == 1
        assert (id, "p1", "pw1", "email1", "fn1", "ln1") == self.table.getFieldsByID(id)

    def testRemove(self):
        self.table.add(self.query, ("p1", "pw1", "email1", "fn1", "ln1")) 
        id = self.table.getID(("p1",))
        self.table.remove(id)

        assert () == self.table.getFieldsByID(id)

    def testRemoveAll(self):
        self.table.add(self.query, ("p1", "pw1", "email1", "fn1", "ln1")) 
        id = self.table.getID(("p1",))

        self.table.removeAll()
        assert () == self.table.getFieldsByID(id)

    def testRemoveAllWhere(self):
        self.table.add(self.query, ("p1", "pw1", "email1", "fn1", "ln1")) 
        id = self.table.getID(("p1",))

        self.table.removeAll(("password",), ("pw1",))
        assert () == self.table.getFieldsByID(id)

    def testRemoveAllWhere2(self):
        self.table.add(self.query, ("p1", "pw1", "email1", "fn1", "ln1")) 
        id = self.table.getID(("p1",))

        self.table.removeAll(("password",), ("pw2",))
        assert (id, "p1", "pw1", "email1", "fn1", "ln1") == self.table.getFieldsByID(id)

    def testSetFieldByID(self):
        self.table.add(self.query, ("p1", "pw1", "email1", "fn1", "ln1")) 
        id = self.table.getID(("p1",))

        self.table.setFieldByID(id, "first_name", "New")
        assert (id, "p1", "pw1", "email1", "New", "ln1") == self.table.getFieldsByID(id)

    def testSetFieldsByID(self):
        self.table.add(self.query, ("p1", "pw1", "email1", "fn1", "ln1")) 
        id = self.table.getID(("p1",))

        self.table.setFieldsByID(id, ("first_name", "last_name"), ("New", "Name"))
        assert (id, "p1", "pw1", "email1", "New", "Name") == self.table.getFieldsByID(id)

    def testSetField(self):
        self.table.add(self.query, ("p1", "pw1", "email1", "fn1", "ln1")) 
        id1 = self.table.getID(("p1",))

        self.table.add(self.query, ("p2", "pw2", "email2", "fn2", "ln2")) 
        id2 = self.table.getID(("p2",))

        self.table.setField("first_name", "New")
        assert (id1, "p1", "pw1", "email1", "New", "ln1") == self.table.getFieldsByID(id1)
        assert (id2, "p2", "pw2", "email2", "New", "ln2") == self.table.getFieldsByID(id2)

    def testSetFields(self):
        self.table.add(self.query, ("p1", "pw1", "email1", "fn1", "ln1")) 
        id1 = self.table.getID(("p1",))

        self.table.add(self.query, ("p2", "pw2", "email2", "fn2", "ln2")) 
        id2 = self.table.getID(("p2",))

        self.table.setFields(("first_name", "last_name"), ("New", "Name"))
        assert (id1, "p1", "pw1", "email1", "New", "Name") == self.table.getFieldsByID(id1)
        assert (id2, "p2", "pw2", "email2", "New", "Name") == self.table.getFieldsByID(id2)

    def testGetID(self):
        assert self.table.getID(("p2",)) == None

    def testGetFieldByID(self):
        self.table.add(self.query, ("p1", "pw1", "email1", "fn1", "ln1")) 
        id1 = self.table.getID(("p1",))

        assert self.table.getFieldByID(id1, "password") == "pw1"
        assert (id1, "p1", "pw1", "email1", "fn1", "ln1") == self.table.getFieldsByID(id1)

    def testGetFieldsByID(self):
        self.table.add(self.query, ("p1", "pw1", "email1", "fn1", "ln1")) 
        id1 = self.table.getID(("p1",))

        assert self.table.getFieldsByID(id1, ("password", "first_name")) == ("pw1", "fn1")
        assert (id1, "p1", "pw1", "email1", "fn1", "ln1") == self.table.getFieldsByID(id1)

    def testGetField(self):
        self.table.add(self.query, ("p1", "pw1", "email1", "fn1", "ln1")) 
        id1 = self.table.getID(("p1",))

        self.table.add(self.query, ("p2", "pw2", "email2", "fn2", "ln2")) 
        id2 = self.table.getID(("p2",))

        assert self.table.getField("password") == ("pw1", "pw2")
        assert (id1, "p1", "pw1", "email1", "fn1", "ln1") == self.table.getFieldsByID(id1)
        assert (id2, "p2", "pw2", "email2", "fn2", "ln2") == self.table.getFieldsByID(id2)

    def testGetFields(self):
        self.table.add(self.query, ("p1", "pw1", "email1", "fn1", "ln1")) 
        id1 = self.table.getID(("p1",))

        self.table.add(self.query, ("p2", "pw2", "email2", "fn2", "ln2")) 
        id2 = self.table.getID(("p2",))

        assert self.table.getFields(("password", "first_name")) == [("pw1", "fn1"), ("pw2","fn2")]
        assert (id1, "p1", "pw1", "email1", "fn1", "ln1") == self.table.getFieldsByID(id1)
        assert (id2, "p2", "pw2", "email2", "fn2", "ln2") == self.table.getFieldsByID(id2)
        
    def testGetAll(self):
        self.table.add(self.query, ("p1", "pw1", "email1", "fn1", "ln1")) 
        id1 = self.table.getID(("p1",))

        self.table.add(self.query, ("p2", "pw2", "email2", "fn2", "ln2")) 
        id2 = self.table.getID(("p2",))

        assert self.table.getAll() == [(id1, "p1", "pw1", "email1", "fn1", "ln1"), (id2, "p2", "pw2", "email2", "fn2", "ln2")]

    def testGetFirst(self):
        assert self.table.getFirst((1,), True) == 1

    def testSelectClause(self):
        assert self.table.selectClause(("first_name", "last_name")) == "SELECT first_name, last_name"
    def testSetClause(self):
        assert self.table.setClause(("first_name", "last_name")) == "SET first_name = %s, last_name = %s"
    def testWhereClause(self):
        assert self.table.whereClause(("first_name", "last_name")) == "WHERE first_name = %s AND last_name = %s"
    def testClause(self):
        assert self.table.clause(("first_name", "last_name"), "TEST ", " + ") == "TEST first_name = %s + last_name = %s"
    def testFormatDateTime(self):
        dt = datetime(1900, 3, 4, 11, 50, 4)
        assert dt.strftime("%m/%d/%y %H:%M:%S") == self.table.formatDateTime(dt)
    def testGetByID(self):
        self.table.add(self.query, ("p1", "pw1", "email1", "fn1", "ln1")) 
        id1 = self.table.getID(("p1",))
        assert (id1, "p1", "pw1", "email1", "fn1", "ln1") == self.table.getByID(id1)


