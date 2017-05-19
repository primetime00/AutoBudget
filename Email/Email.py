
import os
import smtplib
from Dates import Dates
from History import History

from bs4 import BeautifulSoup

from Configuration import Configuration



class Email:
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    def __init__(self):
        self.email = Configuration().getEmail()
        self.history = History()


    def Run(self, data, date=Dates.empty()):
        self.date = date
        for item in data:
            self.processMonth(item)
        self.history.writeData()


    def Error(self, data):
        send_to = self.email["user"]
        subject = "Budget Check Error"
        body = "Error:<br>"+'<br>'.join(data)
        self.send(send_to, subject, body)


    def generateHTML(self, data):
        with open(self.__location__+"/"+"style.css") as cssFile:
            css = cssFile.read()
        with open(self.__location__+"/"+"template.html") as htmlFile:
            html = htmlFile.read()

        spending = data["spending"]
        remaining = data["remaining"]
        average = spending["dailyAverage"]
        forecast = data["forecast"]
        threshold = data["threshold"]
        soup = BeautifulSoup(html, "lxml")

        html = soup.find('html')
        head = soup.new_tag('head')
        style = soup.new_tag('style')
        style.string = css
        head.append(style)
        html.insert(0, head)

        title = soup.find('h2')
        date = data["date"]
        if not date.isCurrentMonthAndYear():
            title.string = title.text.replace("[Date]", date.getDate().strftime('%B'))
            title.string = "---Final " + title.string + "---"
        else:
            title.string = title.text.replace("[Date]", self.date.getDate().strftime('%B'))

        summaryTable = soup.find('div', {'class':'summaryTable'})
        cell = self.modifyCell(summaryTable, 'remaining', "$"+format(remaining, '.2f'))
        cell['class'].append('cashBad' if remaining < threshold else 'cashGood')
        self.modifyCell(summaryTable, 'average', "$" + format(average, '.2f'))
        cell = self.modifyCell(summaryTable, 'forecast', "$" + format(forecast, '.2f'))
        cell['class'].append('cashBad' if remaining < threshold else 'cashGood')

        infoBlock = soup.find('div', {'class':'info'})
        if forecast > threshold:
            div = infoBlock.find('div', {'id':'goodForecast'})
            div['class'].remove('hidden')
        elif forecast >= 0:
            div = infoBlock.find('div', {'id':'lowForecast'})
            div['class'].remove('hidden')
        elif remaining < 0:
            div = infoBlock.find('div', {'id':'negitiveCash'})
            div['class'].remove('hidden')
        elif forecast < 0:
            div = infoBlock.find('div', {'id':'negitiveForecast'})
            div['class'].remove('hidden')

        transTable = soup.find('div', {'class': 'transactionTable'})
        self.createTransactionTable(transTable, data, soup)
        return str(soup)


    def createTransactionTable(self, tableDiv, data, soup):
        top = data["topSpends"]
        table = tableDiv.find('table')
        if top == None:
            table['class'] = 'hidden'
            return
        for item in top:
            row = soup.new_tag('tr')
            cell1 = soup.new_tag('td')
            cell1.string = item['description'].replace('  ', ' ')
            row.append(cell1)
            cell2 = soup.new_tag('td')
            cell2.string = '$'+format(item['amount'], '.2f')
            row.append(cell2)
            table.append(row)

    def modifyCell(self, table, id, data):
        cell = table.find('td', {'id':id})
        cell.string = data
        return cell

    def send(self, recipient, subject, body):

        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        gmail_user = self.email["user"]
        gmail_pwd = self.email["pass"]


        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = gmail_user
        msg['To'] = ", ".join(recipient) if type(recipient) is list else recipient

        html = body

        part2 = MIMEText(html, 'html')
        msg.attach(part2)

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_pwd)
            server.sendmail(gmail_user, recipient if type(recipient) is list else [recipient], msg.as_string())
            server.close()
            print('successfully sent the mail')
        except:
            print("failed to send mail")

    def processMonth(self, monthData):
        if (monthData == None): #we have no result
            return
            #self.Error(["There is no data for month of {} {}".format(self.date.getDate().strftime("%B"), self.date.getDate().year)])
            #return
        html = self.generateHTML(monthData)
        bstr = format(monthData['remaining'], '.2f')
        send_to = self.email["subscribers"]
        date = monthData["date"]
        if not date.isCurrentMonthAndYear():
            subject = "${} {} in {}".format(bstr, "overspent" if monthData['remaining'] <= 0 else "saved", date.getDate().strftime('%B'))
        elif monthData["forecast"] < monthData['threshold']:
            subject = "${} remaining [We are losing money!]".format(bstr)
        else:
            subject = "${} remaining [We are saving money!]".format(bstr)
        self.send(send_to, subject, html)
        self.history.Post(date)



