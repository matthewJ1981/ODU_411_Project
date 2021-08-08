from dbTable import Table

class MacroElement(Table):
    def __init__(self, cnx):
        super().__init__(cnx, "macro_element", ("id","child_id"),
               ("orderNum", "child_id", "macroName"), [("child_id",)])

    #Add new navigation step for shedule item scheduleID, returns id of new navigation step
    def add(self, orderNum, child_id, activity_id = None, macroName = None, url = None, hasInput = None,
             _input = None, imgPath = None, img = None, x = None, y = None):
        try:
            query = "INSERT INTO macro_element (orderNum, child_id, activity_id, macroName, url, hasInput, input, imgPath, img, x, y) \
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (orderNum, child_id, activity_id, macroName, url, hasInput, _input, imgPath, img, x, y)
            # print(query)
            #print(values)
            super().add(query, values)
        except Exception as e:
            print("macro add")
            print(e)
            raise
        
        return self.getID( (orderNum, child_id, macroName) )

    #Get all fields by enement name, element type, and schedule item id
    def get(self, orderNum, child_id, macroName):
        return self.getByID(self.getID((orderNum, child_id, macroName)))


    #Get macroName by id
    def getMacroName(self, id):
        return self.getFieldByID(id, "macroName")

    #Get URL by id
    def getURL(self, id):
        return self.getFieldByID(id, "url")

    #Get order number by id
    def getOrderNum(self, id):
        return self.getFieldByID(id, "orderNum")

    #Get activity id by id
    def getChildID(self, id):
        return self.getFieldByID(id, "child_id")

    #Get activity id by id
    def getActivityID(self, id):
        return self.getFieldByID(id, "activity_id")
    
    #Get image by id
    def getImage(self, id):
        return self.getFieldByID(id, "img")
    
    #Get image by id
    def getImagePath(self, id):
        return self.getFieldByID(id, "imgPath")

    #Get has input by id
    def getHasInput(self, id):
        return self.getFieldByID(id, "hasInput")

    #Get input by id
    def getInput(self, id):
        return self.getFieldByID(id, "input")
            
    #Get x by id
    def getX(self, id):
        return self.getFieldByID(id, "x")
            
    #Get y by id
    def getY(self, id):
        return self.getFieldByID(id, "y")


    #Set macro name by id
    def setMacroName(self, id, newValue):
        return self.setFieldByID(id, "macroName", newValue)
    
    #Set url
    def setURL(self, id, newValue):
        return self.setFieldByID(id, "url", newValue)
    
    #Set image path by id
    def setImagePath(self, id, newValue):
        return self.setFieldByID(id, "imgPath", newValue)

    #Set image by id
    def setImage(self, id, newValue):
        return self.setFieldByID(id, "img", newValue)

    #Set hasInput by id
    def setHasInput(self, id, newValue):
        return self.setFieldByID(id, "hasInput", newValue)

    #Set image by id
    def setInput(self, id, newValue):
        return self.setFieldByID(id, "input", newValue)

    #Set image by id
    def setX(self, id, newValue):
        return self.setFieldByID(id, "x", newValue)

    #Set image by id
    def setY(self, id, newValue):
        return self.setFieldByID(id, "y", newValue)

    #Get all steps for schedule item sid
    def getByActivity(self, aid):
        return self.getFields(("*",), ("activity_id",), (aid,))

    #Get all steps for schedule item sid
    def getByChild(self, cid):
        return self.getFields(("*",), ("child_id",), (cid,))

    def removeByActivity(self, aid):
        for step in self.getByActivity(aid):
            self.remove(step[0])

    def removeByChild(self, cid):
        for step in self.getByChild(cid):
            self.remove(step[0])