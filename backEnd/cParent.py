import threading

from cChild import Child
from cHelpResponse import HelpResponse
import datetime as dt

class Parent():
    def __init__(self, In, db):
        self.updateMembers(In)
        self.db = db
        self.initChildren()
        self.initHelpResponses()
        self.updates = []
        
    def updateMembers(self, In):
        (self.id, 
        self.username, 
        self.password, 
        self.email, 
        self.firstName, 
        self.lastName, 
        self.phoneNum) = In

    #self.updates stores a list of tuples of the form (table, index)
    def pushUpdates(self):
        #print("Parent pushUpdates")
        for t in self.updates:
            if t[0] == 'child':
                #print("Child")
                child = self.children[t[1]]
                id = self.db.child.add(child.getName(), child.getAge(), self.id)
                child.setID(id)
            elif t[0] == "help_response":
                #print("Response")
                response = self.helpResponses[t[1]]
                id = self.db.helpResponse.add(response.getDateTime(), self.id, response.getChildID(), response.getMsg())
                response.setID(id)
            else:
                #print("Parent")
                if t[1] == 'password':
                    self.db.parent.setPassword(self.id, self.password)
                elif t[1] == 'email':
                    self.db.parent.setEmail(self.id, self.email)
                elif t[1] == 'firstName':
                    self.db.parent.setFirstName(self.id, self.firstName)
                elif t[1] == 'lastName':
                    self.db.parent.setLastName(self.id, self.lastName)
                elif t[1] == 'phone':
                    self.db.parent.setPhoneNumber(self.id, self.phoneNum)

        self.updates = []

    #updates members from database
    def update(self, In = None):
        if self.id == -1:
            print("Invalid id")
            return
            
        if In == None:
            In = self.db.parent.getByID(self.id)
        print("Update: " + str(In))
        self.updateMembers(In)

    #load children from database
    def initChildren(self):
        result = []

        for child in self.db.getChildrenByID(self.id):      
            result.append(Child(child, self.db))

        self.children = result

    #load help reponses from database
    def initHelpResponses(self):
        def sortBy(res):
            return res.id

        result = []

        for response in self.db.helpResponse.getByResponder(self.id):
            result.append(HelpResponse(response, self.db))

        result.sort(reverse = True, key = sortBy)
        self.helpResponses = result

    #Add a new child.  CHild will be added to the database via the pushupdates method
    def addChild(self, name, age):
        self.children.append(Child((-1, name, age, 0, 0, 1, self.id, ""), self.db))
        self.updates.append(('child', len(self.children) - 1))

    #Add a new helpresponse.  Response will be added to the database via the pushupdates method
    def addHelpResponse(self, msg, dateTime, childID):
        # dateTime = self.db.formatDateTime(dt.datetime.now())
        self.helpResponses.append(HelpResponse((-1, dateTime, msg, None, self.id, None, childID, 1),  self.db))
        self.updates.append(('help_response', len(self.helpResponses) - 1))
        
    def getChildren(self):
        return self.children

    def getHelpResponses(self):
        return self.helpResponses

    def getID(self):
        return self.id

    def getUserName(self):
        return self.username

    def getPassword(self):
        return self.password
    
    def getEmail(self):
        return self.email

    def getFirstName(self):
        return self.firstName

    def getLastName(self):
        return self.lastName
        
    def getPhoneNumber(self):
        return self.phoneNum

    def setPassword(self, newValue):
        self.password = self.db.parent.hashPassword(newValue)
        self.updates.append(('parent', 'password'))

    def setEmail(self, newValue):
        self.email = newValue
        self.updates.append(('parent', 'email'))


    def setFirstName(self, newValue):
        self.firstName = newValue
        self.updates.append(('parent', 'firstName'))

    def setLastName(self, newValue):
        self.lastName = newValue
        self.updates.append(('parent', 'lastName'))

    def setPhoneNumber(self, newValue):
        self.phone = newValue
        self.updates.append(('parent', 'phone'))

    #Debug output, still not complete
    def print(self):
        print("Name: " + str(self.firstName) + " Phone: " + str(self.phoneNum))
        for c in self.children:
            c.print()

        for r in self.helpReponses:
            r.print()