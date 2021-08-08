from tkinter import *
import tkinter as tk
from tkinter import font as tkFont
from PIL import ImageTk,Image
from time import strftime 
#import pdb

from Macro.Listener import *
import Macro.MacroElement
from Macro.ExecuteMacro import *
from student.frontEnd.ChildEmbeddedBrowser import MainFrame

sys.path.insert(0, os.path.abspath("./student/frontEnd/"))
from childDashboard import *

class RecordMacroBrowser(tk.Frame):
    def __init__(self, root,backend,child):
        print('Entering RecordMacroBrowser.py')
        
        self.root = root
        self.backend = backend
        self.child = child
        
        print("current macro name",self.child.currentMacro.name)
        print("current macro activity id",self.child.currentMacro.activityId)
        print("current macro url",self.child.currentMacro.startUrl)

        
        self.childFrame = ChildDashboard(root,backend)
        self.childFrame.pack(fill=BOTH,expand=True)

        #initialize listener
        self.browserFrame = self.childFrame.centerFrame
        self.listener = Listener(self.browserFrame, root,child)

        #window info
        self.window = None
        self.font = font.Font(family="montserrat",size="16",weight="bold")
        self.tFrameX = root.winfo_x() +200
        self.tFrameY = root.winfo_y() +200
        
        self.buttonSetup()
        self.displayStartWindow()
        

    def displayStartWindow(self):
        self.createWindow()
        #self.window.geometry("+%d+%d" % (self.tFrameX, self.tFrameY))
        self.startInstructions = Label(self.window, font=self.font,text="When you are ready to begin, \n click the 'Start Recording' button below",borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff')
        self.startInstructions.grid(row=0,column=0,columnspan=3,padx=10,pady=10)

        self.startButton = Button(self.window, image=self.startImage, borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff', command=lambda:self.startRecording())
        self.startButton.grid(row=3,column=1, pady=10)


    def startRecording(self):
        self.browserFrame.navigate(self.child.currentMacro.startUrl)
        self.listener.start()
        print("recording started")
        self.notifyRecordingWindow()

        
    def notifyRecordingWindow(self):
        self.createWindow()
        self.window.geometry("+%d+%d" % (self.rootX+20, self.rootY+20))
        #Display recording icon
        rec1 = Image.open('Macro/ResourceImages/rImg.png') #open image
        resized = rec1.resize((100,100), Image.ANTIALIAS) #resize
        correctedImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage 
        self.recordingIcon = Label(self.window, image=correctedImage)
        self.recordingIcon.image = correctedImage #do this so image isnt lost in garbage collection
        self.recordingIcon.grid(column=0, row=0,rowspan=2)

        self.recordingnotification = Label(self.window, font=self.font,text="RECORDING IN PROGRESS",borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff')
        self.recordingnotification.grid(row=0,column=1,columnspan=2,padx=10,pady=10)

        #Display stop button
        self.stopButton = Button(self.window, image=self.stopImage, borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff', command=lambda:self.stopRecording())
        self.stopButton.grid(row=1,column=1, pady=10)

    def stopRecording(self):
        self.listener.stop()
        print("Recording stopped")
        self.listener.display()

        #reset browser
        self.childFrame.centerFrame.destroy()
        self.childFrame.show_browser(MainFrame)
        self.browserFrame = self.childFrame.centerFrame
            
        self.validateMacroWindow()


    def validateMacroWindow(self):
        self.createWindow()
        self.testInstructions = Label(self.window, font=self.font,text="The system will now test the macro. \n Please do not touch the mouse or keyboard \n until playback is complete",borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff')
        self.testInstructions.grid(row=0,column=0,columnspan=3,padx=10,pady=10)

        
        self.okButton = Button(self.window, image=self.okImage, borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff', command=lambda:self.startPlayback())
        self.okButton.grid(row=1,column=1, pady=10)

    def startPlayback(self):
        self.window.destroy()
        self.mList = self.listener.getMacro()
        ExecuteMacro(self, self.listener.macroElements,self.backend,self.child,True)
        

    def createWindow(self):
        if self.window:
            self.window.destroy()
        self.window = tk.Toplevel()
        self.window.attributes('-topmost','true')
        self.window.configure(bg='white')
        self.rootX = self.root.winfo_x()
        self.rootY = self.root.winfo_y()
        self.window.geometry("+%d+%d" % (self.rootX + 350, self.rootY + 350))

    def buttonSetup(self):
        photo = Image.open('student/frontEnd/images/okay.png') #open image
        resized = photo.resize((100, 35), Image.ANTIALIAS) #resize
        self.okImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage

        photo = Image.open('student/frontEnd/images/start.png') #open image
        resized = photo.resize((100, 35), Image.ANTIALIAS) #resize
        self.startImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage

        photo = Image.open('student/frontEnd/images/stop.png') #open image
        resized = photo.resize((100, 35), Image.ANTIALIAS) #resize
        self.stopImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage

            
        
    
