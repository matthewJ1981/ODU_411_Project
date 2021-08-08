from tkinter import *
import tkinter as tk
from tkinter import font as tkfont
from pynput import mouse, keyboard
import cv2
import pyautogui
from Macro.MacroElement import *
#from Macro.EmbeddedBrowser import *
import os, sys
###
#sys.path.insert(0, os.path.abspath("../backEnd"))
#from backEnd import BackEnd
####

class ErrorWindow:
    def __init__(self, key):
        self.key = key


class Listener:

    def __init__ (self,browser, root,child):
        self.root = root
        self.browser = browser
        self.child = child
        self.keyListener= keyboard.Listener(on_press=self.keyPress)
        self.mListener = mouse.Listener(on_click=self.mousePress)
        self.macroName = self.child.currentMacro.name
        self.actID = self.child.currentMacro.activityId
        self.macroElements = self.child.currentMacro.elements
        self.startURL = self.child.currentMacro.startUrl

    #start keyboard listener
    def startKey(self):
        self.keyListener.start()

    #start mouse listener
    def startMouse(self):
        self.mListener.start()

    def start(self):
        self.startKey()
        self.startMouse()
        self.macroElements.append(MacroElement())

    def createNewElement(self,x,y):
        self.macroElements[-1].macroName = self.macroName
        self.macroElements[-1].actID = self.actID
        self.macroElements[-1].orderNum = len(self.macroElements) - 1
        if len(self.macroElements) == 1:
            self.macroElements[-1].url = self.startURL
        else:
            self.macroElements[-1].url = self.browser.getURL()
            print('url during recording:',self.macroElements[-1].url)
        self.macroElements[-1].x = x
        self.macroElements[-1].y = y
       

    
    #Error if special key is used during recording
    def notifyForbiddenKey(self, fkey):
        self.font = font.Font(family="montserrat",size="16",weight="bold")
        self.errorWindow = tk.Toplevel()
        self.errorWindow.attributes('-topmost', 'true')
        self.errorWindow.configure(bg='white')
        self.tFrameX = self.root.winfo_x()
        self.tFrameY = self.root.winfo_y()
        self.errorWindow.geometry("+%d+%d" % (self.tFrameX + 20, self.tFrameY + 20))
        #self.dispKey = format(key)
        self.startInstructions = tk.Message(
            self.errorWindow,
            justify="left",
            font=self.font,
            bg='white',
            text='Warning: special key {} was pressed. ' 
                "Special keys are not allowed. \n\n"
                "This key was discarded, but recording is still in progress. \n"
                "Please continue without using special keys".format(fkey),
            width = 700).grid(row=0,column=0,columnspan=3)
        self.errorWindow.after(10000,lambda: self.errorWindow.destroy())

    #Save keyboard input to the current macro element
    def keyPress(self, key):
        keyIndex = len(self.macroElements)-2
        print(key,' was pressed')
        # Stop listener if escape key is pressed
        newInput = ''
        if key == keyboard.Key.esc:
            self.stop()
        else:
            if key != keyboard.Key.shift:
                if key == keyboard.Key.backspace:
                    newInput = self.macroElements[keyIndex].input[:-1]
                elif key == keyboard.Key.space:
                    newInput = self.macroElements[keyIndex].input + ' '
                else:
                    try:
                        newInput = self.macroElements[keyIndex].input + str(key.char)
                    except:
                        self.notifyForbiddenKey(key)            
            #store the pressed key to end of input string
            if newInput:
                if self.macroElements[keyIndex].hasInput == False:
                    self.macroElements[keyIndex].hasInput = True
                self.macroElements[keyIndex].input = newInput

        
    

    def mousePress(self, x, y, button, pressed):##############################################
        if button == mouse.Button.left:
            if pressed:
                self.createNewElement(x,y)
                #save picture of element
                #self.createElementPic(x,y)
                print("new element created: step ", len(self.macroElements)-1)
                self.display()
                self.macroElements.append(MacroElement())
                
    
    

    def stop(self):
        self.macroElements.pop() #remove elements created when "Stop recording" button was clicked
        self.macroElements.pop()
        self.keyListener.stop()
        self.mListener.stop()
        self.macroElements[-1].url = self.browser.getURL()
        if not self.macroElements:
            assert (self.macroElements)
            self.noElementsError()
        

    def display(self):
        print('list of elements:')
        for e in self.macroElements:
            e.display()
        print('-----------------------------------------------------------------------')

    #def takeSS(cElement):
        # print ('screenshot taken')
        # self.im2 = pyautogui.screenshot(region=(x-75,y-75, 150, 150))
        # self.im2.save('../Macro/screens.png')

    def getMacro(self):
        return self.macroElements

    #save macro to database
    def saveMacro(self):
        
        self.children = self.root.backEnd.parent.getChildren()
        
        self.currentChild = self.children[0]
        for m in self.macroElements:
            self.currentChild.addMacroElement(m.orderNum, 0,m.macroName,m.url,
                                                                    m.hasInput,m.input,m.imgPath,'',m.x,m.y)

    def noElementsError(self):
        print("Warning, no elements for macro!")

        
        
        
    





    
