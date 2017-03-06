from bs4 import BeautifulSoup
from Dates import Dates
from Configuration import Configuration
import re
from dateutil import parser

class HTMLParser:
    # def __init__(self, fname):
    #     self.transactions = []
    #     self.data = ""
    #     self.filename = fname
    #     self.html = None
    #     self.userDate = None

    def __init__(self, fname, dateString, descriptionStr, depositStr, withdrawStr):
        self.transactions = []
        self.data = ""
        self.filename = fname
        self.html = None
        self.userDate = None
        self.date = dateString
        self.description = descriptionStr
        self.deposit = depositStr
        self.withdrawal = withdrawStr

    def __init__(self, fname, bankName):
        self.transactions = []
        self.data = ""
        self.filename = fname
        self.html = None
        self.userDate = None
        parser = Configuration().getHTMLParser(bankName)
        if parser == None:
            raise Exception("Can't find HTML parser")
        self.date = parser["date"]
        self.description = parser["description"]
        self.deposit = parser["deposit"]
        self.withdrawal = parser["withdrawal"] if "withdrawal" in parser else None
        self.empty = parser["empty"] if "empty" in parser else None



    def processHTML(self):
        try:
            with open(self.filename, mode="r") as f:
                soup = BeautifulSoup(f.read(), "lxml")
        except:
            return None
        tableInfo = {}
        if self.empty != None:
            if soup.find(text=re.compile(r'.*'+self.empty+'.*')) != None:
                return []
        ns = soup.find_all(text=re.compile(".*"+self.description+".*"))
        if len(ns) == 0:
            raise
        for item in ns:
            row = item.find_parent('tr')
            if row == None:
                continue
            break
        cells = row.find_all('th')
        if cells == None:
            cells = row.find_all('td')
        if cells == None:
            return None
        for i in range(0, len(cells)):
            if self.date in cells[i].text:
                tableInfo["date"] = i
            elif self.description in cells[i].text:
                tableInfo["description"] = i
            elif self.deposit in cells[i].text:
                tableInfo["deposit"] = i
            elif self.withdrawal != None and self.withdrawal in cells[i].text:
                tableInfo["withdrawal"] = i
        table = row.find_parent('table')
        if 'class' in table.attrs:
            tableInfo["table"] = table["class"][0]
        elif 'id' in table.attrs:
            tableInfo["table"] = table["id"][0]
        else:
            return None
        return self.processTransactions(tableInfo, soup)

    def processTransactions(self, info, soup):
        trans = []
        cashRe = re.compile(r'(\d*\.\d{2})')
        table = soup.find('table', attrs={'class': info['table']})
        if table == None:
            table = soup.find('table', attrs={'id': info['table']})
        if table == None:
            return None
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            tx = {}
            error = False
            for i in range(0, len(cells)):
                if i == info["date"]:
                    try:
                        tx["date"] = parser.parse(cells[i].text, fuzzy=True).strftime("%m/%d/%Y")
                    except:
                        error = True
                        pass
                elif i == info["description"]:
                    val = list(filter(None, cells[i].text.strip().replace("\n", "").split("  ")))
                    val = list(filter(lambda k: 'pending' not in k.lower(), val))
                    if len(val) == 1:
                        tx["description"] = val[0]
                    else:
                        tx["description"] = val[0] + ' ' + val[1]
                elif i == info["deposit"]:
                    val = cells[i].text.strip().replace("$", "").replace(",", "")
                    if len(val) == 0:
                        continue
                    val = cashRe.search(val).group(0)
                    tx["amount"] = float(val)
                elif 'withdrawal' in info and 'amount' not in tx and i == info["withdrawal"]:
                    val = cells[i].text.strip().replace("$", "").replace(",", "")
                    val = cashRe.search(val).group(0)
                    tx["amount"] = -float(val)
            if error == False and len(tx.keys()) > 0:
                trans.append(tx)
        return trans

    def getTransactions(self):
        return self.transactions

    def Run(self, userDate=Dates.empty()):
        self.userDate = userDate
        try:
            self.transactions = self.processHTML()
            if self.transactions == None:
                raise
        except Exception as e:
            raise Exception("Could not read HTML data: " + str(e))