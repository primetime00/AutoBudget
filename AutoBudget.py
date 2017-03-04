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
        from Service import Service
        if self.args.service:
            Service().Run()
        else:
            Service().Single(simulate=self.args.simulation, date=self.args.date)

AutoBudget().Run()


#
#if not Configuration().hasBrowser():
#    print("YOU need to install a browser")
#    BrowserInstall(debug=True).DownloadAndExtract()
#    exit()