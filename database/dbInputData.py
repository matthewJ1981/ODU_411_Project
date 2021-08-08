from dbTable import Table

class InputData(Table):
    def __init__(self, cnx):
        super().__init__(cnx, "input_data", ("id","date_time", "child_id", "mouse_x", "mouse_y", "keyboard_input"),
               ("date_time","child_id"), [("child_id",)])

    #Add new navigation step for shedule item scheduleID, returns id of new navigation step
    def add(self, dateTime, childID, mouseX, mouseY, keyboard):
        try:
            super().add("INSERT INTO input_data (date_time, child_id, mouse_x, mouse_y, keyboard_input) \
                         VALUES (%s, %s, %s, %s, %s)", (dateTime, childID, mouseX, mouseY, keyboard))
        except:
            print("Error, duplicate entry")
            #raise
        
        return self.getID( (dateTime, childID) )

    #Get all fields by datetime and child id
    def get(self, dateTime, childID):
        return self.getByID(self.getID((dateTime, childID)))

    #Get date time by id
    def getDateTime(self, id):
        return self.getFieldByID(id, "date_time")

    #Get child id
    def getChildID(self, id):
        return self.getFieldByID(id, "child_id")

    #Get mouse x
    def getMouseX(self, id):
        return self.getFieldByID(id, "mouse_x")

    #Get mouse y
    def getMouseY(self, id):
        return self.getFieldByID(id, "mouse_y")
    
    #Get keyboard input
    def getKeyboard(self, id):
        return self.getFieldByID(id, "keyboard_input")

    #Get by child
    def getByChild(self, cid):
        return self.getFields(("*",), ("child_id",), (cid,))

    #Remove by child
    def removeByChild(self, cid):
        for data in self.getByChild(cid):
            self.remove(data[0])