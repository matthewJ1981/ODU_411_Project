from tkinter import *
from tkinter import font as tkFont
from student.frontEnd.ChildEmbeddedBrowser import MainFrame

class ParentsBoard:
    def __init__(self, mainClass, backEnd,onclickMenu):
        print("      Entering Parent - parents board screen - /parent/frontEnd/dashboard/pages/parentsBoard.py")

        self.browserFrame = Frame(mainClass.rightFrame,bg='white')
        self.browserFrame.pack(fill=BOTH,expand=True)
        self.browser= MainFrame(self.browserFrame)
        self.browser.after(100,lambda:self.browser.navigate("http://411orang.cpi.cs.odu.edu/"))
        self.browser.pack(fill=BOTH,expand=True)

        

    