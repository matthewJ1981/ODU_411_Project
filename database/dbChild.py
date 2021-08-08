from dbTable import Table
from dbUser import User

class Child(Table):
    def __init__(self, cnx):
        super().__init__(cnx, "child", ("id","parent_id"), ("first_name", "age", "parent_id"), [("parent_id",)])

    #Add child to database for parent pid, return id of new child
    def add(self, name, age, pid, raisedHand = 0, navFailed = 0, skillLevel = 1, image = None):
        try:
            super().add("INSERT INTO child(first_name, age, raised_hand, nav_failed, skill_level, parent_id, image) \
                               VALUES(%s, %s, %s, %s, %s, %s, %s)", (name, age, raisedHand, navFailed, skillLevel, pid, image))
        except:
            raise
        
        id = self.getID((name, age, pid))
        return id

    #Get all fields by name, age, pid
    def get(self, name, age, pid):
        return self.getByID(self.getID((name, age, pid)))

    #Get name by child id
    def getName(self, id):
        return self.getFieldByID(id, "first_name")

    #Get age by child id
    def getAge(self, id):
        return self.getFieldByID(id, "age")

    #Get raised hand by child id
    def getRaisedHand(self, id):
        return self.getFieldByID(id, "raised_hand")

    #Get Nav failed by child id
    def getNavFailed(self, id):
        return self.getFieldByID(id, "nav_failed")

    #Get skill level by child id
    def getSkillLevel(self, id):
        return self.getFieldByID(id, "skill_level")

    #get parent id by child id
    def getParentID(self, id):
        return self.getFieldByID(id, "parent_id")
        
    #Get image
    def getImage(self, id):
        return self.getFieldByID(id, "image")

    #Set name as newValue for child id
    def setName(self, id, newValue):
        return self.setFieldByID(id, "first_name", newValue)

    #Set age as newValue for child id
    def setAge(self, id, newValue):
        return self.setFieldByID(id, "age", newValue)

    #Set raisedhand as newValue for child id
    def setRaisedHand(self, id, newValue):
        return self.setFieldByID(id, "raised_hand", newValue)

    #Set nav failed as newValue for child id
    def setNavFailed(self, id, newValue):
        return self.setFieldByID(id, "nav_failed", newValue)

    #Set skill level as newValue for child id
    def setSkillLevel(self, id, newValue):
        return self.setFieldByID(id, "skill_level", newValue)

    #Set image
    def setImage(self, id, newValue):
        return self.setFieldByID(id, "image", newValue)

    #Get all fields for all children with parent id pid
    def getByParent(self, pid):
        return self.getFields(("*",), ("parent_id",), (pid,))

    #Remove all child with parent id pid
    def removeByParent(self, pid):
        for child in self.getByParent(pid):
            self.remove(child[0])


