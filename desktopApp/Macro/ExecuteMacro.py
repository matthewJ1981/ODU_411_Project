#basic macro execution algorithm(before images are added):
        #for each element:
        #    mouse to element.x,element.y
        #    click mouse
        #    if element.hasInput
        #        enter  enter element.input

        #macroelement class is in Macro->MacroElement.py

from tkinter import *
import tkinter as tk
from tkinter import font as tkfont
from PIL import *
from PIL import ImageTk,Image
from cefpython3 import cefpython as cef
import pyautogui
import time
import os
import sys
import threading
import inspect
pyautogui.FAILSAFE = False
from pynput.mouse import Button,Controller
pyautogui.PAUSE = 0.5
from parent import frontEnd
#sys.path.insert(0, os.path.abspath("./parent/frontEnd/parentPortal"))
from parent.frontEnd.parentPortal.parentPortalMain import *
import pathlib



#import Macro.MacroMenu
#from Macro.EmbeddedBrowser import *
from Macro.MacroElement import *
sys.path.insert(0, os.path.abspath(""))
pyautogui.PAUSE = 0

class ExecuteMacro():
    def __init__(self, parent, eList,backend,child,recording):
        print('Entering ExecuteMacro.py')
        
        parent.root.geometry("1400x800")
       
        #passing the browser and frames of the student browser page
        #self.parent = parent
        self.child = child
        print("current macro name",self.child.currentMacro.name)
        print("current macro activity id",self.child.currentMacro.activityId)
        print("current macro url",self.child.currentMacro.startUrl)
        self.root = parent.root
        #root = parent.root
        self.backend = backend
        self.recording = recording #bool
        self.window = None
        self.font = font.Font(family="montserrat",size="16",weight="bold")
        self.infoFont = font.Font(family="montserrat",size="11",weight="bold")

        self.elementList = eList #list of macroelements
        self.lastElement = self.elementList[-1]
        self.macroName = self.elementList[0].macroName
        self.clickIsNext = True
        self.currentEl = 0
        self.rootX = self.root.winfo_x()
        self.rootY = self.root.winfo_y()

        if recording:
            try:
                self.browser = parent.browserFrame
            except:
                raise
        else:
            try:
                self.browser = parent.centerFrame
            except:
                raise
        self.browserX = self.browser.winfo_rootx()
        self.browserY = self.browser.winfo_rooty()

        #hacky fix for macro screen sizes bug
        #if not self.child.parentPlayback:
         #   if not self.recording:
          #      parent.root.geometry('1400x795')
        print('browser height:',self.browser.winfo_height(),"width:",self.browser.winfo_width())


        self.buttonImageSetup()
        self.root.after(100,lambda:self.browser.navigate(self.elementList[0].url)) #go to the starting URL

        #Notify macro execution window
        self.createWindow()
        self.window.geometry("+%d+%d" % (self.rootX + 20, self.rootY + 20))
        self.macroInProgress = Label(self.window, font=self.font,text="Macro Playback in Progress",borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff')
        self.macroInProgress.pack(padx=10,pady=10)
        self.macroInProgress2 = Label(self.window, font=self.infoFont,text="Please don't touch the mouse or keyboard while the macro is playing.",borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff')
        self.macroInProgress2.pack(padx=10,pady=10)

        self.root.after(5000,lambda:self.startRecordingExecution(self.root))
        

    def endExecution(self,root):
        endURL = self.browser.getURL()
        print('End url =',self.browser.getURL())
        #if endURL == self.elementList[-1].url:
        if self.recording:
            self.displaySavePrompt(root)
        else:
            if not self.child.parentPlayback:
                self.backend.navSuccess()
            self.createWindow()
            self.notifySucessLabel = Label(self.window, font = self.font,text="Execution Successful!",borderwidth = 0, bg='#ffffff', highlightthickness=1, activebackground='#ffffff').grid(row=0,column=0,padx=10,pady=10)
            self.okButton = Button(self.window, image=self.okImage, borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff', command=lambda:self.destroyWindow()).grid(row=1,column=0, pady=10)
        #else:
                #   if not self.child.parentPlayback:
                #      self.backend.navFailed()
                #self.wrongURLError()
            

        

    def displaySavePrompt(self,root):
        self.createWindow()
        self.successLabel = Label(self.window, font = self.font,text="Testing successful!",borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff').grid(row=0,column=1,columnspan=2,padx=10,pady=10)
        #Display save button
        self.saveButton = Button(self.window, image=self.saveImage,text='Save Macro', borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff', command=lambda:self.saveMacro(root)).grid(row=1,column=1, pady=10)
        self.discardButton = Button(self.window, image=self.discardImage,text='Discard Macro', borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff', command=lambda:self.discardMacro()).grid(row=1,column=2, pady=10)

    def saveMacro(self,root):
        print('save macro function')
        
        for e in self.elementList:
            try:
                self.backend.parent.children[self.child.index].addMacroElement(e.orderNum, self.child.currentMacro.activityId, e.macroName,e.url, e.hasInput,e.input,e.imgPath,None,e.x,e.y)
            except:
                raise

        classes = self.backend.parent.children[self.child.index].getClasses()
        activities = []
        for c in classes:
            activities.extend(c.getActivities())
        for a in activities:
            if a.id == self.child.currentMacro.activityId:
                try:
                    a.setHasMacro(True)
                except:
                    raise
        
        print('end save macro function')

        

        #debug
        dbElements = self.backend.parent.children[self.child.index].getMacroElements()
        elements = []
        for e in dbElements:
            el = MacroElement()

            el.macroName = e.macroName
            el.orderNum = e.orderNum
            el.url = e.url
            el.hasInput = e.hasInput
            el.input = e.input
            el.imgPath = e.imgPath
            el.x = e.x
            el.y = e.y
            el.actID = e.activityID
            elements.append(el)

        for e in elements:
            e.display()

        #notification of save
        self.createWindow()

        self.notifySaveLabel = Label(self.window, font=self.font,text="Macro Saved!",borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff')
        self.notifySaveLabel.grid(row=0,column=0,padx=10,pady=10)
        self.okButton = Button(self.window, image=self.okImage,  borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff', command=lambda:self.destroyWindow())
        self.okButton.grid(row=1,column=0, pady=10)

        

    def discardMacro(self):
        self.window.destroy()
        for e in self.elementList:
            if os.path.exists(e.imgPath):
              os.remove(e.imgPath)
        self.createWindow()

        self.notifyDiscardedLabel = Label(self.window, font=self.font,text="Macro Discarded.",borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff')
        self.notifyDiscardedLabel.grid(row=0,column=0,padx=10,pady=10)
        self.okButton = Button(self.window, image=self.okImage,  borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff', command=lambda:self.destroyWindow())
        self.okButton.grid(row=1,column=0, pady=10)


    def destroyWindow(self):
        self.child.currentMacro = None
        if self.window:
            self.window.destroy()
        if self.recording:
            self.root.destroy()
        if self.child.parentPlayback:
            self.root.destroy()
        

    def startRecordingExecution(self, root):
        def executeMacro():
            print (len(inspect.stack()))
            if  self.currentEl >= len(self.elementList):
                self.endExecution(root)
                pass
            else:
                if self.clickIsNext:
                    print('going to click for stepnum: ',str(self.elementList[self.currentEl].orderNum))
                    
                    #if self.mouseInFrame:
                     #   self.leaveFrame()
                    #else:
                    imgPath = self.getElementImagePath(self.currentEl)
                        
                    try:
                        xCoord, yCoord = pyautogui.locateCenterOnScreen(imgPath) #locate the element on the screen
                    except:
                        try: 
                            print("2nd attempt to find element")
                            self.after(500,lambda:xCoord, yCoord = pyautogui.locateCenterOnScreen(imgPath))
                        except:
                            try:
                                print('3rd attempt to find element')
                                self.after(1000,lambda:xCoord, yCoord = pyautogui.locateCenterOnScreen(imgPath))
                            except:
                                try:
                                    print('4th attempt to find element')
                                    self.after(250,lambda:xCoord, yCoord = pyautogui.locateCenterOnScreen(imgPath))
                                except:
                                    try:
                                        print('5th attempt to find element')
                                        self.after(50,lambda:xCoord, yCoord = pyautogui.locateCenterOnScreen(imgPath))
                                    except:
                                        self.imageNotFoundError()
                                        return False

                    print('attempting to move') 
                    pyautogui.moveTo(xCoord, yCoord, .5) #move mouse to the element
                    print('moved to coordinate, clicking')
                    pyautogui.click() #click on the element
                    print('clicked')
                    if self.elementList[self.currentEl].hasInput:
                        self.clickIsNext = False
                    else:
                        self.currentEl = self.currentEl + 1
                        self.root.after(200,lambda:self.leaveFrame())
                    
                #Enter keyboard input:
                else:
                    print('going to keyboard input for stepnum: ',str(self.elementList[self.currentEl].orderNum))
                    if self.elementList[self.currentEl].hasInput:
                        print('element has input')
                        pyautogui.write(self.elementList[self.currentEl].input)
                    self.clickIsNext = True
                    self.currentEl = self.currentEl + 1
                    self.root.after(200,lambda:self.leaveFrame())

                
                root.after(3000,lambda:executeMacro())
        root.update()
        root.after(1000,lambda:self.leaveFrame())
        root.after(3000,lambda:executeMacro())
        root.update()


    def leaveFrame(self):
        print('mouse in frame, moving')
        pyautogui.moveTo(self.browserX+100,self.browserY) #move mouse out of the way to prevent mouse hover events during screenshot
        pyautogui.click()
        self.mouseInFrame = False

    #If recording, saves screenshot of element
    #Returns the saved image path
    def getElementImagePath(self,currentEl):
        if self.recording:
            tempImgPath = './Macro/MacroImages/' + str(self.child.id) + self.macroName + str(self.elementList[currentEl].orderNum) + '.png' #create unique image path to store element image
            if os.path.exists(tempImgPath):
                for i in range(0,30):
                    removePath = './Macro/MacroImages/' + str(self.child.id) + self.macroName + str(i) + '.png'
                    if os.path.exists(removePath):
                        os.remove(removePath)
            print('tempImgPath',tempImgPath)
            print('working dir path',pathlib.Path().absolute())
            elementImage = pyautogui.screenshot(region=(self.elementList[currentEl].x-100, self.elementList[currentEl].y-100,200,200)) #capture and save image of element being clicked
            if not os.path.exists('./Macro/MacroImages'):
                os.makedirs('./Macro/MacroImages')
            elementImage.save(tempImgPath)
            self.elementList[currentEl].imgPath = tempImgPath
        return self.elementList[currentEl].imgPath
    #*****Add error handling***


    #Error handling
    def imageNotFoundError(self):
        
        print("image not found")
        self.createWindow()
        if self.recording:
            self.recElementError = Label(self.window, font=self.font,text="Error: the system could not find the element. Please try recording again.",borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff')
            self.recElementError.grid(row=0,column=0,padx=10,pady=10)
            self.okButton = Button(self.window, image=self.okImage, borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff', command=lambda:self.discardMacro())
            self.okButton.grid(row=1,column=0, pady=10)
        elif self.child.parentPlayback:
            self.recElementError = Label(self.window, font=self.font,text="Error: the system could not find the element. Please delete the macro and record again.",borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff')
            self.recElementError.grid(row=0,column=0,padx=10,pady=10)
            self.okButton = Button(self.window, image=self.okImage, borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff', command=lambda:self.destroyWindow())
            self.okButton.grid(row=1,column=0, pady=10)
        else:
            self.backend.navFailed()
            self.recElementError = Label(self.window, font=self.font,text="Oh No! Something broke! Contacting a parent for you",borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff')
            self.recElementError.grid(row=0,column=0,padx=10,pady=10)
            self.okButton = Button(self.window, image=self.okImage, borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff',command=lambda:self.destroyWindow())
            self.okButton.grid(row=1,column=0, pady=10)
            #trigger littleAssistant
            #trigger parent alert

    def wrongURLError(self):
        print("wrong url")
        self.createWindow()
        if self.recording:
            self.recElementError = Label(self.window, font=self.font,text="Error: navigation failure. Please try recording again.",borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff')
            self.recElementError.grid(row=0,column=0,padx=10,pady=10)
            self.okButton = Button(self.window, image=self.okImage, borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff', command=lambda:self.discardMacro())
            self.okButton.grid(row=1,column=0, pady=10)
        elif self.child.parentPlayback:
            self.recElementError = Label(self.window, font=self.font, text="Error: navigation failure. Please delete the macro and record again.",borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff')
            self.recElementError.grid(row=0,column=0,padx=10,pady=10)
            self.okButton = Button(self.window, image=self.okImage, borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff', command=lambda:self.destroyWindow())
            self.okButton.grid(row=1,column=0, pady=10)
        else:
            self.childURError = Label(self.window, font=self.font,text="Oh No! Something broke! Contacting a parent for you",borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff')
            self.childURLError.grid(row=0,column=0,padx=10,pady=10)
            self.okButton = Button(self.window, image=self.okImage, borderwidth = 0, bg='#ffffff', highlightthickness=0, activebackground='#ffffff')
            self.okButton.grid(row=1,column=0, pady=10)
            #trigger littleAssistant
            #trigger parent alert

        

    def createWindow(self):
        if self.window:
            self.window.destroy()
        self.window = tk.Toplevel()
        self.window.attributes('-topmost','true')
        self.window.configure(bg='white')
        self.rootX = self.root.winfo_x()
        self.rootY = self.root.winfo_y()
        self.window.geometry("+%d+%d" % (self.rootX + 350, self.rootY + 350))

    def buttonImageSetup(self):
        photo = Image.open('student/frontEnd/images/okay.png') #open image
        resized = photo.resize((100, 35), Image.ANTIALIAS) #resize
        self.okImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage

        photo = Image.open('student/frontEnd/images/discard_M.png') #open image
        resized = photo.resize((100, 35), Image.ANTIALIAS) #resize
        self.discardImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage

        photo = Image.open('student/frontEnd/images/save_M.png') #open image
        resized = photo.resize((100, 35), Image.ANTIALIAS) #resize
        self.saveImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage



        
        
