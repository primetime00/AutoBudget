import os, shutil
from Dates import Dates


class Bank:
    def __init__(self, name):
        self.bankWeb = None
        self.bankParser = None
        self.name = name
        self.saveFile = os.getcwd()+'\\'+ self.name + "\\" + self.name+".html"


    def Run(self, simulate=False, date=Dates.empty(), lookBack=1):
        os.makedirs(os.getcwd()+'\\'+ self.name, exist_ok=True)
        if self.bankWeb == None or self.bankParser == None:
            raise Exception("Bank or parser not defined")
        if not simulate:
            self.bankWeb.Run(date=date, lookBack=lookBack)
        self.bankParser.Run(date=date)
        # if not simulate:
        #     try:
        #         shutil.rmtree(os.getcwd()+'\\'+ self.name)
        #     except Exception:
        #         print("Couldn't remove web files")

    def GetTransactions(self):
        return self.bankParser.getTransactions()
