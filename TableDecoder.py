from bs4 import BeautifulSoup
import re
from datetime import datetime
from dateutil import parser


def find(fname, dateString, descriptionStr, depositStr, withdrawStr, dateFormat):
    try:
        with open(fname, mode="r") as f:
            soup = BeautifulSoup(f.read(), "lxml")
    except:
        return None
    tableInfo = {}
    ns = soup.find_all(text=re.compile(".*"+descriptionStr+".*"))
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
        if dateString in cells[i].text:
            tableInfo["date"] = i;
        elif descriptionStr in cells[i].text:
            tableInfo["description"] = i;
        elif depositStr in cells[i].text:
            tableInfo["deposit"] = i;
        elif withdrawStr != None and withdrawStr in cells[i].text:
            tableInfo["withdrawal"] = i;
    tableInfo["dateFormat"] = dateFormat
    table = row.find_parent('table')
    if 'class' in table.attrs:
        tableInfo["table"] = table["class"][0]
    elif 'id' in table.attrs:
        tableInfo["table"] = table["id"][0]
    else:
        return None
    return getTransactions(tableInfo, soup)

def getTransactions(info, soup):
    trans = []
    cashRe = re.compile(r'(\d*\.\d{2})')
    table = soup.find('table', attrs={'class':info['table']})
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
                val = list(filter(None ,cells[i].text.strip().replace("\n", "").split("  ")))
                val = list(filter(lambda k : 'pending' not in k.lower(), val))
                if len(val) == 1:
                    tx["description"] = val[0]
                else:
                    tx["description"] = val[0] + ' ' +val[1]
            elif i == info["deposit"]:
                val = cells[i].text.strip().replace("$","").replace(",","")
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

#v = find("C:\\tmp\\test.html", "Date", "Description", "Amount", None, "%m/%d/%y")
#for i in v:
#    print (i)

v = find("citi\\citi-feb.html", "Date", "Description", "Amount", None, "%m/%d/%y")
for i in v:
    print (i)


v = find("wells\\wells-feb.html", "Date", "Description", "Deposits/Credits", "Withdrawals/Debits", "%m/%d/%y")
#for i in v:
#    print (i)






def train(info, dateString, description, amount, deposit=None):
    tableInfo = info
    navString = soup.find(text=re.compile('.*{}.*'.format(description)))
    #find the cell
    row = navString.find_parent('tr')
    cell = navString.find_parent('td')
    cells = row.find_all('td')
    for i in range(0, len(cells)):
        if dateString in cells[i].text:
            tableInfo["date"] = i;
        elif description in cells[i].text:
            tableInfo["description"] = i;
        if amount != None:
            if amount in cells[i].text:
                tableInfo["amount"] = i;
        elif deposit != None:
            if deposit in cells[i].text:
                tableInfo["deposit"] = i;
    table = row.find_parent('table')
    if 'class' in table.attrs:
        tableInfo["table"] = table["class"][0]
    elif 'id' in table.attrs:
        tableInfo["table"] = table["id"][0]
    else:
        return None
    return tableInfo

#info = train({}, "02/28/17", "SENSUS", "$3,419.73", None)
#info = train(info, "02/28/17", "TRANSFER", None, "$1,685.00")

#print(info["table"])


