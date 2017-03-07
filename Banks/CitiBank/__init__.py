import os

from Banks import Bank
from Banks.CitiBank import CitiBankWeb

from HTMLParser import HTMLParser
from Banks.CitiBank import CitiBankHTML


class CitiBank(Bank):
    def __init__(self, name):
        Bank.__init__(self, name)
        self.bankWeb = CitiBankWeb.CitiBankWeb(self.saveFile)
        #self.parser = CitiBankHTML.CitiBankHTML(self.saveFile)
        self.bankParser = HTMLParser(self.saveFile, "citi")

