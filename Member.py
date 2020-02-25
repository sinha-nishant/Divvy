class Member:
    def __init__(self, name, items):
        # String name of user
        self.__name = name
        # List of Item objects
        self.__items = items

    def getName(self):
        return self.__name

    def setName(self, name):
        self.__name = name

    def getItems(self):
        return self.__items

    def setItems(self, items):
        self.__items = items