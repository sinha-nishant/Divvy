from typing import List
from Item import Item
class Member:
    def __init__(self, name : str = "", items : List[Item] = None, totalWithTax : float = 0):
        # String name of user
        self._name : str = name
        # List of Item objects
        self._items : List[Item] = items
        # Float total with tax
        self._totalWithTax = totalWithTax

    # Returns name of participant
    def getName(self) -> str:
        return self._name

    def setName(self, name : str):
        self._name = name

    def getItems(self) -> List[Item]:
        return self.__items

    def setItems(self, items : List[Item]):
        self._items = items

    def setTotal(self, total : float):
        self._totalWithTax = total

    # Returns total value of items a participant ordered
    def getNoTaxTotal(self) -> float:
        total : int = 0
        for item in self._items:
            item_value = item.getUnitPrice() * item.getQuantity()
            total += item_value
        return total

    def getTotal(self) -> float:
        return self._totalWithTax

    def __repr__(self) -> str:
        message = ""
        message += self._name + " ordered:"
        for item in self._items:
            message += "\n\t" + str(item)
        message += "\nFor a total of $" + str(round(self.getTotal(), 2)) + " with tax\n"
        return message