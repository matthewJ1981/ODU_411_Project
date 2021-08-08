from dbTable import Table

class Class(Table):
    def __init__(self, cnx):
        super().__init__(cnx, "class", ("id",), ("name", "teacher_name"), [])

    #Add new class to database with name and teachername, returns id of new class
    def add(self, name, teacherName,  calendarID = None):
        try:
            super().add("INSERT INTO class (name, teacher_name, calendar_id) \
                         VALUES (%s, %s, %s)", (name, teacherName, calendarID))
        except:
            raise
        
        return self.getID((name, teacherName))

    #Get all fields by name, teacher_name
    def get(self, name, teacher_name):
        return self.getByID(self.getID((name, teacher_name)))
    
    #Get class name by id
    def getClassName(self, id):
        return self.getFieldByID(id, "name")

    #get calender id
    def getCalendarID(self, id):
        return self.getFieldByID(id, "calendar_id")

    #Get teacher name by id
    def getTeacherName(self, id):
        return self.getFieldByID(id, "teacher_name")

    #Set classname as newvalue for id
    def setClassName(self, id, newValue):
        return self.setFieldByID(id, "name", newValue)

    #Set teachername as newvalue for id
    def setTeacherName(self, id, newValue):
        return self.setFieldByID(id, "teacher_name", newValue)

    #set new calnedar id
    def setCalendarID(self, id, newValue):
        return self.setFieldByID(id, "calendar_id", newValue)
