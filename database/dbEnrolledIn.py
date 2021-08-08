from dbTable import Table

class EnrolledIn(Table):
    def __init__(self, cnx):
        super().__init__(cnx, "enrolled_in", ("id","child_id","class_id"),
               ("child_id", "class_id"), [("child_id",),("class_id",)])

    #Add new enrolled_in item for child_id and class_id.  Returns id of new enrolled_in item
    def add(self, child_id, class_id):
        try:
            super().add("INSERT INTO enrolled_in (child_id, class_id) \
                         VALUES (%s, %s)", (child_id, class_id,))
        except:
            raise
        
        return self.getID((child_id, class_id))

    #get all fields by class id and child id
    def get(self, class_id, child_id):
        return self.getByID(self.getID((class_id, child_id)))

    #Get class id by id
    def getClassID(self, id):
        return self.getFieldByID(id, "class_id")
    
    #Get child id by id
    def getChildID(self, id):
        return self.getFieldByID(id, "child_id")

    #Get all classes child cid is enrolled in
    def getByChild(self, cid):
        return self.getFields(("*",), ("child_id",), (cid,))

    #Get all childen in class cid
    def getByClass(self, cid):
        return self.getFields(("*",), ("class_id",), (cid,))

    #Remove all enrolled in by child
    def removeByChild(self, cid):
        for ei in self.getByChild(cid):
            self.remove(ei[0])

    #Remove all enrolled in by class
    def removeByClass(self, clid):
        for ei in self.getByClass(clid):
            self.remove(ei[0])
