class ScheduleItem():
    def __init__(self, In, db):
        self.updateMembers(In)
        self.db = db
        self.updates = []

    def pushUpdates(self):
        #print("Schedule Item pushUpdates")
        for table, index in self.updates:
            #print("Schedule Item")
            if index == 'date_time':
                self.db.scheduleItem.setDateTime(self.id, self.dateTime)
            elif index == 'duration':
                self.db.scheduleItem.setAge(self.id, self.age)

        self.updates = []

    def updateMembers(self, In):
        (self.id, 
        self.dateTime,
        self.duration,
        self.activityID) = In

    def update(self, In = None):
        if self.id == -1:
            print("Invalid id")
            return

        if In == None:
            In = self.db.scheduleItem.getByID(self.id)
        print("Update: " + str(In))
        self.updateMembers(In)

    def setID(self, id):
        self.id = id

    def getID(self):
        return self.id

    def getDateTime(self):
        return self.dateTime

    def getDuration(self):
        return self.duration
    
    def getActivityID(self):
        return self.activityID
        
    def setDateTIme(self, newValue):
            self.dateTime = newValue
            self.updates.append(('schedule_item', 'date_time'))

    def setDuration(self, newValue):
            self.duration = newValue
            self.updates.append(('schedule_item', 'duration'))

    def print(self):
        print("DateTime: " + str(self.dateTime) + ", Duration: " + str(self.duration))
