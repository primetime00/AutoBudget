import os
import smtplib
from Dates import Dates

from bs4 import BeautifulSoup

from Configuration import Configuration


class Email:
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    def __init__(self, date=Dates.empty()):
        self.date = date
        self.email = Configuration().getEmail()


    def Run(self, data):
        html = self.processData(data)
        bstr = format(data['remaining'], '.2f')
        send_to = self.email["subscribers"]
        if data["forecast"] < data['threshold']:
            subject = "${} remaining [We are losing money!]".format(bstr)
        else:
            subject = "${} remaining [We are saving money!]".format(bstr)
        self.send(send_to, subject, html)

    def Error(self, data):
        send_to = self.email["user"]
        subject = "Budget Check Error"
        body = "Error:<br>"+'<br>'.join(data)
        self.send(send_to, subject, body)


    def processData(self, data):
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
        title.string = title.text.replace("[Date]", self.date.getDate().strftime('%B'))
        if not self.date.isCurrentMonthAndYear():
            title.string = "---Final " + title.string + "---"

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
        for item in top:
            row = soup.new_tag('tr')
            cell1 = soup.new_tag('td')
            cell1.string = item['name'].replace('  ', ' ')
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

