import pytest
# import os, sys
# sys.path.insert(0, os.path.abspath("database"))

from database import database
import datetime

import pdb

class TestDB:
    db = database()
    db.createTestDB()

    username = "testParent"
    password = "testPW"
    email = "testEmail"
    firstName = "testFName"
    lastName = "testLName"

    childName = "testChild"
    childAge = 100
    raised_hand = 0
    skill_level = 1

    className = "Math"
    teacherName = "Sue Bird"

    bubbleName = "Bubble1"

    dateTime = datetime.datetime.now()
    duration = 12
    elemName = "www.google.com"
    elemType = "Button"
    index = 1
    img = b'0'

    typeName = "Button"

    pid = -1
    cid = []
    clid = -1
    bid = -1
    hsid = -1
    neid = -1
    nsid = -1
    siid = -1
    moid = -1

    fields = []

    ### SETUP ####
    def setup_method(self):
        self.db = database()
        self.db.useDB()

        try:
            self.db.userType.add("Parent")
            self.db.userType.add("Child")
        except:
            pass
        self.addParent()
        self.addChild()
        self.addClass()
        self.addEnrolledIn()
        self.addScheduleItem()
        self.addBubble()
        self.addNavElemType()
        self.addNavigationStep()
        self.addMemberOf()

    ### TEARDOWN ####
    def teardown_method(self):
        self.cid.clear()
        self.db.removeAll()
        self.db.close()

    ### HELPERS ####
    def addParent(self):
        try:
            self.pid = self.db.parent.add(self.username, self.password, self.email, self.firstName, self.lastName)
        except Exception as e:
            print(e)
            return -1

        return self.pid

    def addChild(self):
        try:
            self.cid.append(self.db.child.add(self.childName, self.childAge, self.pid))
        except Exception as e:
            print(e)
            return -1

        return self.cid[-1]

    def addClass(self):
        try:
            self.clid = self.db._class.add(self.className, self.teacherName)
        except Exception as e:
            print(e)
            return -1

        return self.clid

    def addBubble(self):
        try:
            self.bid = self.db.bubble.add(self.bubbleName)
        except Exception as e:
            print(e)
            return -1

        return self.bid

    def addEnrolledIn(self):
        try:
            print(self.cid[0])
            print(self.clid)
            self.hsid = self.db.enrolledIn.add(self.cid[0], self.clid)
        except Exception as e:
            print(e)
            return -1

        return self.hsid

    def addNavElemType(self):
        try:
            self.neid = self.db.navElemType.add(self.typeName)
        except Exception as e:
            print(e)
            return -1

        return self.neid

    def addNavigationStep(self):
        try:
            self.nsid = self.db.navigationStep.add(self.elemName, self.elemType, self.index, self.siid, self.img)
        except Exception as e:
            print(e)
            return -1

        return self.nsid

    def addScheduleItem(self):
        try:
            self.dateTime = self.db.formatDateTime(datetime.datetime.now())
            self.siid = self.db.scheduleItem.add(self.dateTime, self.duration, self.clid)
        except Exception as e:
            print(e)
            return -1

        return self.siid

    def addMemberOf(self):
        try:
            self.moid = self.db.memberOf.add(self.pid, self.bid)
        except Exception as e:
            print(e)
            return -1

        return self.moid

    #### tests ####

    def testUserExists(self):
        assert self.db.userExists(self.username) == True

    def testStrongPassword(self):
        assert self.db.strongPassword(self.password) == False
        assert self.db.strongPassword("12345678") == True

    def testFormatDateTime(self):
        dt = datetime.datetime.now()
        expected = dt.strftime("%m/%d/%y %H:%M:%S")
        actual = self.db.formatDateTime(dt)

        assert expected == actual

    def testGetChildren(self):
        children = self.db.getChildren(self.username)
        assert children[0][1] == self.childName
    def testGetChildrenByID(self):
        children = self.db.getChildrenByID(self.pid)
        assert children[0][1] == self.childName
   
    def testRemoveAll(self):
        self.db.removeAll()
        assert self.db.parent.getAll() == []

    def testGetClassesForChild(self):
        assert len(self.db.getClassesForChild(self.cid[0])) == 1

    def testGetChildrenInClass(self):
        assert len(self.db.getChildrenInClass(self.clid)) == 1
    
    def testGetChildrenInClasses(self):
        assert len(self.db.getChildrenInClasses()) == 1


