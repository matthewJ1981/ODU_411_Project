from dbTable import Table

class LogEntry(Table):
    def __init__(self, cnx):
        super().__init__(cnx, "log_entry", ("id","child_id", "date_time", "navigation_state"),
               ("child_id","date_time",), [("child_id",)])

    #Add new navigation step for shedule item scheduleID, returns id of new navigation step
    # def add(self, userID, dateTime, navState, screenshot, errorCode, navStepID):
    def add(self, childID, dateTime, navState):        
        try:
            # super().add("INSERT INTO log_entry (user_id, date_time, navigation_state, screenshot, error_code, nav_step_id) \
            #              VALUES (%s, %s, %s, %s, %s, %s)", (userID, dateTime, navState, screenshot, errorCode, navStepID))
            super().add("INSERT INTO log_entry (child_id, date_time, navigation_state) \
                         VALUES (%s, %s, %s)", (childID, dateTime, navState))
        except:
            print("Error, duplicate entry")
            #raise
        
        return self.getID( (childID, dateTime) )

    #Get all fields by enement name, element type, and schedule item id
    def get(self, childID, dateTime):
        return self.getByID(self.getID((childID, dateTime)))

    #Get user id  by id
    def getUserID(self, id):
        return self.getFieldByID(id, "child_id")

    #Get date time  by id
    def getDateTime(self, id):
        return self.getFieldByID(id, "date_time")

    #Get navigation state by id
    def getNavState(self, id):
        return self.getFieldByID(id, "navigation_state")

    # #Get screenshot id by id
    # def getScreenshot(self, id):
    #     return self.getFieldByID(id, "screenshot")
    
    # #Get error code by id
    # def getErrorCode(self, id):
    #     return self.getFieldByID(id, "error_code")

    # #Get nav step id by id
    # def getNavStepID(self, id):
    #     return self.getFieldByID(id, "nav_step_id")

    # #Get all entries by user
    # def getByUser(self, uid):
    #     return self.getFields(("*",), ("user_id",), (uid,))

    #Get all entries by user
    def getByChild(self, uid):
        return self.getFields(("*",), ("child_id",), (uid,))


    # #Get all entries by error code
    # def getByErrorCode(self, code):
    #     return self.getFields(("*",), ("error_code",), (code,))

    # #Get all entries by navigation step
    # def getByNavStep(self, nsid):
    #     return self.getFields(("*",), ("nav_step_id",), (nsid,))

    # #Remove all entries by user
    # def removeByUser(self, uid):
    #     for log in self.getByUser(uid):
    #         self.remove(log[0])

    #Remove all entries by user
    def removeByChild(self, cid):
        for log in self.getByChild(cid):
            self.remove(log[0])

    # #Remove all entries by error code
    # def removeByErrorCode(self, code):
    #     for log in self.getByErrorCode(code):
    #         self.remove(log[0])

    # #Remove all entries by nav step id
    # def removeByNavStepID(self, nsid):
    #     for log in self.getByNavStep(nsid):
    #         self.remove(log[0])