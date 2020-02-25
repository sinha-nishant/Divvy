class Order:
    def __init__(self, restaurant, transaction_date, members):
        # String name of restaurant
        self.__restaurant = restaurant
        # Date object of when transaction occurred
        self.__date = transaction_date
        # List of Member objects
        self.__members = members

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