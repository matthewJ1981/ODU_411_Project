class HelpRequest():
    def __init__(self, In, db):
        self.updateMembers(In)
        self.db = db
        self.updates = []

    def updateMembers(self, In):
        (self.id, 
        self.dateTime,
        self.msg,
        self.videoMsg,
        self.childID) = In

    def pushUpdates(self):
        #print("Help Request pushUpdates")
        for table, index in self.updates:
            #print("Help Request")
            if index == 'date_time':
                self.db.helpRequest.setDateTime(self.id, self.dateTime)
            elif index == 'msg':
                self.db.helpRequest.setMsg(self.id, self.msg)
            elif index == 'video_msg':
                self.db.helpRequest.setVideoMsg(self.id, self.videoMsg)

        self.updates = []

    def update(self, In = None):
        if self.id == -1:
            print("Invalid id")
            return
            
        if In == None:
            In = self.db.helpRequest.getByID(self.id)
            
        print("Update: " + str(In))
        self.updateMembers(In)
        
    def setID(self, id):
        self.id = id
        
    def getID(self):
        return self.id

    def getDateTime(self):
        return self.dateTime

    def getMsg(self):
        return self.msg
    
    def getVideoMsg(self):
        return self.videoMsg

    def getChildID(self):
        return self.childID
        
    def setDateTime(self, newValue):
            self.dateTime = newValue
            self.updates.append(('help_request', 'date_time'))

    def setMsg(self, newValue):
            self.msg = newValue
            self.updates.append(('help_request', 'msg'))

    def setVideoMsg(self, newValue):
            self.videoMsg = newValue
            self.updates.append(('help_request', 'video_msg'))

    def print(self):
        print("dateTime: " + str(self.dateTime) + ", msg: " + str(self.msg))