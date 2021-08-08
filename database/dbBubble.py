from dbTable import Table

class Bubble(Table):
    def __init__(self, cnx):
        super().__init__(cnx, "bubble", ("id",), ("name",), [])

    #Add new bubble to database with name, returns id of new bubble
    def add(self, name):
        try:
            super().add("INSERT INTO bubble (name) \
                         VALUES (%s)", (name,))
        except:
            raise
        
        return self.getID((name,))

    #Get all fields by name
    def get(self, name):
        return self.getByID(self.getID((name,)))

    #Get name by id
    def getName(self, id):
        return self.getFieldByID(id, "name")

    #Set name as newValue for id
    def setName(self, id, newValue):
        return self.setFieldByID(id, "name", newValue)