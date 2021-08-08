import pytest
# import os, sys
# sys.path.insert(0, os.path.abspath("database"))

from dbConnect import dbConnect
from dbParent import Parent
from dbUser import User

class TestDbParent:
    db = dbConnect()
    db.createTestDB()
    
    username = "testParent"
    password = "testPW"
    email = "testEmail"
    firstName = "testFName"
    lastName = "testLName"
    pid = -1

    fields = []
    #### SETUP ####
    def setup_method(self):
        self.db = dbConnect()
        self.db.useDB()
        self.parent = Parent(self.db.cnx())
        self.user = User(self.db.cnx())
        self.addParent()
        self.asList()

    #### TEARDOWN ####
    def teardown_method(self):
        self.parent.removeAll()
        self.db.close()

    #### HELPERS ####
    def addParent(self):
        try:
            self.pid = self.parent.add(self.username, self.password, self.email, self.firstName, self.lastName)
        except:
            return -1
        return self.pid

    def addUserType(self):
        try:
            self.ID = self.userType.add("Parent")
            self.ID = self.userType.add("Child")
        except Exception as e:
            print(e)
            return -1

        return self.ID

    def removeParent(self):
        self.parent.remove(self.pid)

    def getID(self):
        return self.parent.getID((self.username,))

    def asList(self):
        self.fields = [self.pid, self.username, self.password, self.email, self.firstName, self.lastName, self.parent.getUserID(self.pid)]
        return self.fields

    def asTuple(self):
        return tuple(self.fields)

    def getFields(self):
        return self.parent.getFieldsByID(self.pid)

    def getAll(self):
        return self.parent.getAll()
        
    #### TESTS ####

    def testAdd(self):
        assert self.pid == self.getID()
        assert self.parent.verifyPassword(self.username, self.password) == True

    def testSet_Password(self):
        self.parent.setPassword(self.pid, "New password")
        assert self.parent.verifyPassword(self.username, "New password") == True

    def testSet_Email(self):
        self.parent.setEmail(self.pid, "New")
        assert self.parent.getEmail(self.pid) == "New"

    def testSet_FirstName(self):
        self.parent.setFirstName(self.pid, "New")
        assert self.parent.getFirstName(self.pid) == "New"

    def testSet_LastName(self):
        self.parent.setLastName(self.pid, "New")
        assert self.parent.getLastName(self.pid) == "New"

    def testGet_UserName(self):
        assert self.parent.getUserName(self.pid) == self.username

    def testGet_Password(self):
        assert self.parent.verifyPassword(self.username, self.password) == True

    def testGet_Email(self):
        assert self.parent.getEmail(self.pid) == self.email

    def testGet_FirstName(self):
        assert self.parent.getFirstName(self.pid) == self.firstName

    def testGet_LastName(self):
        assert self.parent.getLastName(self.pid) == self.lastName

    def testGetUserID(self):
        assert self.parent.getUserID(self.pid) > 0

    def testGetByUserID(self):
        return len(self.parent.getByUserID(self.parent.getUserID(self.pid))) == 1

    def testRemoveByUserID(self):
        self.parent.removeByUserID(self.parent.getUserID(self.pid))
        assert self.parent.getAll() == []

    def testGet(self):
        assert len(self.parent.get(self.username)) == 7

    def testRemove(self):
        self.parent.remove(self.pid)
        assert self.parent.getAll() == []
        assert self.user.getAll() == []
    def testRemoveAll(self):
        self.parent.removeAll()
        assert self.parent.getAll() == []
        assert self.user.getAll() == []


