

class Child:
    def __init__(self):
        self.name = None
        self.id = None
        self.imgPath = None
        self.parentId = None
        self.index = None
        self.currentMacro = None
        self.parentPlayback = False
        self.macros = []
        self.masterMacroElements = []
        self.classes = []
        self.activities = []
        self.scheduleItems = []

    def setup(self,backend,childID):
        self.id = childID
        self.index = 0
        #Get basic child info
        children = backend.parent.getChildren()
        for c in children:
            self.classes = []
            self.activities = []
            self.scheduleItems = []
            if c.id == childID:
                self.name = c.getName()
                self.imgPath = c.getImage()
                dbMacroElements = c.getMacroElements()
                self.classes = c.getClasses()
                break
            self.index += 1
        print(self.id, self.index,self.imgPath) #debug
        for cl in self.classes:
            self.activities.extend(cl.getActivities())
        for a in self.activities:
            print('actvity name:',a.name,'activity url',a.url)
            temp = a.getScheduleItems()
            self.scheduleItems.extend(temp)
            
            

        #Get list of child's macros
        self.macroNames = []
        tempElementList = []
        for e in dbMacroElements:
            t = MacroElement()
            t.id = e.id
            t.macroName = e.macroName
            t.orderNum = e.orderNum
            t.url = e.url
            t.hasInput = e.hasInput
            t.input = e.input
            t.imgPath = e.imgPath
            t.x = e.x
            t.y = e.y
            t.actID = e.activityID
            tempElementList.append(t)
            self.masterMacroElements.append(t)
            
            if e.getMacroName() not in self.macroNames:
                self.macroNames.append(e.macroName)
                tempMacro = Macro()
                tempMacro.name = e.macroName
                tempMacro.activityId = e.activityID
                self.macros.append(tempMacro)
        print(self.name + "'s macros:",self.macroNames) #debug
        

        for e in tempElementList:
            e.display()

        #Sort the list of macro elements into appropriate macro containers
        for m in self.macros:
            for e in tempElementList:
                if e.macroName == m.name:
                    m.elements.append(e)

        print('display elements when init child')
        for m in self.macros:
            m.elements.sort(key=lambda x: x.orderNum)
            print(m.name + ':')
            for s in m.elements: #debug
                s.display()


class Macro:
    def __init__(self):
        self.name = None
        self.startUrl = None
        self.activityId = None
        self.elements = []


class MacroElement(object):
    def __init__(self):
        self.id = None
        self.macroName = None
        self.orderNum = None
        self.url = None
        self.hasInput = False
        self.input = ''
        self.imgPath = None
        self.x = None
        self.y = None
        self.actID = None

    def display(self):
        print('Macro name: ',self.macroName)
        print('Activity ID: ',self.actID)
        print('orderNum: ',self.orderNum)
        print('url: ',self.url)
        print('hasInput: ',self.hasInput)
        print('input: ',self.input)
        print('imgPath: ',self.imgPath)
        print('x: ',self.x)
        print('y: ',self.y, '\n')

    def initialize(self):
        self.macroName = ""
        self.actID = ""
        self.orderNum = 0
        self.url = ""
        self.hasInput = False
        self.input = ""
        self.imgPath = ""
        self.x = 0
        self.y = 0