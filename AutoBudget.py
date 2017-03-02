from __future__ import print_function
from Budget import Budget
from TransactionProcessor import TransactionProcessor
from Configuration import Configuration
from Email.Email import Email
import traceback, sys
from BrowserInstall import BrowserInstall


simulation = False
serviceMode = False
if "simulate" in sys.argv:
    simulation = True
if "service" in sys.argv:
    serviceMode = True

if simulation and serviceMode:
    def eprint(*args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)
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
        processor.Run(simulate=simulation)
    except Exception as e:
        data = traceback.format_exc().splitlines()
        Email().Error(data)
        exit()

    budget = Budget()
    result = budget.Calculate(processor.GetTransactions())

    v = Email()
    v.Run(result)

if not serviceMode:
    singleInstance(simulation)
else:
    from Service import Service
    Service().Run()
