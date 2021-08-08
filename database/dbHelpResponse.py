from dbTable import Table

class HelpResponse(Table):
    def __init__(self, cnx):
        super().__init__(cnx, "help_response", ("id", "date_time", "responder_id", "child_id"),
               ("date_time", "responder_id"), [("child_id",),("responder_id",)])

    #Add new help response
    def add(self, dateTime, responderID, childID, msg = "Help", videoMsg = None, meetingURL = None):
        try:
            super().add("INSERT INTO help_response (date_time, msg, video_msg, responder_id, meeting_url, child_id, new) \
                         VALUES (%s, %s, %s, %s, %s, %s, %s)", (dateTime, msg, videoMsg, responderID, meetingURL, childID, 1))
        except:
            raise
        
        return self.getID( (dateTime, responderID) )

    #Get all fields by dateTime and childID
    def get(self, dateTime, responderID):
        return self.getByID(self.getID((dateTime, responderID)))

    #Get datetime by id
    def getDateTime(self, id):
        return self.getFieldByID(id, "date_time")

    #Get text message by id
    def getMsg(self, id):
        return self.getFieldByID(id, "msg")

    #Get video message by id
    def getVideoMsg(self, id):
        return self.getFieldByID(id, "video_msg")

    #Get child id by id
    def getChildID(self, id):
        return self.getFieldByID(id, "child_id")
    
    #Get responder id by id
    def getResponderID(self, id):
        return self.getFieldByID(id, "responder_id")

    #Get url id by id
    def getMeetingURL(self, id):
        return self.getFieldByID(id, "meeting_url")

    #Get if msg is new
    def getNew(self, id):
        return self.getFieldByID(id, "new")

    #Set text message by id
    def setMsg(self, id, newValue):
        return self.setFieldByID(id, "msg", newValue)
    
    #Set video message by id
    def setVideoMsg(self, id, newValue):
        return self.setFieldByID(id, "video_msg", newValue)

    #Set meeting url by id
    def setMeetingURL(self, id, newValue):
        return self.setFieldByID(id, "meeting_url", newValue)

    #Set is new
    def setNew(self, id, newValue):
        return self.setFieldByID(id, "new", newValue)

    #Get all responses for child
    def getByChild(self, cid):
        return self.getFields(("*",), ("child_id",), (cid,))

    #Get all responses by responder
    def getByResponder(self, rid):
        return self.getFields(("*",), ("responder_id",), (rid,))

    #Remove all responses for child
    def removeByChild(self, cid):
        for step in self.getByChild(cid):
            self.remove(step[0])

    #Remove all responses by responder
    def removeByResponder(self, rid):
        for step in self.getByResponder(rid):
            self.remove(step[0])