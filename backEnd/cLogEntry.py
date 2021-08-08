class LogEntry():
    def __init__(self, In, db):
        self.updateMembers(In)
        self.db = db
        self.updates = []

    def updateMembers(self, In):
        (self.id, 
        self.childID,
        self.dateTime,
        self.navState) = In

    def pushUpdates(self):
        #print("Log Entry pushUpdates")
        for table, index in self.updates:
            #print("Log Entry")
            pass

        self.updates = []
        
    def update(self, In = None):
        if self.id == -1:
            print("Invalid id")
            return
            
        if In == None:
            In = self.db.logEntry.getByID(self.id)

        print("Update: " + str(In))
        self.updateMembers(In)

    def setID(self, id):
        self.id = id
        
    def getID(self):
        return self.id

    def getDateTime(self):
        return self.dateTime

    def getChildID(self):
        return self.childID

    def getNavState(self):
        return self.navState
        
    def print(self):
        print("Log Entry")