class MacroElement():
    def __init__(self, In, db):
        self.updateMembers(In)
        self.db = db
        self.updates = []

    def updateMembers(self, In):
        (self.id, 
        self.orderNum,
        self.childID,
        self.activityID,
        self.macroName,
        self.url,
        self.hasInput,
        self.input,
        self.imgPath,
        self.img,
        self.x,
        self.y) = In

    def pushUpdates(self):
        #print("Macro Element pushUpdates")
        for table, index in self.updates:
            #print("Macro Element")

            if index == 'ordernNum':
                self.db.macroElement.setOrderNum(self.id, self.orderNum)
            elif index == 'macroName':
                self.db.macroElement.setMacroName(self.id, self.macroName)
            elif index == 'url':
                self.db.macroElement.setURL(self.id, self.url)
            elif index == 'hasInput':
                self.db.macroElement.setURL(self.id, self.hasInput)
            elif index == 'input':
                self.db.macroElement.setURL(self.id, self.input)
            elif index == 'imgPath':
                self.db.macroElement.setURL(self.id, self.imgPath)
            elif index == 'img':
                self.db.macroElement.setURL(self.id, self.img)
            elif index == 'x':
                self.db.macroElement.setURL(self.id, self.x)
            elif index == 'y':
                self.db.macroElement.setURL(self.id, self.y)

        self.updates = []

    def update(self, In = None):
        if self.id == -1:
            print("Invalid id")
            return
        if In == None:
            In = self.db.macroElement.getByID(self.id)

        print("Update: " + str(In))
        self.updateMembers(In)

    def setID(self, id):
        self.id = id
        
    def getID(self):
        return self.id

    def getOrderNum(self):
        return self.orderNum

    def getChildID(self):
        return self.childID

    def getActivityID(self):
        return self.activityID
    
    def getMacroName(self):
        return self.macroName

    def getUrl(self):
        return self.url

    def getHasInput(self):
        return self.hasInput

    def getInput(self):
        return self.input

    def getImgPath(self):
        return self.imgPath

    def getImg(self):
        return self.img
        
    def getX(self):
        return self.x
        
    def getY(self):
        return self.y

    def setOrderNum(self, newValue):
            self.orderNum = newValue
            self.updates.append(('macro_element', 'orderNum'))

    def setMacroName(self, newValue):
            self.macroName = newValue
            self.updates.append(('macro_element', 'macroName'))

    def setUrl(self, newValue):
            self.url = newValue
            self.updates.append(('macro_element', 'url'))

    def setHasInput(self, newValue):
            self.hasInput = newValue
            self.updates.append(('macro_element', 'hasInput'))

    def setInput(self, newValue):
            self.input = newValue
            self.updates.append(('macro_element', 'input'))
 
    def setImgPath(self, newValue):
            self.imgPath = newValue
            self.updates.append(('macro_element', 'imgPath'))

    def setImg(self, newValue):
            self.img = newValue
            self.updates.append(('macro_element', 'img'))

    def setX(self, newValue):
            self.x = newValue
            self.updates.append(('macro_element', 'x'))
        
    def setY(self, newValue):
            self.y = newValue
            self.updates.append(('macro_element', 'y'))

    def print(self):
        print("orderNum: " + str(self.orderNum))