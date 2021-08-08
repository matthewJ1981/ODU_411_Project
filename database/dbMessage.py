from dbTable import Table

class Message(Table):
    def __init__(self, cnx):
        super().__init__(cnx, "message", ("id", "msg", "date_time", "child_id", "parent_id"), ("sender","date_time"), [("parent_id",), ("child_id",)])

    #Add message
    def add(self, msg, dateTime, childID, parentID, sender):
        try:
            super().add("INSERT INTO message(msg, date_time, child_id, parent_id, sender) \
                               VALUES(%s, %s, %s, %s, %s)", (msg, dateTime, childID, parentID, sender))
        except:
            raise
        
        id = self.getID((sender, dateTime))
        return id

    #Get all fields by id
    def get(self, sender, dateTime):
        return self.getByID(self.getID((sender, dateTime)))

    #Get name by child id
    def getMsg(self, id):
        return self.getFieldByID(id, "msg")

    #Get age by child id
    def getDateTime(self, id):
        return self.getFieldByID(id, "date_time")

    #Get raised hand by child id
    def getChildID(self, id):
        return self.getFieldByID(id, "child_id")

    #Get Nav failed by child id
    def getParentID(self, id):
        return self.getFieldByID(id, "parent_id")

    def getByParent(self, pid):
        return self.getFields(("*",), ("parent_id",), (pid,))

    def getByChild(self, pid):
        return self.getFields(("*",), ("child_id",), (pid,))

    def getByParentAndChild(self, pid, cid):
        def sortBy(res):
            return res[2]
        
        temp = self.getFields(("*",), ("parent_id", "child_id"), (pid,cid))
        temp.sort(key = sortBy)
        return temp
        
    #Remove all messages with parent id pid
    def removeByParent(self, pid):
        for x in self.getByParent(pid):
            self.remove(x[0])
            
    def removeByChild(self, pid):
        for x in self.getByChild(pid):
            self.remove(x[0])


