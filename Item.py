class Item:
    def __init__(self, name, quantity, unit_price):
        # String name of item
        self.__name = name
        # Integer quantity of item
        self.__quantity = quantity
        # Float price for a single unit
        self.__unit_price = unit_price

    def getName(self):
        return self.__name

    def getQuantity(self):
        return self.__quantity

    def getUnitPrice(self):
        return self.__unit_price

    def setName(self, name):
        self.__name = name

    def setQuantity(self, quantity):
        self.__quantity = quantity

    def setUnitPrice(self, unit_price):
        self.__unit_price = unit_price