class Item:
    def __init__(self, name : str = "", quantity : int = 0, unit_price : float = 0):
        # String name of item
        self.__name : str = name
        # Integer quantity of item
        self.__quantity : int = quantity
        # Float price for a single unit
        self.__unit_price : float = unit_price

    def getName(self) -> str:
        return self.__name

    def getQuantity(self) -> int:
        return self.__quantity

    def getUnitPrice(self) -> float:
        return self.__unit_price

    def setName(self, name : str):
        self.__name = name

    def setQuantity(self, quantity : int):
        self.__quantity = quantity

    def setUnitPrice(self, unit_price : float):
        self.__unit_price = unit_price

    def __repr__(self) -> str:
        message = ""
        message += "Food: " + self.__name
        message += "\n\tPrice: $" + str(self.__unit_price)
        message += "\n\tQuantity: " + str(self.__quantity)
        return message