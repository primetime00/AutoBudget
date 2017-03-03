from GUI import GUI

from Configuration import Configuration
from time import sleep
from Dates import Dates


class BankWeb:
    def __init__(self, bank, saveFile):
        self.bank = bank
        self.user = bank["login"]
        self.password = bank["password"]
        self.signout = bank["signout"]
        self.site = bank["address"]
        self.userDate = None
        self.transactions = []
        self.UI = GUI()
        self.shouldClose = True
        self.saveFile = saveFile
        self.processMap = [
            (self.OpenSite, "OpenSite"),
            (self.Login, "Login"),
            (self.NavigateToTransactions, "NavigateToTransactoins"),
            (self.SaveTransactions, "SaveTransactions"),
            (self.Logout, "Logout")
        ]

    def Run(self, start=0, end=-1, browser=False, userDate=Dates.empty()):
        self.userDate = userDate
        if browser:
            try:
                self.UI.OpenBrowser(Configuration().getBrowserTitle(), Configuration().getBrowserPath())
            except Exception as e:
                raise Exception("OpenBrowser: " + str(e))

        if end == -1:
            end = len(self.processMap)
        else:
            self.shouldClose = False

        for i in range(start, end):
            func, error = self.processMap[i]
            try:
                func()
            except Exception as e:
                raise Exception(error+": " + str(e))

        if not self.shouldClose:
            return
        if browser:
            try:
                self.UI.CloseBrowser()
            except Exception as e:
                raise Exception("CloseBrowser: " + str(e))

    def OpenSite(self):
        print("Need Defs")
        raise Exception("OpenSite Needs Definition")

    def Login(self):
        print("Need Defs")
        raise Exception("Login Needs Definition")

    def NavigateToTransactions(self):
        print("Need Defs")
        raise Exception("NavigateToTransactions Needs Definition")

    def SaveTransactions(self):
        self.Press('^s')
        self.Wait("Save As", timeout=4)
        self.ClickInput(u'9')
        sleep(0.2)
        self.Select(u'10', u'Web Page, complete (*.htm;*.html)')
        self.Press("{ENTER}")
        sleep(0.2)
        self.ClickInput(u'5')
        sleep(0.2)
        self.Press('{DEL}')
        sleep(0.2)
        self.Type(self.saveFile)
        sleep(0.8)
        self.Click(u'&Save')
        sleep(0.8)
        try:
            self.Wait("Confirm Save As", timeout=2, post_delay=0.5)
            self.Click(u'&Yes')
        except:
            pass
        sleep(4)

    def Logout(self):
        print("Need Defs")
        raise Exception("Logout Needs Definition")


    def Press(self, str, pause=None):
        self.UI.currentWindow.type_keys(str, pause=pause)

    def Type(self, str):
        self.UI.currentWindow.type_keys(str, with_spaces=True)

    def Wait(self, title, timeout=10, post_delay=0.1):
        self.UI.WaitForTitle(title, timeout=timeout, post_delay=post_delay)

    def Click(self, name):
        self.UI.ClickButton(name)

    def ClickInput(self, name):
        self.UI.ClickInputButton(name)

    def Select(self, name, value):
        self.UI.Select(name, value)

    def ClickLoc(self, x, y):
        self.UI.ClickLocation(x, y)



