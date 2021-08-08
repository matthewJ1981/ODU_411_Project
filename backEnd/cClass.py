from cActivity import Activity
import datetime as dt

class Class():
    def __init__(self, In, db):
        self.updateMembers(In)
        self.db = db
        self.initActivities()
        self.updates = []

    def updateMembers(self, In):
        (self.id, 
        self.name,
        self.teacherName,
        self.calendarID) = In

    def update(self, In = None):
        if self.id == -1:
            print("Invalid id")
            return
            
        if In == None:
            In = self.db._class.getByID(self.id)

        print("Update: " + str(In))
        self.updateMembers(In)

    def pushUpdates(self):
        #print("Class pushUpdates")
        for table, index in self.updates:
            if table == 'activity':
                #print("Activity")
                activity = self.activities[index]
                id = self.db.activity.add(activity.getName(), self.id, activity.getHasMacro(), activity.getURL(), activity.getEventID())
                activity.setID(id)
            else:
                #print("Class")
                if index == 'name':
                    self.db._class.setClassName(self.id, self.name)
                elif index == 'teacher_name':
                    self.db._class.setTeacherName(self.id, self.teacherName)
                elif index == 'calender_id':
                    self.db._class.setCalendarID(self.id, self.calendarID)

        self.updates = []

    def initActivities(self):
        result = []

        for activity in self.db.activity.getByClass(self.id):      
            result.append(Activity(activity, self.db))

        self.activities = result

    def addActivity(self, name, hasMacro = None, url = None, eventID = None):
            self.activities.append(Activity((-1, name, self.id, hasMacro, url, eventID), self.db))
            self.updates.append(('activity', len(self.activities) - 1))

    def setID(self, id):
        self.id = id

    def getActivities(self):
        return self.activities

    def getID(self):
        return self.id

    def getName(self):
        return self.name

    def getTeacherName(self):
        return self.teacherName

    def getCalendarID(self):
        return self.calendarID

    def setName(self, newValue):
            self.name = newValue
            self.updates.append(('class', 'name'))

    def setCalendarID(self, newValue):
        self.calendarID = newValue
        self.updates.append(('class', 'calendar_id'))

    def setTeacherName(self, newValue):
            self.teacherName = newValue
            self.updates.append(('class', 'teacher_name'))
            
    def print(self):
        print("Class name: " + str(self.name) + ", teacher name: " + str(self.teacherName))
        for a in self.activities:
            a.print()