from dbTable import Table

class MemberOf(Table):
    def __init__(self, cnx):
        super().__init__(cnx, "member_of", ("id","parent_id","bubble_id"),
         ("parent_id","bubble_id"), [("parent_id",), ("bubble_id",)])

    #Add new member of item for parentId and bubbleID
    def add(self, parentID, bubbleID):
        try:
            super().add("INSERT INTO member_of(parent_id, bubble_id) \
                               VALUES(%s, %s)", (parentID, bubbleID))
        except:
            raise
        
        return self.getID((parentID, bubbleID))

    #Get all fields by parentId and bubbleID
    def get(self, parentID, bubbleID):
        return self.getByID(self.getID((parentID, bubbleID)))

    #Get parent id by id
    def getParentID(self, id):
        return self.getFieldByID(id, "parent_id")
    
    #Get bubble id by id
    def getBubbleID(self, id):
        return self.getFieldByID(id, "bubble_id")

    #Get all parents in bubble bid
    def getByBubble(self, bid):
        return self.getFields(("*",), ("bubble_id",), (bid,))

    #Get all bubbles parent pid is in
    def getByParent(self, pid):
        return self.getFields(("*",), ("parent_id",), (pid,))

    #Remove all enrolled in by child
    def removeByParent(self, pid):
        for mo in self.getByParent(pid):
            self.remove(mo[0])

    #Remove all enrolled in by class
    def removeByBubble(self, bid):
        for mo in self.getByBubble(bid):
            self.remove(mo[0])