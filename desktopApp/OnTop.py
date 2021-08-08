from tkinter import *

from screeninfo import get_monitors

from parent.frontEnd import parentMain
#from parent.frontEnd import parentWelcomeScreen
from parent.frontEnd.parentPortal.parentPortalMain import ParentPortalMain
import os, sys
sys.path.insert(0, os.path.abspath("../backEnd"))
from backEnd import BackEnd
from os import path
from cefpython3 import cefpython as cef
from selenium import webdriver
import threading as t

def browser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=800,600')
    #chrome_options.add_argument('--headless')
    #chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)

    driver.get('https://portal.odu.edu/')
    driver.implicitly_wait(10)
    login = driver.find_element_by_xpath('//*[@id="side-menu"]/li[2]/button')
    login.click()
   
def app():
    app = Main()  
    
class Main:
    def __init__(self):
        #initialize browser
        # assert cef.__version__ >= "55.3", "cef python v55.3+ required to run this"
        # print("excepthook")
        # sys.excepthook = cef.excepthook  # to shutdown all cef processes on error
        # print("initialize")
        # cef.initialize()
        self.backEnd = BackEnd()
        

        print("Entering Main screen - Main_parent.py")
        self.root = Tk()
        def func(root):
            self.root.attributes('-topmost', True)
            self.root.update()
            #root.lift()
            root.after(100, func, root)
        self.root.backEnd = self.backEnd
        self.root.title("littleLEARNERS") 
        #self.root.configure(background='white')
        iconImage=PhotoImage(file="./assets/images/orange.png")
        self.root.iconphoto(False,iconImage)

        # full screen
        self.root.attributes("-fullscreen", False)
        #self.w, self.h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.w, self.h = 400, 800
        self.root.geometry("%dx%d+%d+%d" % (self.w, self.h, w - self.w, h - self.h))  
                  
        func(self.root)
        if not path.exists(".ll"):
            parentMain.ParentMain(self.root, self.backEnd)
        else:
            #parentWelcomeScreen.parentWelcomeScreen(self.root, self.backEnd)
            self.backEnd.init()
            ParentPortalMain(self.root, self.backEnd)

        
        self.root.mainloop()


if __name__ == '__main__':
    t1 = t.Thread(target = browser)
    t2 = t.Thread(target = app)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    
    
