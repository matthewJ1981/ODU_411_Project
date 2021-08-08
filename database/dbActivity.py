from dbTable import Table

class Activity(Table):
    def __init__(self, cnx):
        super().__init__(cnx, "activity", ("id", "class_id"),
               ("name", "class_id"), [("class_id",)])

    def add(self, name, class_id, hasMacro = None, url = None, eventID = None):
        try:
            super().add("INSERT INTO activity (name, class_id, has_macro, url, event_id) \
                         VALUES (%s, %s, %s, %s, %s)", (name, class_id, hasMacro, url, eventID))
        except:
            raise
        
        return self.getID((name, class_id))

    #get all fields by class id and name
    def get(self, name, class_id):
        return self.getByID(self.getID((name, class_id)))

    def setName(self, id, newValue):
        return self.setFieldByID(id, "name", newValue)

    def setHasMacro(self, id, newValue):
        return self.setFieldByID(id, "has_macro", newValue)

    def setURL(self, id, newValue):
        return self.setFieldByID(id, "url", newValue)

    def setEventID(self, id, newValue):
        return self.setFieldByID(id, "event_id", newValue)

    def getClassID(self, id):
        return self.getFieldByID(id, "class_id")

    def getHasMacro(self, id):
        return self.getFieldByID(id, "has_macro")

    def getURL(self, id):
        return self.getFieldByID(id, "url")

    def getEventID(self, id):
        return self.getFieldByID(id, "event_id")

    def getName(self, id):
        return self.getFieldByID(id, "name")

    def getByClass(self, cid):
        return self.getFields(("*",), ("class_id",), (cid,))

    def removeByClass(self, clid):
        for a in self.getByClass(clid):
            self.remove(a[0])
