from dbTable import Table

class ScheduleItem(Table):
    def __init__(self, cnx):
        super().__init__(cnx, "schedule_item", ("activity_id",),
               ("date_time", "activity_id"), [("activity_id",)])

    #Add new schedule item for class activity_id. Returns if of new schedule item
    def add(self, dateTime, duration, activity_id):
        try:
            super().add("INSERT INTO schedule_item (date_time, duration, activity_id) \
                         VALUES (%s, %s, %s)", (dateTime, duration, activity_id))
        except:
            raise
        
        return self.getID((dateTime, activity_id))

    #Get all fields by datetime and class id
    def get(self, dateTime, activity_id):
        return self.getByID(self.getID((dateTime, activity_id)))

    #Get datetime by id
    def getDateTime(self, id):
        return self.getFieldByID(id, "date_time")
    
    #Get duration by id
    def getDuration(self, id):
        return self.getFieldByID(id, "duration")

    #get activity id by id
    def getActivityID(self, id):
        return self.getFieldByID(id, "activity_id")



    #set new datetime by id
    def setDateTime(self, id, newValue):
        return self.setFieldByID(id, "date_time", newValue)

    #set new duration by id
    def setDuration(self, id, newValue):
        return self.setFieldByID(id, "duration", newValue)



    #Get all schedule items for class cid
    def getByActivity(self, aid):
        return self.getFields(("*"), ("activity_id",), (aid,))
    
    def removeByActivity(self, aid):
        for item in self.getByActivity(aid):
            self.remove(item[0])