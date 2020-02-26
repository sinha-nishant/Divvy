class Item:
    def __init__(self, name : str = "", quantity : int = 0, unit_price : float = 0):
        # String name of item
        self._name : str = name
        # Integer quantity of item
        self._quantity : int = quantity
        # Float price for a single unit
        self._unit_price : float = unit_price

    def getName(self) -> str:
        return self._name

    def getQuantity(self) -> int:
        return self._quantity

    def getUnitPrice(self) -> float:
        return self._unit_price

    def setName(self, name : str):
        self._name = name

    def setQuantity(self, quantity : int):
        self._quantity = quantity

    def setUnitPrice(self, unit_price : float):
        self._unit_price = unit_price

    def __repr__(self) -> str:
        message = ""
        message += "Food: " + self._name
        message += "\n\t\tPrice: $" + str(self._unit_price)
        message += "\n\t\tQuantity: " + str(self._quantity)
        return message