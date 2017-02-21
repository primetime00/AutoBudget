import re
from datetime import datetime

from HTMLParser import HTMLParser

class WellsFargoHTML(HTMLParser):
    def __init__(self, fname):
        HTMLParser.__init__(self, fname)

    def parseData(self):
        table = self.html.find('table', {'class': re.compile("transaction.*")})
        if table == None: # no transactions or an error?
            if "No transactions meet your search criteria." in self.data:
                self.transactions = []
                return
            else:
                raise Exception("Wells Fargo could not find transactions [Check for site change]")
        rows = table.find_all('tr', {'class': re.compile("detailed.*")})
        if rows == None: # no transactions
            self.transactions = []
            return
        found = False
        for row in rows:
            cells = row.find_all('td')
            day = cells[1].text
            try:
                datetime.strptime(day, '%m/%d/%y')
                found = True
                text = cells[2].text
                if len(cells[3].text.strip()) > 0:  # it is a deposit
                    amount = '-' + cells[3].text.strip()
                elif len(cells[4].text.strip()) > 0:  # it is an expense
                    amount = cells[4].text.strip()
                else:  # what in the world
                    raise Exception("Failed parsing deposits and expenses in Wells Fargo")
                amount = amount.replace("$", "").replace(",","")
                self.transactions.append({"name": text, "amount": amount})
            except ValueError:
                continue
        if not found:
            raise Exception("Could not parse HTML table!")


