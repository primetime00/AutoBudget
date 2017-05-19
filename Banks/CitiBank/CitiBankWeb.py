from time import sleep
from BankWeb import BankWeb
from Configuration import Configuration


class CitiBankWeb(BankWeb):
    def __init__(self, saveFile):
        BankWeb.__init__(self, Configuration().findBank('citi'), saveFile)

    def OpenSite(self):
        self.Press('{F6}')
        sleep(0.5)
        self.Press(self.site)
        self.Press('{ENTER}')

    def Login(self):
        self.Wait("Banking with Citi", post_delay=4)
        self.ClickLoc(1292, 271) #stinking message popup
        sleep(0.1)
        self.ClickLoc(114, 788)
        self.Press(self.user)
        self.ClickLoc(411, 788)
        self.Press(self.password)
        self.ClickLoc(691, 788)

    def NavigateToTransactions(self):
        self.Wait("Accounts", timeout=15, post_delay=4)
        data = self.GetClipBoard()
        sleep(1.0)
        self.SetYOffset(60)
        #if "Reminder" in data:
        #    self.SetYOffset(80)
        #    sleep(1.0)


        self.ClickLoc(276, 627)
        self.Wait("Account Information", timeout=14, post_delay=6)
        self.ClickLoc(425, 123)
        sleep(0.25)
        self.Press('{END}')
        sleep(0.5)
        self.Press('{ENTER}')
        sleep(1.0)
        self.ClickLoc(280, 189)
        sleep(0.25)
        today = self.userDate.getDate()
        month = today.strftime("%b")
        year = today.year
        value = "{}. 01, {}".format(self.beginDate.getDate().strftime("%b"), self.beginDate.getDate().year)
        self.Type(value)
        self.Press('{ESC}')
        self.ClickLoc(490, 189)
        #we need to go to the first day of the next month due to a bug in citibanks web page
        today = self.userDate.getFirstOfNextMonth()
        month = today.strftime("%b")
        day = format(today.day, '02')
        year = today.year
        value = "{}. {}, {}".format(month, day, year)
        sleep(0.5)
        self.Type(value)
        self.Press('{ESC}')
        self.ClickLoc(677, 189)
        self.Wait("Account Information", timeout=14, post_delay=2.5)


    def Logout(self):
        self.Wait("Account Information", timeout=12, post_delay=0.2)
        self.Press("{F6}")
        sleep(2.0)
        self.Press(self.signout)
        self.Press("{ENTER}")
        self.Wait("Sign Off", timeout=7)

