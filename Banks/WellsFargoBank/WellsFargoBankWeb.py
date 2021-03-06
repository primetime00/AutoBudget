from datetime import date
from time import sleep

from BankWeb import BankWeb

from Configuration import Configuration


class WellsFargoBankWeb(BankWeb):
    def __init__(self, saveFile):
        BankWeb.__init__(self, Configuration().findBank('wells'), saveFile)

    def OpenSite(self):
        self.Press('{F6}')
        sleep(0.5)
        self.Press(self.site)
        self.Press('{ENTER}')

    def Login(self):
        self.Wait("Wells Fargo", post_delay=4)
        self.ClickLoc(255, 329)
        self.Press(self.user)
        sleep(0.25)
        self.ClickLoc(255, 364)
        self.Press(self.password)
        sleep(0.25)
        self.Press('{ENTER 1}')

    def NavigateToTransactions(self):
        self.Wait("Wells Fargo", timeout=5, post_delay=9)
        self.ClickLoc(496, 374)
        self.Wait("Wells Fargo", timeout=4, post_delay=3)
        self.SetYOffset(17)
        self.ClickLoc(179, 638)
        self.ClickLoc(253, 895)
        sleep(0.25)
        self.Press('{DOWN 6}')
        self.Press('{SPACE}')
        sleep(0.25)
        self.ClickLoc(533, 811)
        today = self.userDate.getDate()
        month = format(today.month, '02')
        year = today.strftime("%y")
        value = "{}/01/{}".format(format(self.beginDate.getDate().month, '02'), self.beginDate.getDate().strftime("%y"))
        self.Press(value)
        sleep(0.5)
        self.ClickLoc(756, 811)
        self.Press('{}/{}/{}'.format(month, today.day, year))
        sleep(5.5)
        self.SetYOffset(0)
        self.ClickLoc(1089, 1012)
        self.Wait("Wells Fargo", timeout=4, post_delay=2.5)


    def Logout(self):
        self.Wait("Wells Fargo", timeout=2, post_delay=0.2)
        self.Press("{F6}")
        sleep(2.0)
        self.Press(self.signout)
        self.Press("{ENTER}")
        self.Wait("Wells Fargo", timeout=5, post_delay=2)
