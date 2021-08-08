class HelpResponse():
    def __init__(self, In, db):
        self.updateMembers(In)
        self.db = db
        self.updates = []

    def updateMembers(self, In):
        (self.id, 
        self.dateTime,
        self.msg,
        self.videoMsg,
        self.responderID,
        self.meetingUrl,
        self.childID,
        self.new) = In

    def pushUpdates(self):
        #print("Help response pushUpdates")
        for table, index in self.updates:
            #print("Help response")
            if index == 'date_time':
                self.db.helpResponse.setDateTime(self.id, self.dateTime)
            elif index == 'msg':
                self.db.helpResponse.setMsg(self.id, self.msg)
            elif index == 'video_msg':
                self.db.helpResponse.setVideoMsg(self.id, self.videoMsg)
            elif index == 'url':
                self.db.helpResponse.setMeetingURL(self.id, self.meetingUrl)
            elif index == 'new':
                self.db.helpResponse.setNew(self.id, self.new)

        self.updates = []

    def update(self, In = None):
        if self.id == -1:
            print("Invalid id")
            return
            
        if In == None:
            In = self.db.helpResponse.getByID(self.id)

        print("Update: " + str(In))
        self.updateMembers(In)
        
    def setID(self, id):
        self.id == id
        
    def getID(self):
        return self.id

    def getDateTime(self):
        return self.dateTime

    def getMsg(self):
        return self.msg
    
    def getVideoMsg(self):
        return self.videoMsg

    def getResponderID(self):
        return self.responderID

    def getMeetingUrl(self):
        return self.meetingUrl

    def getChildID(self):
        return self.childID
        
    def getNew(self):
        return self.new

    def setDateTime(self, newValue):
        self.dateTime = newValue
        self.updates.append(('help_response', 'date_time'))

    def setMsg(self, newValue):
        self.msg = newValue
        self.updates.append(('help_response', 'msg'))

    def setVideoMsg(self, newValue):
        self.videoMsg = newValue
        self.updates.append(('help_response', 'video_msg'))

    def setMeetingUrl(self, newValue):
        self.meetingUrl = newValue
        self.updates.append(('help_response', 'url'))
  
    def setNew(self, newValue):
        self.new = newValue
        self.updates.append(('help_response', 'new'))
  
    def print(self):
        print("dateTime: " + str(self.dateTime) + ", msg: " + str(self.msg))