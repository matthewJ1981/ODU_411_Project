from tkinter import *
from tkinter import font as tkFont
from tkinter import messagebox
from PIL import ImageTk,Image 

###
import os, sys
sys.path.insert(0, os.path.abspath("../Macro"))

from MacroMenu import *
###

from parent.frontEnd import parentMain
from student.frontEnd import studentWelcomeScreen

class HomeScreen:
    def __init__(self, root, backEnd):

        print("Entering Home screen - /home/HomeScreen.py")

        def goToWelcomeScreen(user):
            self.fm.destroy()
            studentWelcomeScreen.StudentWelcomeScreen(root, user, backEnd)

        def parentClick():
            self.fm.destroy()
            parentMain.ParentMain(root, backEnd)

        def studentClick():
            user=''
            successfulLogIn=False
            files = [f for f in os.listdir('.') if os.path.isfile(f)]
            for f in files:
                if(f.endswith('.ll')):
                    user=f.replace('.ll','')
                    successfulLogIn=True

            if(successfulLogIn):
                goToWelcomeScreen(user)
            else:
                messagebox.showinfo(None, "Please have a parent log in")
            
        ###
        def macroClick():
            self.fm.destroy()
            MacroMenu(root)
        ###
        
        def displayHomeScreen(message):
            self.fm = Frame(root)

            # display logo
            self.img = Image.open("./assets/images/login_logo.png")
            self.resizedImg = self.img.resize((500,200), Image.ANTIALIAS)
            self.newImg = ImageTk.PhotoImage(self.resizedImg)
            self.logo = Label(self.fm, image=self.newImg, width= 500, height=200)
            self.logo.grid(row=0,column=0, columnspan = 2)
        

            self.entryFont = tkFont.Font(size=25)
            self.logInButton= Button(self.fm, font=self.entryFont, width=15, text="I am a Parent",command = lambda:parentClick())
            self.logInButton.grid(row=1,column=0,pady=(100,0), padx=20)
            self.logInButton= Button(self.fm, font=self.entryFont, width=15, text="I am a Student",command = lambda:studentClick())
            self.logInButton.grid(row=1,column=1,pady=(100,0), padx=20)
            
            ###
            self.logInButton= Button(self.fm, text="Macro",command = lambda:macroClick())
            self.logInButton.grid(row=1,column=2,pady=(100,0), padx=20)
            ###
            
            self.messageLabel = Label(self.fm,text=message)
            self.messageLabel.grid(row=2, column=2)
            
            self.fm.pack(expand=YES)
        
        displayHomeScreen("")
    

