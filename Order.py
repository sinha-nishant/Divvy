class Order:
    def __init__(self, transaction_date, restaurant, members, total):
        # String name of restaurant
        self.__restaurant = restaurant
        # Date object of when transaction occurred
        self.__date = transaction_date
        # List of Member objects
        self.__members = members
        # Float total value of order with tax
        self.__total = total

    def setRestaurant(self, restaurant):
        self.__restaurant = restaurant

    def getRestaurant(self):
        return self.__restaurant

    def setMembers(self, members):
        self.__members = members

    def getMembers(self):
        return self.__members

    def setDate(self, transaction_date):
        self.__date = transaction_date

    def getDate(self):
        return self.__date

    def getTotal(self):
        return self.__total

    def __str__(self):
        message = "Transaction Date: " +  self.__date
        message += "\nRestaurant: " + self.__restaurant + '\n'
        message += "\nTotal: $" + str(round(self.getTotal(), 2))
        for member in self.__members:
            message += "\n" + str(member)
        return message