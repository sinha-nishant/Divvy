import pymongo, os
from Order import Order
from typing import Dict

class DB:
    password : str = os.environ['MONGODB']
    client : pymongo.MongoClient = pymongo.MongoClient("mongodb+srv://nishant:{}@firstcluster-b8uyp.gcp.mongodb.net/test?retryWrites=true&w=majority".format(password))
    # Only working with the Orders database
    orders = client['Orders']
    # Need to specify session because atomicity is necessary
    # Multiple document operations aren't atomic by default
    @staticmethod
    def add(order : Order):
        memberCosts : Dict[str, float] = order.getMemberCosts()
        with DB.client.start_session() as session:
            # Add order to transactions collection
            transactions = DB.orders['Transactions']
            transactions.insert_one({
                'Date' : order.getDate(),
                'Item' : order.getItem(),
                'Total' : order.getTotal(),
                'Members' : memberCosts
                }, session = session)

            # Update balances in Members collection
            members = DB.orders['Members']
            # No need to track how much my balance is
            memberCosts.pop('Nishant')
            for member_name in memberCosts:
                members.update_one(
                    {'Name' : member_name},
                    {'$inc' : {'Balance' : memberCosts[member_name]}},
                    upsert = True, session = session)

            # Returns list of dictionaries of members with excessive balances
            return list(members.find({'$and': [{'Name': {'$in': list(memberCosts.keys())}}, {'Balance': {'$gt': 100}}]}))

    # Don't need to specify session because single document operations are atomic
    @staticmethod
    def credit(name : str, value : float) -> float:
        members = DB.orders['Members']
        new_balance : float = members.find_one_and_update({'Name' : name}, {'$inc' : {'Balance' : -value}}, projection = {'Balance' : 1, '_id' : 0}, upsert = True, return_document = pymongo.ReturnDocument.AFTER)['Balance']
        return new_balance