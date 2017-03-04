import json
from datetime import datetime
from Dates import Dates
from Singleton import Singleton

class History(Singleton):

    def firstTime(self, **kwargs):
        self.date = (kwargs["date"] if "date" in kwargs else Dates.empty())
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

    def indexOf(self, month, year):
        for i in range(0, len(self.data)):
            dt = datetime.strptime(self.data[i]['date'], "%Y-%m")
            if dt.year == year and dt.month == month:
                return i
        return -1

    def isValid(self, dateStr):
        try:
            dt = datetime.strptime(dateStr, "%Y-%m")
        except:
            return False
        now = self.date.getDate()
        if dt.year > now.year or (dt.year == now.year and dt.month >= now.month):
            return False
        return True

    def Store(self, spending, remaining, date):
        dt = date.getDate().strftime("%Y-%m")
        totalDays = date.pastDays()+date.remainingDays()
        average = spending / totalDays
        index = self.indexOf(date.getDate().month, date.getDate().year)
        if index >= 0:
            self.data[index] = {"date": dt, "average": average, "saved": remaining}
        else:
            self.data.append({"date": dt, "average": average, "saved": remaining})
        with open('Config\\history.json', mode='w') as f:
            f.write(json.dumps(self.data, indent=2))

    def calculateWeightedAverage(self, average, date):
        averages = [self.average, average]
        days = [self.size*30, date.pastDays()]
        return sum(days[g] * averages[g] for g in range(len(averages))) / sum(days)

    def empty(self):
        return len(self.data) == 0


