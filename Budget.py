from Configuration import Configuration
from Dates import Dates
from History import History


class Budget:
    def __init__(self, output=None, date=Dates.empty()):
        self.date=date
        self.budgetData = Configuration().getBudget()
        self.transactions = []
        self.outputFile = output
        self.history = History()

    def Run(self, transactions):
        self.SortTransactions(transactions)

        results = []
        for trans in self.transactions:
            if (len(trans) == 0):
                continue
            currentDate = Dates(trans[0]["date"].month, trans[0]["date"].year)
            if currentDate > self.date:
                break
            val = self.Calculate(trans)
            if self.history.needsPosted(currentDate) or currentDate == self.date:
               results.append(val)
        return results



    def SortTransactions(self, transactions):
        transactions.sort(key=lambda x: x["date"])
        count = 0
        start = 0
        previous = transactions[0]["date"].month
        for i in range(0, len(transactions)):
            current = transactions[i]["date"].month
            if current != previous:
                count += 1
                self.transactions.append(transactions[start:i])
                start = i
                previous = current
        self.transactions.append(transactions[start:i + 1])

    def Calculate(self, monthTransactions):


        self.currentTransactions = monthTransactions
        income = self.sumIncome()
        expenses = self.sumExpenses()
        spending = self.processTransactions()
        remaining = income - expenses - spending["total"]
        forcast = income - expenses - spending["projected"]

        topSpends = self.GetSortedTransactions()[0:6]
        date = Dates(self.currentTransactions[0]["date"].month, self.currentTransactions[0]["date"].year)

        result = {
            "income" : income,
            "spending" : spending,
            "topSpends" : topSpends,
            "expenses" : expenses,
            "forecast" : forcast,
            "threshold" : self.budgetData["savingsThreshold"],
            "remaining" : remaining,
            "date" : date
        }

        #if this is a past budget, lets write out the data
        if not date.isCurrentMonthAndYear():
            self.history.Store(spending['total'], remaining, date)
        return result

    def GetSortedTransactions(self, remove_ignore=True):
        if not remove_ignore:
            return sorted(self.currentTransactions, key=lambda x: x["amount"], reverse=True)
        return sorted([item for item in self.currentTransactions if not self.ignored(item["description"])], key=lambda x: x["amount"], reverse=True)



    def addTransactions(self, trans):
        for tran in trans:
            self.transactions.append({"date":tran["date"], "name":tran["description"], "amount":tran["amount"]})

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
            t = self.currentTransactions
        for trans in t:
            if self.outputFile != None:
                f.write('"{}", {}\n'.format(trans["name"], trans["amount"]))
            if not self.ignored(trans["description"]):
                total += trans["amount"]
        if self.outputFile != None:
            f.close()

        #is this month over?
        now = Dates.empty()
        then = self.currentTransactions[0]["date"]
        oldDate = Dates(then.month, then.year)
        days = oldDate.pastDays() + oldDate.remainingDays()
        if (now > Dates(then.month, then.year)):
            average = total / days
            projection = total
        else: #we are working with an incomplete month, use history
            average = self.history.calculateWeightedAverage(float(total)/self.date.pastDays(), self.date)
            projection = average*self.date.remainingDays()+total

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



