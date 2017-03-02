from __future__ import print_function
from Budget import Budget
from TransactionProcessor import TransactionProcessor
from Email.Email import Email
import traceback, sys, argparse
from Dates import Dates
from BrowserInstall import BrowserInstall


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


parser = argparse.ArgumentParser()
parser.add_argument('--simulation', action='store_true', help='Run with simulated data')
parser.add_argument('--service', action='store_true', help='Run in service mode')
parser.add_argument('--date', help='Run budget on a different date/year', type=Dates.string)
try:
    args = parser.parse_args()
except Exception as e:
    eprint(e)

if args.simulation and args.service:
    eprint("Service mode cannot be used with simulation data.")
    exit()

#
#if not Configuration().hasBrowser():
#    print("YOU need to install a browser")
#    BrowserInstall(debug=True).DownloadAndExtract()
#    exit()

def singleInstance(sim):
    try:
        processor = TransactionProcessor()
        processor.Run(simulate=sim, date=args.date)
    except Exception as e:
        data = traceback.format_exc().splitlines()
        Email().Error(data)
        exit()

    budget = Budget(date=args.date, output="C:\\tmp\\trans.csv")
    result = budget.Calculate(processor.GetTransactions())

    v = Email(date=args.date)
    v.Run(result)

if not args.service:
    singleInstance(args.simulation)
else:
    from Service import Service
    Service().Run()
