from tkinter import *
from tkinter import messagebox
from PIL import ImageTk,Image

from parent import frontEnd
from .parentPortal.parentPortalMain import ParentPortalMain
from parent.frontEnd import parentWelcomeScreen
from student.frontEnd import childMain

#import json

class ParentLogin:
    def __init__(self, root, backEnd, onChildMachine = False):
        root.title("littleLEARNERS - Parent Login") 
        print("  Entering Parent Login screen - /parent/frontEnd/parentLogin.py")

        def goBackClick():
            self.fm.destroy()
            frontEnd.parentMain.ParentMain(root, backEnd, onChildMachine)

        def goToParentDashBoard(username):
            self.fm.destroy()
            if onChildMachine:
                childMain.ChildMain(root, backEnd)
            else:
                ParentPortalMain(root, backEnd)
                # parentWelcomeScreen.parentWelcomeScreen(root, backEnd)

        def getLoginResponse(root, username, password):

            returnCode, returnMessage = backEnd.login(username, password)
            messagebox.showinfo(None, returnMessage)

            if returnCode == "000":        
                goToParentDashBoard(username)
            else:
                print(returnMessage)

        def displayParentLogin():
            self.fm = Frame(root)
            self.fm.configure(background='white')

            photo = Image.open('assets/images/login_icon.png') #open image
            resized = photo.resize((125, 125), Image.ANTIALIAS) #resize
            correctedImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage
            self.loginIcon=Label(self.fm, image=correctedImage,bg='#ffffff')
            self.loginIcon.image = correctedImage
            self.loginIcon.grid(row=0,column=0, columnspan=2,pady=(25,25), padx=10)
            
            # display user input
            self.userLabel= Label(self.fm,text="Username", bg='#ffffff', pady=10, padx=25, font = ('montserrat', 16, 'bold'))
            self.userLabel.grid(row=1,column=0)
            self.usernameEntry = Entry(self.fm)
            self.usernameEntry.grid(row=1,column=1)

            # display password input
            self.pwdLabel= Label(self.fm,text="Password", bg='#ffffff', pady=10, padx=25, font = ('montserrat', 16, 'bold'))
            self.pwdLabel.grid(row=2,column=0)
            self.passwordEntry = Entry(self.fm, show ="*")
            self.passwordEntry.grid(row=2,column=1)

            photo = Image.open('assets/images/login.png') #open image
            resized = photo.resize((200, 52), Image.ANTIALIAS) #resize
            correctedImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage
            self.logInButton=Button(self.fm, image=correctedImage, borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff', command = lambda: getLoginResponse(self.fm, self.usernameEntry.get(), self.passwordEntry.get()))
            self.logInButton.image = correctedImage
            self.logInButton.grid(row=3,column=0, columnspan=2,pady=(25,0), padx=10)

            photo = Image.open('assets/images/go_back.png') #open image
            resized = photo.resize((200, 52), Image.ANTIALIAS) #resize
            correctedImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage
            self.logInButton=Button(self.fm, image=correctedImage, borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff', command = lambda: goBackClick())
            self.logInButton.image = correctedImage
            self.logInButton.grid(row=4,column=0, columnspan=2,pady=(25,0), padx=10)

            # display buttons
            #self.enterButton= Button(self.fm, text = "Enter",command = lambda: getLoginResponse(self.fm, self.usernameEntry.get(), self.passwordEntry.get()))
            # self.enterButton= Button(self.fm, text = "Enter",command = lambda: getLoginResponse(self.fm, "p2", "12345678"))
            #self.enterButton.grid(row=3,column=0)
            #self.backButton= Button(self.fm, text="Click to go back", command = lambda: goBackClick())
            #self.backButton.grid(row=3,column=0)


            self.fm.pack(expand=YES)
        

        displayParentLogin()