from dbTable import Table

class User(Table):
    def __init__(self, cnx):
        super().__init__(cnx, "user", ("id", "type", "user_id"), ("type","user_id"), [("type",)])

    #Add a new user id to the database
    def add(self, userType, userID):

        try:
            super().add("INSERT INTO user(type, user_id) \
                               VALUES(%s, %s)", (userType, userID))
        except:
            raise
        
        return self.getID((userType, userID))

    #Returns all fields
    def get(self, userType, userID):
        return self.getByID(self.getID((userType, userID)))

    #Returns user type
    def getType(self, id):
        return self.getFieldByID(id, "type")

    #Returns user_id
    def getUserID(self, id):
        return self.getFieldByID(id, "user_id")

    #Get all users by type
    def getByType(self, tid):
        return self.getFields(("*",), ("type",), (tid,))

    #Remove all user by type
    def removeByType(self, tid):
        for user in self.getByType(tid):
            self.remove(user[0])