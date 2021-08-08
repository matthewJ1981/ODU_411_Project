from cScheduleItem import ScheduleItem
from cMacroElement import MacroElement
import datetime as dt

class Activity():
    def __init__(self, In, db):

        self.updateMembers(In)
        self.db = db
        self.initScheduleItems()
        self.updates = []

    def updateMembers(self, In):
        (self.id, 
        self.name,
        self.classID, 
        self.hasMacro,
        self.url,
        self.eventID) = In

    def pushUpdates(self):
       # print("Activity pushUpdates")
        for table, index in self.updates:
            if table == 'schedule_iten':
                print("Schedule Item")
                item = self.scheduleItems[index]
                id = self.db.scheduleItem.add(item.getDateTime(), item.getDuration(), self.id, item.getCalendarID())
                item.setID(id)
            else:
                #print("Activity")
                if index == 'name':
                    self.db.activity.setName(self.id, self.name)
                elif index == 'has_macro':
                    self.db.activity.setHasMacro(self.id, self.hasMacro)
                elif index == 'url':
                    self.db.activity.setURL(self.id, self.url)
                elif index == 'event_id':
                    self.db.activity.setEventID(self.id, self.eventID)

        self.updates = []

    def update(self, In = None):
        if self.id == -1:
            print("Invalid id")
            return
            
        if In == None:
            In = self.db.activity.getByID(self.id)

        print("Update: " + str(In))
        self.updateMembers(In)


    def initScheduleItems(self):
        result = []

        for item in self.db.scheduleItem.getByActivity(self.id):      
            result.append(ScheduleItem(item, self.db))

        self.scheduleItems = result

    def addScheduleItem(self, dateTime, duration):
        try:
            #id = self.db.scheduleItem.add(dateTime, duration, self.id)
            #self.scheduleItems.append(ScheduleItem(self.db.scheduleItem.getByID(id), self.db))
            self.scheduleItems.append(ScheduleItem((-1, dateTime, duration, self.id), self.db))
            self.updates.append(('schedule_item', len(self.scheduleItems) - 1))
        except:
            raise
        
    def getScheduleItems(self):
        return self.scheduleItems

    def setID(self, id):
        self.id = id

    def getID(self):
        return self.id

    def getName(self):
        return self.name

    def getHasMacro(self):
        return self.hasMacro

    def getURL(self):
        return self.url

    def getClassID(self):
        return self.classID

    def getEventID(self):
        return self.eventID

    def setName(self, newValue):
            self.name = newValue
            self.updates.append(('activity', 'name'))

    def setHasMacro(self, newValue):
            self.hasMacro = newValue
            self.updates.append(('activity', 'has_macro'))

    def setURL(self, newValue):
            self.url = newValue
            self.updates.append(('activity', 'url'))

    def setEventID(self, newValue):
            self.eventID = newValue
            self.updates.append(('activity', 'event_id'))

    def setScheduleItem(self,newValue):
        for i in self.scheduleItems:
            i.dateTime=newValue
    
    #just returns datetime object 
    def getScheduleItem(self):
        for i in self.scheduleItems:
            return i.dateTime

    def print(self):
        print("Name: " + str(self.name))
        for i in self.scheduleItems:
            i.print()