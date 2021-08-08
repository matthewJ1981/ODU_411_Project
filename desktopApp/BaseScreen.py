from tkinter import *
from PIL import ImageTk,Image 
from tkinter import messagebox
import threading
class Base:
    def __init__(self, root, backEnd):
        self._job = None
        self.root = root
        self.backEnd = backEnd

    def start(self, username):
        self.checkDatabase(username)

    def stop(self):
        if self._job is not None:
            self.root.after_cancel(self._job)
            self._job = None

    def checkDatabase(self, username):
        print("Checking database")

        #Pull database changes
        #self.backEnd.parentBackEnd.initParent()

        names = self.backEnd.checkRaisedHand(username)
        if names != []:
            messagebox.showinfo("Alert", str(names) + " needs help")

        self._job = self.root.after(5000, self.checkDatabase, username)

