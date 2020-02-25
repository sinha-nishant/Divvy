from typing import List
from Item import Item
class Member:
    def __init__(self, name : str = "", items : List[Item] = None):
        # String name of user
        self.__name : str = name
        # List of Item objects
        self.__items : List[Item] = items

    # Returns name of participant
    def getName(self) -> str:
        return self.__name

    def setName(self, name : str):
        self.__name = name

    def getItems(self) -> List[Item]:
        return self.__items

    def setItems(self, items : List[Item]):
        self.__items = items

    # Returns total value of items a participant ordered
    def getTotal(self) -> float:
        total : int = 0
        for item in self.__items:
            item_value = item.getUnitPrice() * item.getQuantity()
            total += item_value
        return total

    def __repr__(self) -> str:
        message = ""
        message += self.__name + " ordered:"
        for item in self.__items:
            message += "\n\t" + str(item)
        message += "\nFor a total of $" + str(self.getTotal())
        return message