from bs4 import BeautifulSoup
from Dates import Dates

class HTMLParser:
    def __init__(self, fname):
        self.transactions = []
        self.data = ""
        self.filename = fname
        self.html = None
        self.userDate = None

    def Run(self, userDate=Dates.empty()):
        self.userDate = userDate
        try:
            with open(self.filename) as html:
                self.data = html.read()
            if self.data == "":
                raise
            self.html = BeautifulSoup(self.data, "lxml")
        except Exception as e:
            raise Exception("Could not read HTML data: " + str(e))
        self.parseData()

    def parseData(self):
        raise Exception("HTML has no definition to parse data.")

    def getTransactions(self):
        return self.transactions