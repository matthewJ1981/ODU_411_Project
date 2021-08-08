from pynput import mouse, keyboard
import pyautogui
import time
# class Listener:
#     #def __init__ (self, parent, currChild):
#     def __init__ (self, backEnd):
#         print("Listener")
#         self.startKey()
#         self.startMouse()
#         self.parent = parent
#         self.currChild = currChild

class Listener:
    def __init__ (self, backEnd):
        print("Listener")
        #self.startKey()
        self.startMouse()
        self.backEnd = backEnd
        self.buffer = ""
        self.prev = 0
        self.curr = 0
        self.minTime = 1
        self.timeLeft = self.minTime

    def tempKey(self, key):
        print(key,' was pressed')
        if key == keyboard.Key.enter:
            print("Enter")
            #self.backEnd.parent.getChildren()[self.backEnd.currChild].addInputData(self.backEnd.UTCNow(), None, None, self.buffer)
            buffer = ""
        else:
            try:
                self.buffer += (key.char)
            except:
                #print("Error" + str(key))
                #self.buffer += str(key)
                #print(self.buffer)
                pass
    

    #start keyboard listener
    def startKey(self):
        self.keyListener= keyboard.Listener(on_press=self.tempKey)
        self.keyListener.start()

    #start mouse listener
    def startMouse(self):
        self.mListener = mouse.Listener(on_click=self.clicked)
        self.mListener.start()

    def clicked(self, x, y, button, pressed):
        if button == mouse.Button.left and pressed:
            #print("Clicked")
            # self.curr = time.perf_counter()
            # if self.prev == 0:
            #     self.prev = self.curr
            # self.timeLeft -= self.curr - self.prev
            # print(self.timeLeft)
            # self.prev = self.curr
            # if self.timeLeft <= 0:
            #     self.timeLeft = self.minTime
            self.backEnd.parent.getChildren()[self.backEnd.currChild].addInputData(self.backEnd.formatAsStringMicro(self.backEnd.UTCNowMicro()), x, y, None)

        elif button == mouse.Button.right and pressed:
            print("Right")
            self.backEnd.parent.getChildren()[self.backEnd.currChild].addLogEntry(self.backEnd.formatAsString(self.backEnd.UTCNow()), 0)
            self.backEnd.parent.getChildren()[self.backEnd.currChild].setNavFailed(1)
            #self.backEnd.navFailed()
            #print(self.backEnd.getLogEntries())
        elif button == mouse.Button.middle and pressed:
            print("Middle")
            self.backEnd.parent.getChildren()[self.backEnd.currChild].setRaisedHand(1)
            #self.backEnd.navFailed()
            #print(self.backEnd.getLogEntries())

    def stop(self):
        self.keyListener.stop()
        self.mListener.stop()
        print('Listener stopped')
    





    
