
class Message():
    def __init__(self, In, db):
        self.updateMembers(In)
        self.db = db
        self.updates = []
        
    
    def updateMembers(self, In):
        (self.id, 
        self.msg,
        self.dateTime,
        self.childID, 
        self.parentID,
        self.sender) = In

    # Pull updates from the database.  This is being taken care of in the parent now
    def update(self, In = None):
        if self.id == -1:
            print("Invalid id")
            return
            
        if In == None:
            In = self.db.message.getByID(self.id)

        print("Update: " + str(In))
        self.updateMembers(In)



    # Get and set
    def setID(self, id):
        self.id == id

    def getID(self):
        return self.id

    def getMsg(self):
        return self.msg

    def getDateTime(self):
        return self.dateTime
    
    def getChildID(self):
        return self.childID

    def getParentID(self):
        return self.parentID

    def getSender(self):
        return self.sender

    #Debug output, not complete
    def print(self):
        print("Msg: " + str(self.msg) + ", DateTime: " + str(self.dateTime) + ", childID: " \
                    + str(self.childID) + ", parenID: " + str(self.parentID) + ", sender: " + str(self.sender)) 
