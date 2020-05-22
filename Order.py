from typing import List, Dict
from datetime import datetime
from Member import Member
class Order:
    def __init__(self, transaction_date : datetime, product : str, members : List[Member], total: float):
        # String name of /restaurant
        self._product : str = product
        # Date object of when transaction occurred
        self._date : datetime = transaction_date
        # List of Member objects
        self._members : List[Member] = members
        # Float total value of order with tax
        self._total : float = total

    def setProduct(self, product : str):
        self._product = product

    # Returns name of product/restaurant
    def getProduct(self) -> str:
        return self._product

    def setMembers(self, members : List[Member]):
        self._members = members

    # Returns dictionary of participants' costs
    def getMemberCosts(self) -> Dict[str, float]:
        membersDict : Dict[str, float] = dict()
        for member in self._members:
            membersDict[member.getName()] = member.getTotal()
        return membersDict

    def setDate(self, transaction_date : datetime):
        self._date = transaction_date

    # Returns date of transaction
    def getDate(self) -> datetime:
        return self._date

    # Returns total price of order with tax
    def getTotal(self) -> float:
        return self._total

    @staticmethod
    def splitTotal(members : List[Member], subtotals : List[float], totalWithTax : float):
        subtotal = sum(subtotals)
        for i in range(len(members)):
            members[i].setTotal((subtotals[i]/subtotal) * totalWithTax)

    def __str__(self) ->  str:
        message = "Transaction Date: " +  str(self._date)
        message += "\nProduct/Restaurant: " + self._product
        message += "\nTotal: $" + str(round(self.getTotal(), 2)) + '\n'
        for member in self._members:
            message += "\n" + str(member)
        return message