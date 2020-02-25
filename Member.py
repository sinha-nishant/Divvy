class Member:
    def __init__(self, name = "", items = None):
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

    def getTotal(self):
        total = 0
        for item in self.__items:
            item_value = item.getUnitPrice() * item.getQuantity()
            total += item_value
        return total

    def __repr__(self):
        message = ""
        message += self.__name + " ordered:"
        for item in self.__items:
            message += "\n\t" + str(item)
        message += "\nFor a total of $" + str(self.getTotal())
        return message