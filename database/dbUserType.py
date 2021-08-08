from dbTable import Table

class UserType(Table):
    def __init__(self, cnx):
        super().__init__(cnx, "user_type", ("id",), ("type",), [])

    #Add a new user id to the database
    def add(self, userType):

        try:
            super().add("INSERT INTO user_type(type) \
                               VALUES(%s)", (userType,))
        except:
            raise
        
        return self.getID((userType, ))

    #Returns all fields
    def get(self, userType):
        return self.getByID(self.getID((userType, )))

    #Returns user type
    def getType(self, id):
        return self.getFieldByID(id, "type")

    def setType(self, id, newValue):
        return self.setFieldByID(id, "type", newValue)