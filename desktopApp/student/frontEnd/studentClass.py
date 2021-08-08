import sys

class Student:

    def __init__(self, imageFile, firstName, lastName):
        #This will be replaced with functions to pull info from the database
        self.image = imageFile
        self.firstName = firstName
        self.lastName = lastName

    def setFirstName(self):
        return

    def setLastName(self):
        return

    def getFirstName(self):
        return self.firstName

    def getLastName(self):
        return self.getLastName

    def getImage(self):
        return self.image