import base64, email, pickle, os.path, re
from typing import List, Dict
from datetime import datetime

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from Order import Order
from Member import Member
from Item import Item

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

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
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    user_id= 'me'

    # Call the Gmail API
    results = service.users().labels().list(userId = user_id).execute()
    label_id = results.get('labels')[3]['id']

    response = service.users().messages().list(userId = user_id, labelIds=label_id).execute()
    messages = []
    if 'messages' in response:
        messages.extend(response['messages'])

    while 'nextPageToken' in response:
        page_token = response['nextPageToken']
        response = service.users().messages().list(userId=user_id, labelIds=label_id, pageToken=page_token).execute()
        messages.extend(response['messages'])

    orders : List[Dict] = []
    for i in range(len(messages)):
        message = service.users().messages().get(userId=user_id, id=messages[i]['id']).execute()
        orders.append(message)

    # Parts is of size 2, but the second is only graphics
    parts : List[Dict] = orders[5]['payload']['parts']
    part0 : str = parts[0]['body']['data']
    body = base64.urlsafe_b64decode(part0)
    em : str = email.message_from_bytes(body).as_string()
    restaurant : str = em[:em.index('Total')].strip().split('\n')[-1].strip()
    transaction_date : str = orders[5]['payload']['headers'][1]['value'].split(';')[-1].strip()
    del orders, part0, body

    findNames = re.compile('- For: \w+ \w+ -')
    raw_names: List[str] = findNames.findall(em)
    member_names = re.findall('\w+ \w+', "".join(raw_names))

    subOrders : List[str] = re.split('- For: \w+ \w+ -', em)
    dollar = re.compile('\$\d+(?:\.\d+)?')
    total_cost = float(dollar.findall(subOrders[0])[0].lstrip('$'))
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

    members : List[Member] = []
    for key in memberToItems.keys():
        members.append(Member(key, memberToItems[key]))

    subtotal : int = 0
    for member in members:
        subtotal += member.getNoTaxTotal()

    for i in range(len(members)):
        members[i].setTotal((members[i].getNoTaxTotal()/subtotal) * total_cost)

    order : Order = Order(datetime.strptime(transaction_date, '%a, %d %b %Y %H:%M:%S %z (%Z)'), restaurant, members, total_cost)

    print(order)

main()