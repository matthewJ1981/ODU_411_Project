from tkinter import *
from tkinter import font as tkFont
from PIL import ImageTk,Image 

#from home import HomeScreen
from parent.frontEnd import parentMain
from BaseScreen import Base

###
#import os, sys
#sys.path.insert(0, os.path.abspath("../Macro"))

#from Macro.MacroMenu import *
###

### random stuff
import random
import string

class parentWelcomeScreen(Base):
    def __init__(self, root, backEnd):
        super().__init__(root, backEnd)
        print("Entering Home screen - /parent/frontEnd/WelcomeScreen.py")

        backEnd.init()
        backEnd.parent.print()
        self.username = backEnd.parent.getUserName()
        
        #random kids
        def addChild():
            print("add child button was clicked in parent welcome screen(/parent/frontEnd/WelcomeScreen.py) ")
            letters = string.ascii_letters
            name = ''.join(random.choice(letters) for i in range(5))
            age = 5
            backEnd.parent.addChild(name, age)
            
        def Macro():
            self.fm.destroy()
            MacroMenu(root, backEnd)

        def logOutClick():
            self.fm.destroy()
            self.stop()
            #HomeScreen.HomeScreen(root, backEnd)
            backEnd.logOut()
            parentMain.ParentMain(root, backEnd)

        def displayWelcomeScreen(message):
            self.fm = Frame(root)

            scrollbar = Scrollbar(self.fm)

            # display logo
            self.img = Image.open("./assets/images/avatar.png")
            self.resizedImg = self.img.resize((450,450), Image.ANTIALIAS)
            self.newImg = ImageTk.PhotoImage(self.resizedImg)
            self.logo = Label(self.fm, image=self.newImg, width= 450, height=450)
            self.logo.grid(row=0,column=0)
        

            self.entryFont = tkFont.Font(size=25)

            self.messageLabel = Label(self.fm, font=self.entryFont, text = self.username + " Welcome to littleLEARNERS!!!")
            self.messageLabel.grid(row=1,column=0,pady=(50,0), padx=20)

            self.logInButton= Button(self.fm, width=15, text="Log Out",command = lambda:logOutClick())
            self.logInButton.grid(row=2,column=0,pady=(50,0), padx=20)
            
            self.macroButton= Button(self.fm, width=15, text="Macro",command = lambda:Macro())
            self.macroButton.grid(row=3,column=0,pady=(20,0), padx=20)

            self.addChild= Button(self.fm, width=15, text="add Child",command = lambda:addChild())
            self.addChild.grid(row=4,column=0,pady=(20,0), padx=20)

            self.fm.pack(expand=YES)
        
        displayWelcomeScreen("")

        self.start(self.username)

