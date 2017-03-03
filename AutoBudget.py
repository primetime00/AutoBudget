from __future__ import print_function
from Budget import Budget
from TransactionProcessor import TransactionProcessor
from Email.Email import Email
import traceback, sys, argparse
from Dates import Dates
from BrowserInstall import BrowserInstall


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class AutoBudget:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--simulation', action='store_true', help='Run with simulated data')
        parser.add_argument('--service', action='store_true', help='Run in service mode')
        parser.add_argument('--date', help='Run budget on a different date/year', type=Dates.string,
                            default=Dates.empty())
        try:
            self.args = parser.parse_args()
        except Exception as e:
            eprint(e)
            exit()
        self.checkArgs()

    def checkArgs(self):
        if self.args.simulation and self.args.service:
            eprint("Service mode cannot be used with simulation data.")
            exit()

    def Run(self):
        if self.args.service:
            from Service import Service
            Service().Run()
        else:
            self.singleRun(simulate=False)

    def singleRun(self, simulate=False):
        date = self.args.date
        try:
            self.processor = TransactionProcessor()
            self.processor.Run(simulate=simulate, date=date)
        except Exception as e:
            data = traceback.format_exc().splitlines()
            Email().Error(data)
            exit()
        self.processBudget()

    def processBudget(self):
        date = self.args.date
        budget = Budget(date=date, output="C:\\tmp\\trans.csv")
        result = budget.Calculate(self.processor.GetTransactions())
        self.emailResults(result)

    def emailResults(self, result):
        date = self.args.date
        Email(date=date).Run(result)

AutoBudget().Run()


#
#if not Configuration().hasBrowser():
#    print("YOU need to install a browser")
#    BrowserInstall(debug=True).DownloadAndExtract()
#    exit()