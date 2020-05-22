class Member:
    # totalWithTax should not be utilized if unknown
    # should instead be calculated through the Order class method splitTotal()
    def __init__(self, name : str = "", totalWithTax : float = 0):
        # String name of user
        self._name : str = name
        # Float total with tax
        self._totalWithTax = totalWithTax

    # Returns name of participant
    def getName(self) -> str:
        return self._name

    def setName(self, name : str):
        self._name = name

    def setTotal(self, total : float):
        self._totalWithTax = total

    def getTotal(self) -> float:
        return self._totalWithTax

    def __repr__(self) -> str:
        message = ""
        message += self._name + " spent " + "a total of $" + str(round(self.getTotal(), 2)) + " with tax\n"
        return message