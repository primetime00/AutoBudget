import json

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

    def getBrowserPath(self):
        return self.data["browser"]["path"]

    def getBrowserName(self):
        return self.data["browser"]["name"]

    def getBrowserTitle(self):
        return self.data["browser"]["title"]