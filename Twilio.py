from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

from typing import Dict

import numexpr as ne

from Sheets import *
from datetime import datetime

from time import time as time_now

app = Flask(__name__)

def add(body : List[str], resp : MessagingResponse) -> Dict[str, float]:
    restaurant = body[0].strip().title()
    subtotals: List[float] = list()
    members: List[Member] = list()
    for i in range(1, len(body) - 1):
        parts = body[i].split(' ')
        members.append(Member(parts[0].strip()))
        if checkFloat(parts[1].strip()):
            subtotals.append(float(parts[1].strip()))
        else:
            subtotals.append(ne.evaluate(parts[1].strip()))

    total : float = float(body[-1].strip())
    Order.splitTotal(members, subtotals, total)

    sheets : Sheets = Sheets()
    balances: Dict[str, float] = sheets.add(Order(datetime.now(), restaurant, members, total))
    resp.message("\nAdded order from %s for a total of $%.2f" % (restaurant, total))
    if not balances:
        return dict()
    print("Balances", balances)
    excessive : Dict[str : float] = dict()
    if 'Arjun' in balances.keys() and balances['Arjun'] > 150:
        excessive['Arjun'] = balances['Arjun']
    if 'Param' in balances.keys() and balances['Param'] > 150:
        excessive['Param'] = balances['Param']
    return excessive

def credit(name : str, value : float, resp : MessagingResponse, contacts : Dict):
    sheets : Sheets = Sheets()
    sheets.withdraw(name, value)
    resp.message("Credited $%.2f to your balance" % value)
    resp.message(to = contacts['Nishant'], body = "%s credited $%.2f to their balance" % (name, value))

def checkFloat(value : str) -> bool:
    value = value.replace(".", "", 1).strip()
    if value.isdigit():
        return True
    elif value[0] == "-" and value[1:].isdigit():
        return True
    return False

@app.route("/", methods = ['GET', 'POST'])
def sms():
    phone = request.form['From'][:2] + " (" + request.form['From'][2:5] + ") " + request.form['From'][5:8] + "-" + request.form['From'][8:]
    print("Phone:", phone)

    contacts = {"Param": os.environ.get("PARAM"), "Arjun": os.environ.get("ARJUN"), "Nishant": os.environ.get("NISHANT")}
    for key in contacts:
        contacts[key] = contacts[key].strip().encode('ascii', 'ignore').decode('ascii', 'ignore')

    body : List[str] = request.form['Body'].split('\n')
    for i in range(len(body)):
        body[i] = body[i].strip()

    command : str = body[0].title()

    resp: MessagingResponse = MessagingResponse()

    if command == "Credit":
        if checkFloat(body[1]):
            print(contacts)
            for key in contacts:
                if contacts[key] == phone:
                    print("Found:", key, phone)
                    start = time_now()
                    credit(key, float(body[1]), resp, contacts)
                    print("Seconds to credit:", time_now() - start)
        else:
            resp.message("The first line of your message must be 'Credit/credit' and "
                         "the second line must be a number indicating how much you would like to credit your balance by")
    else:
        if phone == contacts['Nishant']:
            start = time_now()
            excessive : Dict[str : float] = add(body, resp)
            print("Time to add:", time_now() - start)
            for contact in excessive:
                phone : str = contacts[contact]
                resp.message(to = phone, body = "Your current balance is %.2f" % excessive[contact])
        else:
            resp.message("You only have permission to credit your balance")

    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)