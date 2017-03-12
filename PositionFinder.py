from pywinauto import Application as AutoApp, findwindows, timings
from pywinauto.win32functions import SetForegroundWindow, ShowWindow, SetFocus, SetActiveWindow
import win32api
from pynput.mouse import Button, Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener, Key, KeyCode
from time import sleep, time
from PIL import ImageGrab, Image
import pyscreeze
import os
from Singleton import Singleton
from threading import Lock

basedir = os.path.abspath(os.path.dirname(__file__))
imagedir = basedir+'\\'+'images'
os.makedirs(imagedir, exist_ok=True)

try:
    browser = AutoApp().connect(title_re=".*Mozilla")
except:
    print("Can't find mozilla firefox")
    exit()


window = browser.top_window()
info = window.WrapperObject()
rect = info.rectangle()
oldX = -1
oldY = -1

try:
    window.MoveWindow(0,0, 1347, 1028)
    SetForegroundWindow(info.handle)
    ShowWindow(info.handle, 5)
    SetFocus(info.handle)
    SetActiveWindow(info.handle)
except Exception as e:
    print(e)

class Capture(Singleton):


    def firstTime(self, **kwargs):
        self.keys = []
        self.captureToggle = False
        self.lock = Lock()
        basedir = os.path.abspath(os.path.dirname(__file__))
        self.imagedir = basedir + '\\' + 'images'
        os.makedirs(self.imagedir, exist_ok=True)

    def on_click(self, x, y, button, pressed):
        with self.lock:
            if not self.captureToggle:
                return
            window = browser.top_window()
            info = window.WrapperObject()
            rect = info.rectangle()
            n_x = x-rect.left
            n_y = y-rect.top
            if n_x < 0 or n_y < 0:
                return
            if x > rect.right or y > rect.bottom:
                return
            if not pressed:
                return
            cap = ImageGrab.grab(bbox=(n_x-80, n_y-20, n_x+80, n_y+20))
            cap.save(imagedir+'\\cap.png')
            screen = ImageGrab.grab(bbox=(rect.left, rect.top, rect.right, rect.bottom))
            screen.save(imagedir + '\\screen.png')
            print(x-rect.left, y-rect.top, pressed)
            with self.lock:
                self.captureToggle = False

    def on_press(self, key):
        with self.lock:
            if key in self.keys:
                return
            self.keys.append(key)
            if len(self.keys) == 2 and Key.ctrl_r in self.keys and key == KeyCode.from_char('/'):
                print("YAY")
                self.captureToggle = True


    def on_release(self, key):
        with self.lock:
            if key not in self.keys:
                return
            self.keys.remove(key)

def on_click(x, y, button, pressed):
    Capture().on_click(x, y, button, pressed)

def on_press(key):
    Capture().on_press(key)

def on_release(key):
    Capture().on_release(key)


screen = Image.open(imagedir+"\\screen.png")
haystack = screen.load()
cap = Image.open(imagedir+"\\cap.png")
needle = cap.load()

# import datetime
# n1 = datetime.datetime.now()
# v = pyscreeze.locate(cap, screen, grayscale=True)
# print(pyscreeze.center(v))
# n2 = datetime.datetime.now()
# print(n2-n1)

mListener = MouseListener(on_click=on_click)
kListener = KeyboardListener(on_press=on_press, on_release=on_release)

#with MouseListener(on_click=on_click) as listener:
#    listener.join()

c = Capture()
mListener.start()
kListener.start()


mListener.join()
kListener.join()

#while 1:
#    x,y = win32api.GetCursorPos()
#    if x != oldX or y != oldY:
#        print(x-rect.left, y-rect.top)
#        oldY = y
#        oldX = x
