import json
from datetime import datetime
from Dates import Dates
from Singleton import Singleton

class History(Singleton):

    def firstTime(self, **kwargs):
        try:
            with open('Config\\history.json', mode='r') as f:
                jData = f.read()
            self.data = sorted(json.loads(jData), key=lambda x: x['date'])
            self.average = self.calculateTotalAverage()
            self.saved = self.calculateTotalSaved()
        except:
            self.data = []
            self.average = 0
            self.saved = 0
            self.size = 0


    def calculateTotalAverage(self):
        valids = [item['average'] for item in self.data if self.isValid(item['date'])]
        self.size = len(valids)
        if len(valids) == 0:
            return 0
        return sum(valids) / len(valids)

    def calculateTotalSaved(self):
        valids = [item['saved'] for item in self.data if self.isValid(item['date'])]
        return sum(valids)

    def includesDate(self, month, year):
        valids = [item for item in self.data if self.isValid(item['date'])]
        for item in reversed(valids):
            dt = datetime.strptime(item['date'], "%Y-%m")
            if dt.year == year and dt.month == month:
                return True
        return False

    def indexOf(self, date):
        for i in range(0, len(self.data)):
            if Dates.string(self.data[i]['date']) == date:
                return i
        return -1

    def isValid(self, dateStr):
        if Dates.string(dateStr) > Dates.empty():
            return False
        return True

    def Store(self, spending, remaining, date):
        dt = date.getDate().strftime("%Y-%m")
        totalDays = date.pastDays()+date.remainingDays()
        average = spending / totalDays
        index = self.indexOf(date)
        if index >= 0:
            self.data[index] = {"date": dt, "average": average, "saved": remaining, "posted": self.data[index]["posted"]}
        else:
            self.data.append({"date": dt, "average": average, "saved": remaining, "posted":False})
        self.writeData()
        self.average = self.calculateTotalAverage()
        self.saved = self.calculateTotalSaved()

    def hasPosted(self, date):
        loc = self.indexOf(date)
        if loc == -1:
            return False
        return self.data[loc]["posted"]

    def needsPosted(self, date):
        if not self.hasPosted(date):
            if date.daysSinceLastDay() > 3:
                return True
        return False





    def calculateWeightedAverage(self, average, date):
        averages = [self.average, average]
        days = [date.remainingDays(), date.pastDays()]
        weighted = sum(days[g] * averages[g] for g in range(len(averages))) / sum(days)
        return weighted

    def empty(self):
        return len(self.data) == 0

    def Post(self, date):
        loc = self.indexOf(date)
        if loc == -1:
            return
        self.data[loc]["posted"] = True

    def writeData(self):
        with open('Config\\history.json', mode='w') as f:
            f.write(json.dumps(self.data, indent=2))



