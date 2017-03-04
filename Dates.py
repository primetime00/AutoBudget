from datetime import date, datetime, time, timedelta
from calendar import monthrange

class Dates():
    dateArray = [
        '%m/%Y',
        '%m/%d/%Y',
        '%m/%y',
        '%m/%d/%y',
        '%m-%Y',
        '%m-%d-%Y',
        '%m-%y',
        '%m-%d-%y',
    ]

    @classmethod
    def empty(cls):
        return cls(datetime.now().month, datetime.now().year)

    @classmethod
    def string(cls, dateString):
        found=False
        for da in cls.dateArray:
            try:
                d = datetime.strptime(dateString, da)
                found = True
                break
            except:
                continue
        if not found:
            raise Exception("Can't parse date")
        return cls(d.month, d.year)

    @staticmethod
    def previousMonth():
        return datetime.now().replace(day=1) - timedelta(days=1)



    def __init__(self, month, year):
        self.date = self.calculateDayAndTime(month, year)


    def getDate(self):
        return self.date

    def lastDay(self):
        return monthrange(self.date.year, self.date.month)[1]

    def remainingTime(self):
        lastTime = datetime.combine(date(month=self.date.month, day=self.lastDay(), year=self.date.year), time.max)
        return lastTime-self.date

    def pastTime(self):
        firstTime = datetime.combine(date(month=self.date.month, day=1, year=self.date.year), time.min)
        return self.date - firstTime

    def remainingDays(self):
        return self.remainingTime().days + (self.remainingTime().seconds/(60*60*24.0))

    def remainingSeconds(self):
        time = self.remainingTime()
        sec = time.days*24*60*60 + time.seconds
        return sec

    def pastDays(self):
        return self.pastTime().days + (self.pastTime().seconds/(60*60*24.0))

    def pastSeconds(self):
        time = self.pastTime()
        sec = time.days*24*60*60 + time.seconds
        return sec

    def calculateDayAndTime(self, month, year):
        today = datetime.now()
        if year != today.year or month != today.month: ##we are gathering a previous time
            if datetime(year=year, month=month, day=1) > today:
                raise Exception("Cannot use future times")
            ndate = date(month=month, day=monthrange(year, month)[1], year=year)
            ntime = time(23, 59, 58, 999999)
            return datetime.combine(ndate, ntime)
        else: #assume that we want current time
            return datetime.now()

    def isCurrentMonthAndYear(self):
        today = datetime.now()
        return self.getDate().month == today.month and self.getDate().year == today.year

    def getFirstOfNextMonth(self):
        v = self.getDate()
        return datetime(v.year + int(v.month / 12), ((v.month % 12) + 1), 1)





