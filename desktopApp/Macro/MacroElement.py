
class MacroElement(object):
    def __init__(self):
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
