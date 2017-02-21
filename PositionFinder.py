from pywinauto import Application as AutoApp, findwindows, timings
from pywinauto.win32functions import SetForegroundWindow, ShowWindow, SetFocus, SetActiveWindow
import win32api
from time import sleep, time

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
while 1:
    x,y = win32api.GetCursorPos()
    if x != oldX or y != oldY:
        print(x-rect.left, y-rect.top)
        oldY = y
        oldX = x
