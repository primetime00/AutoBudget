from Configuration import Configuration
from GUI import GUI

from Banks.BankFactory import BankFactory


class TransactionProcessor:
    def __init__(self):
        self.bankFactory = BankFactory()
        self.transactions = []
        self.banks = self.AddBanks()

    def AddBanks(self):
        bList = []
        for bankData in Configuration().getBanks():
            if "include" in bankData and bankData["include"] == "false":
                continue
            bList.append(self.bankFactory.createBank(bankData["name"]))
        return bList

    def Run(self, simulate=False):
        if not simulate:
            GUI().OpenBrowser(Configuration().getBrowserTitle(), Configuration().getBrowserPath())
        for bank in self.banks:
            bank.Run(simulate=simulate)
            self.transactions.extend(bank.GetTransactions())
        if not simulate:
            GUI().CloseBrowser()

    def GetTransactions(self):
        return self.transactions

