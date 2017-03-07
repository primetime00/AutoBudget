import win32.win32api as win32api
import time, ctypes, os
from Configuration import Configuration
from Dates import Dates
from History import History

from TransactionProcessor import TransactionProcessor
from Budget import Budget
from Email.Email import Email
import traceback, json


class Service:
    RERUN = 0
    SUCCESS = 1
    FAIL = 2
    CATCHUP = 3

    def __init__(self):
        self.debug = True
        self.errorLog = []

    def initialize(self):
        self.data = {}
        with open(os.getcwd()+"\\Config\\service.json") as cFile:
            self.data = json.loads(cFile.read())
        self.maxFails = self.data["maxFailures"]
        self.failures = 0
        self.idle = 60*self.data["idleMinutes"]
        self.sleepTime = 60*self.data["sleepMinutes"]
        self.scheduleTime = 60*self.data["scheduleMinutes"]
        self.lastRun = time.time() - (self.scheduleTime * 2)



    def Single(self, simulate=False):
        res = self.tick(simulate=simulate, date=Configuration().getSettings()["currentDate"])
        if not res:
            Email().Error(self.errorLog)

    def Run(self):
        self.initialize()
        while 1:
            currentTime = time.time()
            secondsSinceLastRun = (currentTime - self.lastRun)
            print("CHECKING {} {} {}".format(secondsSinceLastRun, self.scheduleTime, self.isIdle()))
            if secondsSinceLastRun > self.scheduleTime and self.isIdle():
                print("RUNNING")
                res = self.doTick()
                if res == self.FAIL:
                    Email().Error(self.errorLog)
                    self.lastRun = time.time()
                    self.failures = 0
                elif res == self.SUCCESS:
                    time.sleep(self.sleepTime)  # check again in 15 minutes
                    continue
                elif res == self.CATCHUP:
                    time.sleep(4)  # grab the next set of data
                    continue
                else:
                    time.sleep(10)
                    continue
            else:
                time.sleep(self.sleepTime)  # check again in 15 minutes
                continue



    def killBrowser(self):
        os.system('taskkill/im ' + Configuration().getBrowserName() + '.exe /f')

    def doTick(self):
        previous = False
        res = self.tick()

        if (res == True):
            self.failures = 0
            if previous:
                return self.CATCHUP
            self.lastRun = time.time()
            self.failures = 0
            return self.SUCCESS
        else:
            self.killBrowser()
            print("ouch fail")
            self.failures += 1
            if self.failures >= self.maxFails:
                return self.FAIL
            return self.RERUN

    def tick(self, simulate=False, date=Dates.empty(), lookBack=Configuration().getSettings()["lookBackMonths"]):
        print("Doing tick")
        processor = TransactionProcessor()
        try:
            processor.Run(simulate=simulate, date=date, lookBack=lookBack)
        except:
            self.errorLog.append("----------------------------------------------------")
            self.errorLog.extend(traceback.format_exc().splitlines())
            self.errorLog.append("----------------------------------------------------")
            for l in self.errorLog:
                print(l)
            return False

        budget = Budget(date=date)
        results = budget.Run(processor.GetTransactions())
        Email().Run(results)
        return True

    def isIdle(self):
        if self.debug:
            return True
        current = (ctypes.c_ulong(win32api.GetTickCount()).value / 1000)
        idle = win32api.GetLastInputInfo() / 1000
        print("IDLE {} {}".format((current - idle), self.idle))
        return (current - idle) >= self.idle

