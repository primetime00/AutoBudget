import re

from HTMLParser import HTMLParser
from datetime import datetime


class CitiBankHTML(HTMLParser):
    def __init__(self, fname):
        HTMLParser.__init__(self, fname)
        #self.moneyPattern = re.compile(r'\$\s*[.0-9]*\s*([-.0-9]*)')

    def parseData(self):
        moneyPattern = re.compile(r'\$\s*[.0-9]*\s*([-.0-9]*)')
        rows = self.html.find_all('tr', {'class': re.compile(".*transactionsTableRow")})
        if rows == None or len(rows) == 0:
            if "No activity available for period requested" in self.data:
                self.transactions = []
                return
            else:
                raise Exception("CitiBank could not find transactions [Check for site change]")
        for row in rows:
            transactionName = row.find('td', {'class': re.compile(".*TransactionDescriptionColumn")})
            amountName = row.find('td', {'class': re.compile(".*CreditCardTransactionAmountColumn")})
            dateName = row.find('td', {'class': re.compile(".*TransactionDateColumn")})
            groups = moneyPattern.search(amountName.text)
            spanText = transactionName.find_all('span')[2].text.strip()
            actualDate = dateName.text.strip().split('  ')[0]
            d = datetime.strptime(actualDate, "%b. %d, %Y")
            self.transactions.append({"name": spanText, "amount": groups.group(1)})