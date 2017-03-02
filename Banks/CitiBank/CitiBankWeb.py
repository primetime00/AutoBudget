from datetime import date
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

    def LoginOld(self):
        self.Wait("Banking with Citi", post_delay=4)
        self.Press('{TAB 12}')
        self.Press(self.user)
        self.Press('{TAB 1}')
        self.Press(self.password)
        self.Press('{ENTER 1}')

    def NavigateToTransactions(self):
        self.Wait("Accounts", timeout=15, post_delay=4)
        self.ClickLoc(276, 627)
        self.Wait("Account Information", timeout=14, post_delay=4)
        self.ClickLoc(425, 123)
        sleep(0.25)
        self.Press('{END}')
        sleep(0.5)
        self.Press('{ENTER}')
        sleep(1.0)
        self.ClickLoc(280, 189)
        sleep(0.25)
        today = date.today()
        if self.userDate is not None:
            today = self.userDate
        month = today.strftime("%b")
        year = today.year
        value = "{}. 01, {}".format(month, year)
        self.Type(value)
        self.Press('{ESC}')
        self.ClickLoc(490, 189)
        day = format(today.day, '02')
        value = "{}. {}, {}".format(month, day, year)
        sleep(0.5)
        self.Type(value)
        self.Press('{ESC}')
        self.ClickLoc(677, 189)
        self.Wait("Account Information", timeout=14, post_delay=2.5)


    def NavigateToTransactionsOld(self):
        self.Wait("Accounts", timeout=15, post_delay=4)
        self.Press('{F6}')
        sleep(0.5)
        self.Press('{TAB 21}')
        self.Press('{ENTER}')
        self.Wait("Account Information", timeout=14, post_delay=3)
        self.Press('{F6}')
        sleep(0.5)
        self.Press('{TAB 37}')
        self.Press('{SPACE 1}')
        sleep(0.5)
        self.Press('{DOWN 10}')
        self.Press('{ENTER}')
        sleep(1.0)
        self.Press('{TAB 4}')
        sleep(0.5)
        today = date.today()
        month = today.strftime("%b")
        year = today.year
        value = "{}. 01, {}".format(month, year)
        self.Type(value)
        self.Press('{ESC}')
        self.Press('{TAB 2}')
        day = format(today.day, '02')
        value = "{}. {}, {}".format(month, day, year)
        sleep(0.5)
        self.Type(value)
        self.Press('{ESC}')
        self.Press('{TAB 2}')
        self.Press('{ENTER}')
        sleep(2)

    def Logout(self):
        self.Wait("Account Information", timeout=12, post_delay=0.2)
        self.Press("{F6}")
        sleep(2.0)
        self.Press(self.signout)
        self.Press("{ENTER}")
        self.Wait("Sign Off", timeout=7)

