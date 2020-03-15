from datetime import datetime
from Order import Order
from Member import Member
from Item import Item
from Sheets import Sheets
def main():
    #def __init__(self, transaction_date: datetime, restaurant: str, members: List[Member], total: float):
    date = "2020/03/14"
    date= datetime.strptime(date, '%Y/%m/%d')
    restaurant= 'myTest'
    #def __init__(self, name: str = "", items: List[Item] = None, totalWithTax: float = 0):
    members=[]
    #def __init__(self, name: str = "", quantity: int = 0, unit_price: float = 0):
    item1 = Item("item1", 1, 0.01)
    item2 = Item("item2", 1, 0.01)
    item3 = Item("item3", 1, 0.02)
    member1= Member("NewPerson1", [item1], 0.0125)
    member2 = Member("Nishant", [item2], 0.0125)
    member3 = Member("NewPerson2", [item3], 0.025)
    members.append(member1)
    members.append(member2)
    members.append(member3)
    myOrder= Order(date, restaurant, members, 0.05)
    mySheet= Sheets()
    mySheet.add(myOrder)
main()