from tkinter import *
from tkinter import messagebox
from PIL import ImageTk,Image

from parent import frontEnd

class ParentRegister:
    def __init__(self,root, backEnd):
        root.title("littleLEARNERS - Parent Register") 
        print("Entering Parent Register screen - /parent/frontEnd/parentRegister.py")

        def goToParentLogin():
            self.fm.destroy()
            frontEnd.parentLogin.ParentLogin(root, backEnd)

        def goBackClick():
            self.fm.destroy()
            frontEnd.parentMain.ParentMain(root, backEnd)

        def getRegisterResponse(username, password, email, firstName, lastName, phoneNumber):
            print("Enter button was clicked in Parent Register screen - /parent/frontEnd/parentRegister.py")
            
            #Tuple fields can be explicitly named
            responseCode, returnMessage = backEnd.register(username, password, email, firstName, lastName, phoneNumber)

            # returnCode = response[0]
            # returnMessage = response[1]
            
            messagebox.showinfo(None,returnMessage)

            if (responseCode == "000"):    
                print(returnMessage)
                goToParentLogin()  
            else:
                print(returnMessage)

        def displayParentRegister():
            self.fm = Frame(root)
            self.fm.configure(background='white')
            
            # user id
            self.user=Label(self.fm,text="Username", bg='#ffffff', pady=10, padx=25, font = ('montserrat', 16, 'bold'))
            self.user.grid(row=0,column=0)
            self.usernameEntry = Entry(self.fm)
            self.usernameEntry.grid(row=0,column=1)

            # password
            self.pas= Label(self.fm,text="Password", bg='#ffffff', pady=10, padx=25, font = ('montserrat', 16, 'bold'))
            self.pas.grid(row=1,column=0)
            self.passwordEntry = Entry(self.fm, show ="*")
            self.passwordEntry.grid(row=1,column=1)

            # email
            self.email= Label(self.fm,text="Email", bg='#ffffff', pady=10, padx=25, font = ('montserrat', 16, 'bold'))
            self.email.grid(row=2,column=0)
            self.emailEntry = Entry(self.fm)
            self.emailEntry.grid(row=2,column=1)

            # first name
            self.firstName= Label(self.fm,text="First Name", bg='#ffffff', pady=10, padx=25, font = ('montserrat', 16, 'bold'))
            self.firstName.grid(row=4,column=0)
            self.firstNameEntry = Entry(self.fm)
            self.firstNameEntry.grid(row=4,column=1)

            # last name
            self.lastName= Label(self.fm,text="Last Name", bg='#ffffff', pady=10, padx=25, font = ('montserrat', 16, 'bold'))
            self.lastName.grid(row=5,column=0)
            self.lastNameEntry = Entry(self.fm)
            self.lastNameEntry.grid(row=5,column=1)

            # phone number
            self.phoneNumber= Label(self.fm,text="Phone Number", bg='#ffffff', pady=10, padx=25, font = ('montserrat', 16, 'bold'))
            self.phoneNumber.grid(row=6,column=0)
            self.phoneNumberEntry = Entry(self.fm)
            self.phoneNumberEntry.grid(row=6,column=1)

            # registration button
            self.enterButton= Button(
                self.fm
                , text = "Enter"
                ,command = 
                    lambda: getRegisterResponse(
                        self.usernameEntry.get(), 
                        self.passwordEntry.get(), 
                        self.emailEntry.get(), 
                        self.firstNameEntry.get(), 
                        self.lastNameEntry.get(), 
                        self.phoneNumberEntry.get()
                    )
            )

            photo = Image.open('assets/images/register.png') #open image
            resized = photo.resize((200, 52), Image.ANTIALIAS) #resize
            correctedImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage
            self.register=Button(self.fm, image=correctedImage, borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff', command = 
                    lambda: getRegisterResponse(
                        self.usernameEntry.get(), 
                        self.passwordEntry.get(), 
                        self.emailEntry.get(), 
                        self.firstNameEntry.get(), 
                        self.lastNameEntry.get(), 
                        self.phoneNumberEntry.get()
                    ))
            self.register.image = correctedImage
            self.register.grid(row=7,column=0, columnspan=2,pady=(25,0), padx=10)

            photo = Image.open('assets/images/go_back.png') #open image
            resized = photo.resize((200, 52), Image.ANTIALIAS) #resize
            correctedImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage
            self.goBack=Button(self.fm, image=correctedImage, borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff', command = lambda: goBackClick())
            self.goBack.image = correctedImage
            self.goBack.grid(row=8,column=0, columnspan=2,pady=(25,0), padx=10)

            # self.enterButton.grid(row=7,column=0)
            # self.backButton= Button(self.fm, text="Click to go back", command = lambda: goBackClick())
            # self.backButton.grid(row=8,column=0)
            
            self.fm.pack(expand=YES)
        
        displayParentRegister()