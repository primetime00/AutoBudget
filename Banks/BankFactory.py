from Banks.CitiBank import CitiBank
from Banks.WellsFargoBank import WellsFargoBank


class BankFactory:
    def __init__(self):
        self.bankMap = {
            'wells' : WellsFargoBank,
            'citi' : CitiBank
        }

    def createBank(self, name):
        if name not in self.bankMap:
            raise Exception("Factory could not create bank: " + name)
        return self.bankMap[name](name)