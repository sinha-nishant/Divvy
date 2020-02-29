import base64, email, pickle, os.path, re
from typing import List, Dict
from datetime import datetime
from time import time as time_now

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from Order import Order
from Member import Member
from Item import Item

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
from Sheets import *

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    start = time_now()
    # Personal label ID for DoorDash
    label_id : str = 'Label_1748595172489237696'
    # Retrieves most recent email with the label DoorDash
    response = service.users().messages().list(userId = 'me', labelIds = label_id, maxResults = 7).execute()
    order = service.users().messages().get(userId = 'me', id = response['messages'][5]['id']).execute()
    print('API Response time:', time_now() - start, 'seconds')
    start = time_now()

    # Parts is of size 2, but the second is only graphics
    parts : List[Dict] = order['payload']['parts']
    part0 : str = parts[0]['body']['data']
    body = base64.urlsafe_b64decode(part0)
    em : str = email.message_from_bytes(body).as_string()
    restaurant : str = em[:em.index('Total')].strip().split('\n')[-1].strip()
    transaction_date : str = order['payload']['headers'][1]['value'].split(';')[-1].strip()
    del order

    findNames = re.compile('- For: \w+ \w+ -')
    raw_names: List[str] = findNames.findall(em)
    member_names = re.findall('\w+ \w+', "".join(raw_names))

    subOrders : List[str] = re.split('- For: \w+ \w+ -', em)
    dollar = re.compile('\$\d+(?:\.\d+)?')
    total_cost = float(dollar.search(subOrders[0]).group().lstrip('$'))
    del subOrders[0]

    subOrders[-1] = subOrders[-1][:subOrders[-1].index('Subtotal')]

    findItem = re.compile("\dx\w+.*")

    memberToItems : Dict[str: List[Item]] = dict()
    for i in range(len(member_names)):
        prices : List[float] = [float(price.lstrip('$')) for price in dollar.findall(subOrders[i])]
        quantities : List[int] = []
        foods : List[str] = []
        raw_items : List[str] = findItem.findall(subOrders[i])

        for item in raw_items:
            elements : List[str] = item.split('x', 1)
            quantities.append(int(elements[0]))
            foods.append(elements[1])

        items : List[Item] = []
        for j in range(len(foods)):
            items.append(Item(foods[j], quantities[j], prices[j]))

        memberToItems[member_names[i]] = items

    members : List[Member] = [Member(key, memberToItems[key]) for key in memberToItems.keys()]

    subtotal = sum(member.getNoTaxTotal() for member in members)

    for i in range(len(members)):
        members[i].setTotal((members[i].getNoTaxTotal()/subtotal) * total_cost)

    order : Order = Order(datetime.strptime(transaction_date, '%a, %d %b %Y %H:%M:%S %z (%Z)'), restaurant, members, total_cost)
    print(order)
    print('Program time excluding API Response time:', time_now() - start, 'seconds')
    mySheet= Sheets(order)
    #mySheet.add_sheet("Total Amounts")
    # mySheet.remove(0,mySheet.getSize())
    #mySheet.create("Totals")
    pprint(len(mySheet.get_all_sheets()))
    pprint(mySheet.get_all_sheets()[1].get_all_records())
main()