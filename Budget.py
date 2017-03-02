from Configuration import Configuration
from Dates import Dates


class Budget:
    def __init__(self, output=None, date=Dates.empty()):
        self.date=date
        self.budgetData = Configuration().getBudget()
        self.transactions = []
        self.outputFile = output

    def Calculate(self, transactions):
        self.transactions = []
        self.addTransactions(transactions)
        income = self.sumIncome()
        expenses = self.sumExpenses()
        spending = self.processTransactions()
        remaining = income - expenses - spending["total"]
        forcast = income - expenses - spending["projected"]

        topSpends = self.GetSortedTransactions()[0:3]

        result = {
            "income" : income,
            "spending" : spending,
            "topSpends" : topSpends,
            "expenses" : expenses,
            "forecast" : forcast,
            "threshold" : self.budgetData["savingsThreshold"],
            "remaining" : remaining
        }
        return result

    def GetSortedTransactions(self, remove_ignore=True):
        if not remove_ignore:
            return sorted(self.transactions, key=lambda x: x["amount"], reverse=True)
        return sorted([item for item in self.transactions if not self.ignored(item["name"])], key=lambda x: x["amount"], reverse=True)



    def addTransactions(self, trans):
        for tran in trans:
            self.transactions.append({"name":tran["name"], "amount":float(tran["amount"])})

    def sum(self, field):
        total = 0
        month = self.date.getDate().month
        for item in self.budgetData[field]:
            if "month" in item and item["month"] != month:
                continue
            total+= item["amount"]
        return total

    def sumIncome(self):
        return self.sum("income")

    def sumExpenses(self):
        return self.sum("expenses")

    def processTransactions(self):
        total = 0
        if self.outputFile != None:
            f = open(self.outputFile, mode="w")
            t = sorted(self.transactions, key=lambda x: x["amount"])
        else:
            t = self.transactions
        for trans in t:
            if self.outputFile != None:
                f.write('"{}", {}\n'.format(trans["name"], trans["amount"]))
            if not self.ignored(trans["name"]):
                total += float(trans["amount"])
        if self.outputFile != None:
            f.close()

        average = float(total)/self.date.pastDays()

        projection = average * self.date.lastDay()

        result = {
            "total": total,
            "dailyAverage": average,
            "projected": projection
        }
        return result

    def ignored(self, name):
        for ignore in self.budgetData["ignore"]:
            if ignore.lower() in name.lower():
                return True
        return False



