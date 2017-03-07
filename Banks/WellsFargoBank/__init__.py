import os

from Banks import Bank
from Banks.WellsFargoBank import WellsFargoBankWeb

from Banks.WellsFargoBank import WellsFargoHTML
from HTMLParser import HTMLParser


class WellsFargoBank(Bank):
    def __init__(self, name):
        Bank.__init__(self, name)
        self.bankWeb = WellsFargoBankWeb.WellsFargoBankWeb(self.saveFile)
        #self.parser = WellsFargoHTML.WellsFargoHTML(self.saveFile)
        self.bankParser = HTMLParser(self.saveFile, "wells")



