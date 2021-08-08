from dbTable import Table

class HelpRequest(Table):
    def __init__(self, cnx):
        super().__init__(cnx, "help_request", ("id", "child_id", "date_time"),
               ("date_time", "child_id"), [("child_id",)])

    #Add new help request
    def add(self, dateTime, childID, msg = "Help", videoMsg = None):
        try:
            super().add("INSERT INTO help_request (date_time, msg, video_msg, child_id) \
                         VALUES (%s, %s, %s, %s)", (dateTime, msg, videoMsg, childID))
        except:
            raise
        
        return self.getID( (dateTime, childID) )

    #Get all fields by dateTime and childID
    def get(self, dateTime, childID):
        return self.getByID(self.getID((dateTime, childID)))

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
    
    #Set text message by id
    def setMsg(self, id, newValue):
        return self.setFieldByID(id, "msg", newValue)
    
    #Set video message by id
    def setVideoMsg(self, id, newValue):
        return self.setFieldByID(id, "video_msg", newValue)

    #Get all requests by child
    def getByChild(self, cid):
        return self.getFields(("*",), ("child_id",), (cid,))

    #Remove all steps by child
    def removeByChild(self, cid):
        for step in self.getByChild(cid):
            self.remove(step[0])