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
        '%Y-%m',
        '%Y-%m-%d',
        '%y-%m',
        '%y-%m-%d',

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

    @classmethod
    def previousMonth(cls, numMonths=1):
        return cls.previousMonth(cls.empty(), numMonths=numMonths)

    @classmethod
    def previousMonth(cls, userDate, numMonths=1):
        if numMonths < 1:
            raise Exception("Previous number of months must be 1 or more.")
        d = userDate.getDate()
        for i in range(0, numMonths):
            d = d.replace(day=1) - timedelta(days=1)
        return cls(d.month, d.year)

    def typeCheck(self, other):
        if type(other) is type(self):
            return True
        return False

    def __init__(self, month, year):
        self.date = self.calculateDayAndTime(month, year)

    def __lt__(self, other):
        if self.typeCheck(other):
            c1 = (self.getDate().month < other.getDate().month) and (self.getDate().year == other.getDate().year)
            c2 = (self.getDate().year < other.getDate().year)
            return c1 or c2
        return False

    def __gt__(self, other):
        if self.typeCheck(other):
            c1 = (self.getDate().month > other.getDate().month) and (self.getDate().year == other.getDate().year)
            c2 = (self.getDate().year > other.getDate().year)
            return c1 or c2
        return False


    def __eq__(self, other):
        if self.typeCheck(other):
            c1 = (self.getDate().month == other.getDate().month) and (self.getDate().year == other.getDate().year)
        else:
            c1 = False
        return c1

    def __ne__(self, other):
        return not self.__eq__(other)

    def __ge__(self, other):
        return self.__eq__(other) or self.__gt__(other)

    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)

    def __str__(self):
        return self.date.strftime("%m/%Y")

    def getDate(self):
        return self.date

    def lastDay(self):
        return monthrange(self.date.year, self.date.month)[1]

    def daysSinceLastDay(self):
        now = Dates.empty()
        return (now.getDate() - self.date).days

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





