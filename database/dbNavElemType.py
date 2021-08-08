from dbTable import Table

class NavElemType(Table):
    def __init__(self, cnx):
        super().__init__(cnx, "nav_elem_type", ("id",),
               ("type_name",), [])

    #Add new element type typename, returns id of new type
    def add(self, typeName):
        try:
            super().add("INSERT INTO nav_elem_type (type_name) \
                         VALUES (%s)", (typeName,))
        except:
            raise
        
        return self.getID((typeName,))

    #Get all fields by typename
    def get(self, typeName):
        return self.getByID(self.getID((typeName,)))

    #get typename by id
    def getTypeName(self, id):
        return self.getFieldByID(id, "type_name")

    #Set typename as newvalue by id
    def setTypeName(self, id, newValue):
        return self.setFieldByID(id, "type_name", newValue)