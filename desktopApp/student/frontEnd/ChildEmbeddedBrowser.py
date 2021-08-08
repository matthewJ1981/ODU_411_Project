# ~~~Code taken from https://github.com/cztomczak/cefpython/tree/master/examples and modified~~~
# To add the embedded browser:
# self.embeddedbrowser = MainFrame(root)

from tkinter import *
import numpy as np
from cefpython3 import cefpython as cef
import cv2
import ctypes
import tkinter as tk
import sys
import os
import platform
import logging as _logging

from PIL import ImageTk,Image
import time
from time import strftime 

#Platforms
WINDOWS = (platform.system() == "Windows")
LINUX = (platform.system() == "Linux")

# Globals
settings = {}

# Constants
# Tk 8.5 doesn't support png images
IMAGE_EXT = ".png"
   

class MainFrame(tk.Frame):

    def __init__(self, root):
        cef.Initialize(settings=settings)
        self.browser_frame = None
        self.navigation_bar = None
        self.root = root
        self.currentURL = ''
        

        # Root
        tk.Grid.rowconfigure(root, 0, weight=1)
        tk.Grid.columnconfigure(root, 0, weight=1)

        # MainFrame
        tk.Frame.__init__(self, root)
        self.setup_icon()
        self.bind("<Configure>", self.on_configure)
        

        # NavigationBar
        self.navigation_bar = NavigationBar(self)
        self.navigation_bar.pack(fill=X)
        #self.navigation_bar.grid(row=0, column=0,
         #                        sticky=(tk.N + tk.S + tk.E + tk.W))
        #tk.Grid.rowconfigure(self, 0, weight=0)
        #tk.Grid.columnconfigure(self, 0, weight=0)

        # BrowserFrame
        self.browser_frame = BrowserFrame(self, self.navigation_bar)
        self.browser_frame.pack(fill=tk.BOTH,expand=True)
        #self.browser_frame.grid(row=1, column=0,
         #                       sticky=(tk.N + tk.S + tk.E + tk.W))
        #tk.Grid.rowconfigure(self, 1, weight=1)
        #tk.Grid.columnconfigure(self, 0, weight=1)

        # Pack MainFrame
        self.pack(fill=tk.BOTH, expand=tk.YES)

        

    def on_root_configure(self, _):
        if self.browser_frame:
            self.browser_frame.on_root_configure()

    def on_configure(self, event):
        if self.browser_frame:
            width = event.width
            height = event.height
            if self.navigation_bar:
                height = height - self.navigation_bar.winfo_height()
            self.browser_frame.on_mainframe_configure(width, height)

    def on_close(self):
        if self.browser_frame:
            self.browser_frame.on_root_close()
            self.browser_frame = None
        #else:
          #  self.master.destroy()
        manager = cef.CookieManager.GetGlobalManager()
        self.cookie_visitor = CookieVisitor()
        result = manager.VisitAllCookies(self.cookie_visitor)

    def get_browser(self):
        if self.browser_frame:
            return self.browser_frame.browser
        return None

    def get_browser_frame(self):
        if self.browser_frame:
            return self.browser_frame
        return None

    def setup_icon(self):
        resources = os.path.join(os.path.dirname(__file__), "resources")
        icon_path = os.path.join(resources, "tkinter"+IMAGE_EXT)
        if os.path.exists(icon_path):
            self.icon = tk.PhotoImage(file=icon_path)
            # noinspection PyProtectedMember
            self.master.call("wm", "iconphoto", self.master._w, self.icon)

    def navigate(self,tempURL):
        self.navigation_bar.load_url(tempURL)

    def getURL(self):
        return self.currentURL

class BrowserFrame(tk.Frame):

    def __init__(self, mainframe, navigation_bar):
        self.navigation_bar = navigation_bar
        self.closing = False
        self.browser = None
        tk.Frame.__init__(self, mainframe)
        self.mainframe = mainframe
        self.bind("<Configure>", self.on_configure)
        """For focus problems see Issue #255 and Issue #535. """
        self.focus_set()

    def embed_browser(self):
        window_info = cef.WindowInfo()
        rect = [0, 0, self.winfo_width(), self.winfo_height()]
        window_info.SetAsChild(self.get_window_handle(), rect)
        self.browser = cef.CreateBrowserSync(window_info,
                                             url="https://www.cs.odu.edu/~411orang/welcome/index.html", )
        assert self.browser
        self.browser.SetClientHandler(LifespanHandler(self))
        self.browser.SetClientHandler(LoadHandler(self))
        self.browser.SetClientHandler(FocusHandler(self))
        self.message_loop_work()

    def get_window_handle(self):
        if self.winfo_id() > 0:
            return self.winfo_id()
        else:
            raise Exception("Couldn't obtain window handle")

    def message_loop_work(self):
        cef.MessageLoopWork()
        self.after(10, self.message_loop_work)

    def on_configure(self, _):
        if not self.browser:
            self.embed_browser()

    def on_root_configure(self):
        # Root <Configure> event will be called when top window is moved
        if self.browser:
            self.browser.NotifyMoveOrResizeStarted()

    def on_mainframe_configure(self, width, height):
        if self.browser:
            if platform.system() == "Windows":
                ctypes.windll.user32.SetWindowPos(
                    self.browser.GetWindowHandle(), 0,
                    0, 0, width, height, 0x0002)
            elif platform.system() == "Linux":
                self.browser.SetBounds(0, 0, width, height)
            self.browser.NotifyMoveOrResizeStarted()

    def on_focus_in(self, _):
        #logger.debug("BrowserFrame.on_focus_in")
        if self.browser:
            self.browser.SetFocus(True)

    def on_focus_out(self, _):
        #logger.debug("BrowserFrame.on_focus_out")
        """For focus problems see Issue #255 and Issue #535. """
        if LINUX and self.browser:
            self.browser.SetFocus(False)

    def on_root_close(self):
        #logger.info("BrowserFrame.on_root_close")
        if self.browser:
            #logger.debug("CloseBrowser")
            self.browser.CloseBrowser(True)
            self.clear_browser_references()
        else:
            #logger.debug("tk.Frame.destroy")
            self.destroy()
            

    def clear_browser_references(self):
        # Clear browser references that you keep anywhere in your
        # code. All references must be cleared for CEF to shutdown cleanly.
        self.browser = None

    def getURL(self):
        return self.browser.GetUrl()

class LifespanHandler(object):

    def __init__(self, tkFrame):
        self.tkFrame = tkFrame

    def OnBeforeClose(self, browser, **_):
        manager = cef.CookieManager.GetGlobalManager().DeleteCookies("","")
        #Cef.GetGlobalCookieManager().DeleteCookies("", "")
   


class LoadHandler(object):

    def __init__(self, browser_frame):
        self.browser_frame = browser_frame

    def OnLoadStart(self, browser, **_):
        if self.browser_frame.master.navigation_bar:
            self.browser_frame.mainframe.doneLoading = False
            self.browser_frame.master.navigation_bar.set_url(browser.GetUrl())

    def OnLoadingStateChange(self, browser, is_loading, **_):
        """For detecting if page loading has ended it is recommended
        to use OnLoadingStateChange which is most reliable. The OnLoadEnd
        callback also available in LoadHandler can sometimes fail in
        some cases e.g. when image loading hangs."""
        if not is_loading:
            self.browser_frame.mainframe.currentURL = browser.GetUrl()
        

class CookieVisitor(object):
    def Visit(self, cookie, count, total, delete_cookie_out):
        delete_cookie_out[0] = True
        return True
        
        

class FocusHandler(object):
    """For focus problems see Issue #255 and Issue #535. """

    def __init__(self, browser_frame):
        self.browser_frame = browser_frame

    def OnSetFocus(self, source, **_):
        if platform.system() == "Linux":
            return False
        else:
            return True

    def OnGotFocus(self, **_):
        if platform.system() == "Linux":
            self.browser_frame.focus_set()


class NavigationBar(tk.Frame):

    def __init__(self, master):
        self.back_state = tk.NONE
        self.forward_state = tk.NONE
        self.back_image = None
        self.forward_image = None
        self.reload_image = None

        tk.Frame.__init__(self, master)
        resources = os.path.join(os.path.dirname(__file__), "resources")

        # Back button
        photo = Image.open('./student/frontEnd/images/back.png') #open image
        resized = photo.resize((30, 30), Image.ANTIALIAS) #resize
        correctedImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage
        self.back_button = Button(self, image=correctedImage, borderwidth = 0, highlightthickness=0, activebackground='#ffffff', command=self.go_back)
        self.back_button.image = correctedImage 
        self.back_button.grid(row=0, column=0)

        # Forward button
        photo = Image.open('./student/frontEnd/images/forward.png') #open image
        resized = photo.resize((30, 30), Image.ANTIALIAS) #resize
        correctedImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage
        self.forward_button = Button(self, image=correctedImage, borderwidth = 0, highlightthickness=0, activebackground='#ffffff', command=self.go_forward)
        self.forward_button.image = correctedImage        
        self.forward_button.grid(row=0, column=1)

        # Reload button
        photo = Image.open('./student/frontEnd/images/reload.png') #open image
        resized = photo.resize((30, 30), Image.ANTIALIAS) #resize
        correctedImage = ImageTk.PhotoImage(resized) #intialiaze as PhotoImage
        self.reload_button = Button(self, image=correctedImage, borderwidth = 0, highlightthickness=0, activebackground='#ffffff', command=self.reload)
        self.reload_button.image = correctedImage
        self.reload_button.grid(row=0, column=2)

        # Url entry
        self.url_entry = tk.Entry(self)
        self.url_entry.bind("<Return>", self.on_load_url)
        self.url_entry.bind("<Button-1>", self.on_button1)
        self.url_entry.grid(row=0, column=3,
                            sticky=(tk.N + tk.S + tk.E + tk.W))
        tk.Grid.rowconfigure(self, 0, weight=100)
        tk.Grid.columnconfigure(self, 3, weight=100)

        # Update state of buttons
        self.update_state()

    def go_back(self):
        if self.master.get_browser():
            self.master.get_browser().GoBack()

    def go_forward(self):
        if self.master.get_browser():
            self.master.get_browser().GoForward()

    def reload(self):
        if self.master.get_browser():
            self.master.get_browser().Reload()

    def set_url(self, url):
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, url)


    def on_load_url(self, _):
        if self.master.get_browser():
            self.master.get_browser().StopLoad()
            self.master.get_browser().LoadUrl(self.url_entry.get())

    def load_url(self, tempurl):
        if self.master.get_browser():
            self.master.get_browser().StopLoad()
            self.master.get_browser().LoadUrl(tempurl)
            


    def on_button1(self, _):
        self.master.master.focus_force()

    def update_state(self):
        browser = self.master.get_browser()
        if not browser:
            if self.back_state != tk.DISABLED:
                self.back_button.config(state=tk.DISABLED)
                self.back_state = tk.DISABLED
            if self.forward_state != tk.DISABLED:
                self.forward_button.config(state=tk.DISABLED)
                self.forward_state = tk.DISABLED
            self.after(100, self.update_state)
            return
        if browser.CanGoBack():
            if self.back_state != tk.NORMAL:
                self.back_button.config(state=tk.NORMAL)
                self.back_state = tk.NORMAL
        else:
            if self.back_state != tk.DISABLED:
                self.back_button.config(state=tk.DISABLED)
                self.back_state = tk.DISABLED
        if browser.CanGoForward():
            if self.forward_state != tk.NORMAL:
                self.forward_button.config(state=tk.NORMAL)
                self.forward_state = tk.NORMAL
        else:
            if self.forward_state != tk.DISABLED:
                self.forward_button.config(state=tk.DISABLED)
                self.forward_state = tk.DISABLED
        self.after(100, self.update_state)