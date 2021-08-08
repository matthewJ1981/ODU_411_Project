from dbTable import Table

class NavigationStep(Table):
    def __init__(self, cnx):
        super().__init__(cnx, "navigation_step", ("id","activity_id"),
               ("elem_name","elem_type", "activity_id"), [("activity_id",)])

    #Add new navigation step for shedule item scheduleID, returns id of new navigation step
    def add(self, elemName, elemType, stepIndex, activityID, img = b'0'):
        try:
            super().add("INSERT INTO navigation_step (elem_name, elem_type, step_index, activity_id, img) \
                         VALUES (%s, %s, %s, %s, %s)", (elemName, elemType, stepIndex, activityID, img))
        except:
            raise
        
        return self.getID( (elemName, elemType, activityID) )

    #Get all fields by enement name, element type, and schedule item id
    def get(self, elemName, elemType, activity_id):
        return self.getByID(self.getID((elemName, elemType, activity_id)))

    #Get element name by id
    def getElemName(self, id):
        return self.getFieldByID(id, "elem_name")

    #Get element type by id
    def getElemType(self, id):
        return self.getFieldByID(id, "elem_type")

    #Get index of step by id
    def getIndex(self, id):
        return self.getFieldByID(id, "step_index")

    #Get schedule id by id
    def getActivityID(self, id):
        return self.getFieldByID(id, "activity_id")
    
    #Get image by id
    def getImage(self, id):
        return self.getFieldByID(id, "img")

    #Set element name by id
    def setElemName(self, id, newValue):
        return self.setFieldByID(id, "elem_name", newValue)
    
    #Set element type by id.  Type has to exist in nav_elem_type table
    def setElemType(self, id, newValue):
        return self.setFieldByID(id, "elem_type", newValue)
    
    #Set step index by id
    def setIndex(self, id, newValue):
        return self.setFieldByID(id, "step_index", newValue)

    #Set image by id
    def setImage(self, id, newValue):
        return self.setFieldByID(id, "img", newValue)

    #Get all steps for schedule item sid
    def getByActivity(self, aid):
        return self.getFields(("*",), ("activity_id",), (aid,))

    def removeByActivity(self, aid):
        for step in self.getByActivity(aid):
            self.remove(step[0])