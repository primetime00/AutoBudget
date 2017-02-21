from pywinauto import Application as AutoApp, findwindows, timings
from time import sleep, time
from ctypes import windll

from pywinauto.win32functions import SetForegroundWindow, ShowWindow, SetFocus, SetActiveWindow

class GUI:
    __instance = None
    def __new__(cls, *args, **kwargs):
        if GUI.__instance is None:
            GUI.__instance = object.__new__(cls)
            GUI.__instance.firstTime()
        return GUI.__instance

    def firstTime(self):
        self.browser = None
        self.currentWindow = None
#        dc = windll.user32.GetDC(0)
#        self.dpiX = windll.gdi32.GetDeviceCaps(dc, 88)
#        self.dpiY = windll.gdi32.GetDeviceCaps(dc, 90)
#        windll.user32.ReleaseDC(0, dc)

    def positionBrowser(self):
        window = self.currentWindow
        info = window.WrapperObject()
        window.MoveWindow(0, 0, 1347, 1028)
        SetForegroundWindow(info.handle)
        ShowWindow(info.handle, 5)
        SetFocus(info.handle)
        SetActiveWindow(info.handle)

    def OpenBrowser(self, title, path):
        try:
            self.browser = AutoApp().connect(title_re=title)
            self.WaitForTitle(title, post_delay=0.1, timeout=20)
            return
        except:
            pass
        try:
            self.browser = AutoApp().start(path)
            sleep(3)
            self.browser = AutoApp().connect(title_re=title)
        except Exception as e:
            print(e)
            raise Exception("Could not open the browser")
        self.WaitForTitle(title, post_delay=1.5)
        self.positionBrowser()

    def WaitForTitle(self, title, timeout=10, post_delay=0.1):
        t0 = time()
        while time() - t0 < timeout:
            handles = findwindows.find_windows(title_re=title)
            if len(handles) > 0: #found it
                win = self.browser.window(handle=handles[0])
                try:
                    win.wait('exists enabled visible ready', timeout=timeout-(time()-t0))
                except timings.TimeoutError:
                    raise Exception("Could not find window with title: " + title)
                sleep(post_delay)
                self.currentWindow = win
                return win
        raise Exception("Could not find window with title: " + title)

    def ClickButton(self, name):
        self.currentWindow[name].Click()

    def ClickInputButton(self, name):
        self.currentWindow[name].ClickInput()

    def Select(self, name, value):
        self.currentWindow[name].Select(value)

    def CloseBrowser(self):
        self.currentWindow.type_keys('%{F4}')

    def ClickLocation(self, x, y):
        px = x
        py = y
        self.currentWindow.ClickInput(coords=(px, py))


