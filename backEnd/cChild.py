from cClass import Class
from cHelpRequest import HelpRequest
from cMacroElement import MacroElement
from cLogEntry import LogEntry
from cInputData import InputData
import threading
import time

class Child():
    def __init__(self, In, db):
        self.updateMembers(In)
        self.db = db
        self.initClasses()
        self.initHelpRequests()
        self.initMacroElements()
        self.initLogEntries()
        self.initInputData()
        self.updates = []
        if self.image == None:
            self.image = 'student/frontEnd/images/avatar.png'        
    
        self._lock = False
        self.size = 0

    def locked(self):
        return self.locked == True
    def lock(self):
        self._lock = True
    def unlock(self):
        self._lock = False

    def updateMembers(self, In):
        (self.id, 
        self.name,
        self.age,
        self.raisedHand,
        self.navFailed,
        self.skillLevel,
        self.parentID,
        self.image) = In

    # Pull updates from the database.  This is being taken care of in the parent now
    def update(self, In = None):
        #print("Pulling updates")
        if self.locked():
            return

        self.lock()
        if self.id == -1:
            print("Invalid id")
            return
            
        if In == None:
            In = self.db.child.getByID(self.id)

        print("Update: " + str(In))
        self.updateMembers(In)
        self.unlock()

    #Push updates to the database
    def pushUpdates(self):
        
        #print("Child pushUpdates")
        # while self.locked():
        #     pass
        if self.locked():
            return

        self.lock()
        #print("Updates: " + str(time.perf_counter()))
        
        for table, index in self.updates:
            if table == 'input_data':
                #print("Size:" + str(self.size))
                if (self.size >= len(self.inputData)):
                    continue
                #print("Input data")
                #data = self.inputData[len(self.inputData) - 1]
                #print("Length: " + str(len(self.inputData)) + " Index: " + str(index))
                data = self.inputData[index]
                id = self.db.inputData.add(data.getDateTime(), self.id, data.getX(), data.getY(), data.getKeyboard())
                data.setID(id)
            elif table == "log_entry":
                #print("Log entry")
                entry = self.logEntries[index]
                id = self.db.logEntry.add(self.id, entry.getDateTime(), entry.getNavState())
                entry.setID(id)
            elif table == "macro_element":
                #print("Macro element")
                elem = self.macroElements[index]
                id = self.db.macroElement.add(elem.getOrderNum(), self.id, elem.getActivityID(), elem.getMacroName(), elem.getUrl(),
                                                elem.getHasInput(), elem.getInput(), elem.getImgPath(), elem.getImg(), elem.getX(), elem.getY())
                elem.setID(id)
            elif table == "help_request":
                #print("Help request")
                req = self.helpRequests[index]
                id = self.db.helpRequest.add(req.getDateTime(), self.id, req.getMsg())
                req.setID(id)
            elif table == "class":
                #print("Class")
                cl = self.classes[index]
                id = self.db._class.add(cl.getName(), cl.getTeacherName())
                cl.setID(id)
                self.db.enrolledIn.add(self.id, id)
            else:
                #print("Child")
                if index == 'name':
                    self.db.child.setName(self.id, self.name)
                elif index == 'age':
                    self.db.child.setAge(self.id, self.age)
                elif index == 'raised_hand':
                    self.db.child.setRaisedHand(self.id, self.raisedHand)
                elif index == 'nav_failed':
                    self.db.child.setNavFailed(self.id, self.navFailed)
                elif index == 'skill_level':
                    self.db.child.setSkillLevel(self.id, self.skillLevel)
                elif index == 'image':
                    self.db.child.setImage(self.id, self.image)

        self.updates = []
        self.unlock()

    #Pull classes the child is in from the database
    def initClasses(self):
        result = []

        for eid, cid, clid in self.db.enrolledIn.getByChild(self.id):      
            result.append(Class(self.db._class.getByID(clid), self.db))

        self.classes = result

    #Pull childs help requests from the database
    def initHelpRequests(self):
        def sortBy(req):
            return req.id

        result = []

        for request in self.db.helpRequest.getByChild(self.id):      
            result.append(HelpRequest(request, self.db))

        result.sort(reverse = True, key = sortBy)
        # print("Init help requests: ")
        # for r in result:
        #     r.print()
        self.helpRequests = result

    #Pull childs macro elements from the database
    def initMacroElements(self):
        result = []

        for elem in self.db.macroElement.getByChild(self.id):
            result.append(MacroElement(elem, self.db))

        self.macroElements = result

    #Pull childs log entries from the database
    def initLogEntries(self):
        result = []

        for log in self.db.logEntry.getByChild(self.id):
            result.append(LogEntry(log, self.db))

        self.logEntries = result

    #Pull childs input data from the database
    def initInputData(self):
        while self.locked():
            pass

        self.lock()
        result = []

        for data in self.db.inputData.getByChild(self.id):
            result.append(InputData(data, self.db))

        self.size = len(result)
        self.inputData = result                

        self.unlock()
    #Add methods
    def addClass(self, name, teacherName):
        self.classes.append(Class((-1, name, teacherName, None), self.db))
        self.updates.append(('class', len(self.classes) - 1))

    def addHelpRequest(self, msg, dateTime):
        self.helpRequests.append(HelpRequest((-1, dateTime, msg, None, self.id), self.db))
        self.updates.append(('help_request', len(self.helpRequests) - 1))


    def addMacroElement(self, orderNum, activity_id = None, macroName = None, url = None, hasInput = None,
                        _input = None, imgPath = None, img = None, x = None, y = None):
        self.macroElements.append(MacroElement((-1, orderNum, self.id, activity_id, macroName, url, hasInput, _input, imgPath, img, x, y), self.db))
        self.updates.append(('macro_element', len(self.macroElements) - 1))

    def addLogEntry(self, dateTime, navState):
        self.logEntries.append(LogEntry((-1, self.id, dateTime, navState), self.db))
        self.updates.append(('log_entry', len(self.logEntries) - 1))


    def addInputData(self, dateTime, x, y, keyboard):
        
        # while(self.locked()):
        #     pass

        if self.locked():
            return
        #print("Add: " + str(time.perf_counter()))
        self.lock()
        self.size = len(self.inputData)
        self.inputData.append(InputData((-1, dateTime, self.id, x, y, keyboard), self.db))
        # for e in self.inputData:
        #     e.print()
        self.updates.append(('input_data', len(self.inputData) - 1))
        self.unlock()

    # Get and set
    def setID(self, id):
        self.id == id

    def getID(self):
        return self.id

    def getName(self):
        return self.name

    def getAge(self):
        return self.age
    
    def getRaisedHand(self):
        return self.raisedHand

    def getNavFailed(self):
        return self.navFailed

    def getSkillLevel(self):
        return self.skillLevel

    def getParentID(self):
        return self.parentID
        
    def getImage(self):
        return self.image

    def setName(self, newValue):
        self.name = newValue
        self.updates.append(('child', 'name'))

    def setAge(self, newValue):
        self.age = newValue
        self.updates.append(('child', 'age'))

    def setRaisedHand(self, newValue):
        self.raisedHand = newValue
        self.updates.append(('child', 'raised_hand'))

    def setNavFailed(self, newValue):
        self.navFailed = newValue
        self.updates.append(('child', 'nav_failed'))

    def setSkillLevel(self, newValue):
        self.skillLevel = newValue
        self.updates.append(('child', 'skill_level'))

    def setImage(self, newValue):
        self.image = newValue
        self.updates.append(('child', 'image'))
        
    def getClasses(self):
        return self.classes

    def getLogEntries(self):
        return self.logEntries

    def getInputData(self):
        return self.inputData

    def getHelpRequests(self):
        return self.helpRequests

    def getMacroElements(self):
        return self.macroElements

    #Debug output, not complete
    def print(self):
        print("Name: " + str(self.name) + ", Age: " + str(self.age))
        for c in self.classes:
            c.print()
        for r in self.helpRequests:
            r.print()
        for e in self.macroElements:
            e.print()
        for e in self.logEntries:
            e.print()
        for e in self.inputData:
            e.print()