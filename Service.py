import win32.win32api as win32api
import time, ctypes, os
from Configuration import Configuration

from TransactionProcessor import TransactionProcessor
from Budget import Budget
from Email.Email import Email
import traceback, json


class Service:
    RERUN = 0
    SUCCESS = 1
    FAIL = 2

    def __init__(self):
        self.data = {}
        with open(os.getcwd()+"\\Config\\service.json") as cFile:
            self.data = json.loads(cFile.read())
        self.maxFails = self.data["maxFailures"]
        self.failures = 0
        self.idle = 60*self.data["idleMinutes"]
        self.sleepTime = 60*self.data["sleepMinutes"]
        self.scheduleTime = 60*self.data["scheduleMinutes"]
        self.lastRun = time.time() - (self.scheduleTime * 2)

        self.errorLog = []

    def Run(self):
        while 1:
            currentTime = time.time()
            secondsSinceLastRun = (currentTime - self.lastRun)
            if secondsSinceLastRun > self.scheduleTime and self.isIdle():
                res = self.doTick()
                if res == self.FAIL:
                    Email().Error(self.errorLog)
                    self.lastRun = time.time()
                    self.failures = 0
                elif res == self.SUCCESS:
                    time.sleep(self.sleepTime)  # check again in 15 minutes
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
        res = self.tick()
        if (res == True):
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

    def tick(self):
        print("Doing tick")
        processor = TransactionProcessor()
        try:
            processor.Run(simulate=False)
        except:
            self.errorLog.append("----------------------------------------------------")
            self.errorLog.extend(traceback.format_exc().splitlines())
            self.errorLog.append("----------------------------------------------------")
            return False

        budget = Budget()
        result = budget.Calculate(processor.GetTransactions())
        Email().Run(result)
        return True

    def isIdle(self):
        current = (ctypes.c_ulong(win32api.GetTickCount()).value / 1000)
        idle = win32api.GetLastInputInfo() / 1000
        return (current - idle) >= self.idle


Service().Run()
