from tkinter import *
from cefpython3 import cefpython as cef
import os, sys

from Macro.MacroMenu import *

class Main():
    def __init__(self):

        #initialize browser
        #assert cef.__version__ >= "55.3", "CEF Python v55.3+ required to run this"
        #sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
        #cef.Initialize(settings = {}, switches = {'disable-gpu': ""})
        
        self.root = Tk()
        self.root.title("littleLEARNERS") 

        # full screen
        self.root.attributes("-fullscreen", False)
        self.w, self.h = self.root.winfo_screenwidth()/2, self.root.winfo_screenheight()-200
        self.root.geometry("%dx%d" % (self.w, self.h))               

        
        MacroMenu(self.root,"hello")

        self.root.mainloop()

        cef.Shutdown()

if __name__ == '__main__':
    app = Main() 