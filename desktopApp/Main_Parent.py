from tkinter import *

from screeninfo import get_monitors

from parent.frontEnd import parentMain
#from parent.frontEnd import parentWelcomeScreen
from parent.frontEnd.parentPortal.parentPortalMain import *
import os, sys
sys.path.insert(0, os.path.abspath("../backEnd"))
from backEnd import BackEnd
from os import path
from cefpython3 import cefpython as cef

class Main:
    def __init__(self):
        
        #self.backEnd = BackEnd()
        with BackEnd() as self.backEnd:

            print("Entering Main screen - Main_parent.py")
            self.root = Tk()
            self.root.geometry("1200x800")
            self.root.backEnd = self.backEnd
            self.root.title("littleLEARNERS") 
            self.root.configure(background='white')
            iconImage=PhotoImage(file="student/frontEnd/images/icon.png")
            self.root.iconphoto(False,iconImage)

            # full screen
            # self.root.attributes("-fullscreen", False)
            # self.w, self.h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
            # self.root.geometry("%dx%d" % (self.w, self.h))  

            #initialize browser
            assert cef.__version__ >= "55.3", "CEF Python v55.3+ required to run this"
            sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
            cef.Initialize(settings = {}, switches = {'disable-gpu': ""})
                    
                    
            if not path.exists(".ll"):
                parentMain.ParentMain(self.root, self.backEnd)
            else:
                #parentWelcomeScreen.parentWelcomeScreen(self.root, self.backEnd)
                self.backEnd.init()
                ParentPortalMain(self.root, self.backEnd)

            self.root.mainloop()

            cef.Shutdown()
        
        


if __name__ == '__main__':
    app = Main()  
