import json, os
from Singleton import Singleton
from Dates import Dates

class Configuration(Singleton):

    def firstTime(self, **kwargs):
        with open('Config\\configuration.json', mode='r') as f:
            jData = f.read()
        self.data = json.loads(jData)
        if "settings" not in self.data:
            self.addSettings({"lookBackMonths": 1, "currentDate":Dates.empty()})
        else:
            if "lookBackMonths" not in self.data["settings"]:
                self.addSettings({"lookBackMonths": 1})
            if "currentDate" not in self.data["settings"]:
                self.addSettings({"currentDate":Dates.empty()})
            else:
                date = Dates.string(self.data["settings"]["currentDate"])
                self.addSettings({"currentDate": date})

    def findBank(self, name):
        for bank in self.data["banks"]:
            if bank["name"] == name:
                return bank
        return None

    def getBanks(self):
        return self.data["banks"]

    def getHTMLParser(self, bank):
        bank = self.findBank(bank)
        if bank == None:
            return None
        return bank["parser"]

    def getBudget(self):
        return self.data["budget"]

    def getEmail(self):
        return self.data["email"]

    def getSettings(self):
        return self.data["settings"]

    def hasBrowser(self):
        if "browser" not in self.data:
            return False
        if "path" not in self.data["browser"]:
            return False
        if os.path.exists(self.data["browser"]["path"]):
            return True
        return False

    def installBrowser(self, name, title, path):
        self.data["browser"] = {
            "name":name,
            "title":title,
            "path":path
        }
        self.save()

    def getBrowserPath(self):
        return self.data["browser"]["path"]

    def getBrowserName(self):
        return self.data["browser"]["name"]

    def getBrowserTitle(self):
        return self.data["browser"]["title"]

    def save(self):
        with open('Config\\configuration.json', mode='w') as f:
            json.dump(self.data, f, sort_keys=True, indent=4, separators=(',', ': '))

    def addSettings(self, settings):
        if "settings" not in self.data:
            self.data["settings"] = {}
        for key, value in settings.items():
            self.data["settings"][key] = value
