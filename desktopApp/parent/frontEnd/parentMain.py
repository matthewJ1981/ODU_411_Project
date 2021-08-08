from tkinter import *
from tkinter import font as tkFont
from PIL import ImageTk,Image

from parent.frontEnd import parentLogin, parentRegister

class ParentMain:
    def __init__(self, root, backEnd, onChildMachine = False):
        root.title("littleLEARNERS - Parent Main") 
        print("Entering Parent Main screen - /parent/frontEnd/parentMain.py")

        def loginClick(root):
            self.fm.destroy()
            parentLogin.ParentLogin(root, backEnd, onChildMachine)

        def registerClick(root):
            self.fm.destroy()
            parentRegister.ParentRegister(root, backEnd)

        # def homeClick(root):
        #     self.fm.destroy()
        #     #HomeScreen.HomeScreen(root, backEnd)
        #     parentMain.ParentMain(root, backEnd)

        def displayParentStartScreen():     
            self.fm = Frame(root)            
            self.fm.configure(background='white')
            
            # display buttons
            self.entryFont = tkFont.Font(size=25)

            #login Button
            photo = Image.open('assets/images/login.png') #open image
            resized = photo.resize((250, 65), Image.ANTIALIAS) #resize
            correctedImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage
            self.logInButton=Button(self.fm, image=correctedImage, borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff', command = lambda: loginClick(root))
            self.logInButton.image = correctedImage
            self.logInButton.grid(row=2,column=0,pady=(50,0), padx=10)

            #Resgister Button
            photo = Image.open('assets/images/register.png') #open image
            resized = photo.resize((250, 65), Image.ANTIALIAS) #resize
            correctedImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage
            self.registerButton=Button(self.fm, image=correctedImage, borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff', command = lambda: registerClick(root))
            self.registerButton.image = correctedImage
            self.registerButton.grid(row=2,column=1,pady=(50,0), padx=10)
            
            #logo image
            photo = Image.open('student/frontEnd/images/orangePic3.png') #open image
            resized = photo.resize((700, 340), Image.ANTIALIAS) #resize
            correctedImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage        
            self.pictureFrame = Label(self.fm, image=correctedImage, anchor=NE, bg="white")
            self.pictureFrame.image = correctedImage #do this so image isnt lost in garbage collection
            self.pictureFrame.grid(row=0,column=0, columnspan=2,pady=(0,50), padx=20, sticky=N)

            #self.logInButton= Button(self.fm, font=self.entryFont, width=15, text="Click here to login", command = lambda: loginClick(root))
            #self.logInButton.grid(row=0,column=0,pady=(100,0), padx=20)
            #self.registerButton= Button(self.fm, font=self.entryFont, width=15, text="Click here to register", command = lambda: registerClick(root))
            #self.registerButton.grid(row=0,column=1,pady=(100,0), padx=20)

            # backButton= Button(self.fm, text="Click to go back to Home Screen", command = lambda: homeClick(root))
            # backButton.grid(row=1,column=0,pady=(100,0), padx=20, columnspan = 2)

            self.fm.pack(expand=YES)


        displayParentStartScreen()

    