class InputData():
    def __init__(self, In, db):
        self.updateMembers(In)
        self.db = db
        self.updates = []

    def updateMembers(self, In):
        (self.id, 
        self.dateTime,
        self.childID,
        self.x,
        self.y,
        self.keyboard) = In

    def pushUpdates(self):
        #print("Input Data pushUpdates")
        for table, index in self.updates:
            #print("Input data")
            pass

        self.updates = []

    def update(self, In = None):
        if self.id == -1:
            print("Invalid id")
            return
            
        if In == None:
            In = self.db.inputData.getByID(self.id)

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

    def getX(self):
        return self.x
        
    def getY(self):
        return self.y

    def getKeyboard(self):
        return self.keyboard

    def print(self):
        print("Input Data " + self.dateTime)
