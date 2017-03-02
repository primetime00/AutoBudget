import json, os

class Configuration:
    __instance = None
    def __new__(cls, *args, **kwargs):
        if Configuration.__instance is None:
            Configuration.__instance = object.__new__(cls)
            Configuration.__instance.firstTime()
        return Configuration.__instance

    def firstTime(self):
        with open('Config\\configuration.json', mode='r') as f:
            jData = f.read()
        self.data = json.loads(jData)

    def findBank(self, name):
        for bank in self.data["banks"]:
            if bank["name"] == name:
                return bank

    def getBanks(self):
        return self.data["banks"]

    def getBudget(self):
        return self.data["budget"]

    def getEmail(self):
        return self.data["email"]

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
