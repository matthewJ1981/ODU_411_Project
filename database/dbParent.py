from dbTable import Table
from argon2 import PasswordHasher
from dbUser import User

class Parent(Table):
    time_cost = 16
    memory_cost = 2**15
    parallelism = 2
    hash_len = 32
    salt_len = 16
    def __init__(self, cnx):
        super().__init__(cnx, "parent", ("id","username"), ("username",), [])

    #Add a new parent to the database.  Username and email must be unique.  Password is hashed.
    #Returns id of new parent
    def add(self, username, password, email, firstName, lastName, phone = None, bubble = None):

        try:
            super().add("INSERT INTO parent(username, password, email_addr, first_name, last_name, phone) \
                               VALUES(%s, %s, %s, %s, %s, %s)", (username, self.hashPassword(password), email, firstName, lastName, phone))
        except:
            raise
        
        id = self.getID((username,))
        #user = User(self.cnx)
        #uid = user.add("Parent", id)
        #self.setFieldByID(id, "user_id", uid)
        return id

    #Returns all fields of parent with username
    def get(self, username):
        return self.getByID(self.getID((username,)))

    #Returns username by id
    def getUserName(self, id):
        return self.getFieldByID(id, "username")

    #Returns hashed password by id
    def getPassword(self, id):
        return self.getFieldByID(id, "password")

    #Returns email by id
    def getEmail(self, id):
        return self.getFieldByID(id, "email_addr")
    
    #Returns firstname by id
    def getFirstName(self, id):
        return self.getFieldByID(id, "first_name")

    #Returns lastname by id
    def getLastName(self, id):
        return self.getFieldByID(id, "last_name")

    # #Get user id
    # def getUserID(self, id):
    #     return self.getFieldByID(id, "user_id")

    #Get phone number
    def getPhoneNumber(self, id):
        return self.getFieldByID(id, "phone")

    #Hash and set new password
    def setPassword(self, id, newValue):
        return self.setFieldByID(id, "password", self.hashPassword(newValue))

    #Set email as newvValue for parent id
    def setEmail(self, id, newValue):
        return self.setFieldByID(id, "email_addr", newValue)

    #Set first name as newValue for parent id
    def setFirstName(self, id, newValue):
        return self.setFieldByID(id, "first_name", newValue)

    #Set last name as newValue for parent id
    def setLastName(self, id, newValue):
        return self.setFieldByID(id, "last_name", newValue)

    #Set phone as newValue for parent id
    def setPhoneNumber(self, id, newValue):
        return self.setFieldByID(id, "phone", newValue)

    # def getByUserID(self, uid):
    #     return self.getFields(("*",), ("user_id",), (uid,))

    #Remove all parents with user id
    def removeByUserID(self, uid):
        for parent in self.getByUserID(uid):
            self.remove(parent[0])

    #Hash password
    def hashPassword(self, password):
        argon2Hasher = PasswordHasher(time_cost = self.time_cost, memory_cost = self.memory_cost, 
                                      parallelism = self.parallelism, hash_len = self.hash_len, 
                                      salt_len = self.salt_len)
        return argon2Hasher.hash(password)

    #Checks password for username and compares with entered password
    def verifyPassword(self, username, password):
        argon2Hasher = PasswordHasher(time_cost = self.time_cost, memory_cost = self.memory_cost, 
                                      parallelism = self.parallelism, hash_len = self.hash_len, 
                                      salt_len = self.salt_len)
        try:           
            argon2Hasher.verify(self.getPassword(self.getID((username,))), password)
        except:
            return False
        else:
            return True

    # def remove(self, pid):
    #     Table.remove(super(Parent, self), pid)
    #     user = User(self.cnx)
    #     user.remove(user.getID(("Parent", pid)))
        
    #     return True

    # def removeAll(self):
    #     parents = self.getField("id")
    #     super().removeAll()
    #     user = User(self.cnx)
    #     for id in parents:
    #         user.remove(user.getID(("Parent", id)))

    #     return True