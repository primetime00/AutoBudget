class Singleton:
    __instance = {}
    def __new__(cls, *args, **kwargs):
        if cls not in Singleton.__instance:
            Singleton.__instance[cls] = object.__new__(cls)
            Singleton.__instance[cls].firstTime(kwargs=kwargs)
            v = Singleton.__instance
        return Singleton.__instance[cls]

    def firstTime(self, **kwargs):
        print("need definition")
