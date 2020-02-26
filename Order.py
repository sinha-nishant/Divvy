from typing import List
from datetime import datetime
from Member import Member
class Order:
    def __init__(self, transaction_date : datetime, restaurant : str, members : List[Member], total: float):
        # String name of restaurant
        self._restaurant : str = restaurant
        # Date object of when transaction occurred
        self._date : datetime = transaction_date
        # List of Member objects
        self._members : List[Member] = members
        # Float total value of order with tax
        self._total : float = total

    def setRestaurant(self, restaurant : str):
        self._restaurant = restaurant

    # Returns name of restaurant
    def getRestaurant(self) -> str:
        return self._restaurant

    def setMembers(self, members : List[Member]):
        self._members = members

    # Returns list of participants
    def getMembers(self) -> List[Member]:
        return self._members

    def setDate(self, transaction_date : datetime):
        self._date = transaction_date

    # Returns date of transaction
    def getDate(self) -> datetime:
        return self._date

    # Returns total price of order with tax
    def getTotal(self) -> float:
        return self._total

    def __str__(self) ->  str:
        message = "Transaction Date: " +  str(self._date)
        message += "\nRestaurant: " + self._restaurant
        message += "\nTotal: $" + str(round(self.getTotal(), 2)) + '\n'
        for member in self._members:
            message += "\n" + str(member)
        return message