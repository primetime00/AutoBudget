import os, shutil
from Dates import Dates


class Bank:
    def __init__(self, name):
        self.bank = None
        self.parser = None
        self.name = name
        self.saveFile = os.getcwd()+'\\'+ self.name + "\\" + self.name+".html"


    def Run(self, simulate=False, userDate=Dates.empty()):
        os.makedirs(os.getcwd()+'\\'+ self.name, exist_ok=True)
        if self.bank == None or self.parser == None:
            raise Exception("Bank or parser not defined")
        if not simulate:
            self.bank.Run(userDate=userDate)
        self.parser.Run(userDate=userDate)
        # if not simulate:
        #     try:
        #         shutil.rmtree(os.getcwd()+'\\'+ self.name)
        #     except Exception:
        #         print("Couldn't remove web files")

    def GetTransactions(self):
        return self.parser.getTransactions()
