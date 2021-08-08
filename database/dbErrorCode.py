from dbTable import Table

class ErrorCode(Table):
    def __init__(self, cnx):
        super().__init__(cnx, "error_code", ("id", "code", "msg"), ("code",), [])

    #Add a new user id to the database
    def add(self, code, msg):

        try:
            super().add("INSERT INTO error_code(code, msg) \
                               VALUES(%s, %s)", (code, msg))
        except:
            raise
        
        return self.getID((code, ))

    #Returns all fields
    def get(self, code):
        return self.getByID(self.getID((code, )))

    #Returns user type
    def getCode(self, id):
        return self.getFieldByID(id, "code")

    def getMsg(self, id):
        return self.getFieldByID(id, "msg")