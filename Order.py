from typing import List
from datetime import datetime
from Member import Member
class Order:
    def __init__(self, transaction_date : datetime, restaurant : str, members : List[Member], total: float):
        # String name of restaurant
        self.__restaurant : str = restaurant
        # Date object of when transaction occurred
        self.__date : datetime = transaction_date
        # List of Member objects
        self.__members : List[Member] = members
        # Float total value of order with tax
        self.__total : float = total

    def setRestaurant(self, restaurant : str):
        self.__restaurant = restaurant

    # Returns name of restaurant
    def getRestaurant(self) -> str:
        return self.__restaurant

    def setMembers(self, members : List[Member]):
        self.__members = members

    # Returns list of participants
    def getMembers(self) -> List[Member]:
        return self.__members

    def setDate(self, transaction_date : datetime):
        self.__date = transaction_date

    # Returns date of transaction
    def getDate(self) -> datetime:
        return self.__date

    # Returns total price of order with tax
    def getTotal(self) -> float:
        return self.__total

    def __str__(self) ->  str:
        message = "Transaction Date: " +  str(self.__date)
        message += "\nRestaurant: " + self.__restaurant
        message += "\nTotal: $" + str(round(self.getTotal(), 2)) + '\n'
        for member in self.__members:
            message += "\n" + str(member)
        return message