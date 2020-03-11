from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

from typing import Dict

import numexpr as ne

from Sheets import *
from datetime import datetime

app = Flask(__name__)

def add(body : List[str], resp : MessagingResponse) -> Dict[str, float]:
    restaurant = body[0].title()
    subtotals: List[float] = list()
    members: List[Member] = list()
    for i in range(1, len(body) - 1):
        parts = body[i].split(' ')
        members.append(Member(parts[0]))
        if parts[1].isdigit():
            subtotals.append(float(parts[1]))
        else:
            subtotals.append(ne.evaluate(parts[1]))

    total : float = float(body[-1])
    Order.splitTotal(members, subtotals, total)

    sheets : Sheets = Sheets()
    balances: Dict[str, float] = sheets.add(Order(datetime.now(), restaurant, members, total))
    resp.message("\nAdded order from %s for a total of $%.2f" % (restaurant, total))
    excessive : Dict[str : float] = dict()
    if balances['Arjun'] > 100:
        excessive['Arjun'] = balances['Arjun']
    if balances['Param'] > 100:
        excessive['Param'] = balances['Param']
    return excessive

def credit(name : str, value : float, resp : MessagingResponse, contacts : Dict):
    sheets : Sheets = Sheets()
    sheets.withdraw(name, value)
    resp.message("Credited $%.2f to your balance" % value)
    resp.message(to = contacts['Nishant'], body = "%s credited $%.2f to their balance" % (name, value))

def checkFloat(value : str) -> bool:
    value = value.replace(".", "", 1)
    if value.isdigit():
        return True
    elif value[0] == "-" and value[1:].isdigit():
        return True
    return False

@app.route("/sms", methods = ['GET', 'POST'])
def sms():
    contacts = dict()
    with open('Contacts.txt', 'r') as raw_contacts:
        contacts_list : List[str] = raw_contacts.readlines()
        for contact in contacts_list:
            contact_parts : List[str] = contact.split(', ')
            contacts[contact_parts[0]] = contact_parts[1].strip().encode('ascii', 'ignore').decode('ascii', 'ignore')

    body : List[str] = request.form['Body'].split('\n')
    for i in range(len(body)):
        body[i] = body[i].strip()

    command : str = body[0].strip().title()

    resp: MessagingResponse = MessagingResponse()

    if command == "Credit":
        if checkFloat(body[1]):
            phone = request.form['From'][:2] + " (" + request.form['From'][2:5] + ") " + request.form['From'][5:8] + "-" + request.form['From'][8:]
            for key in contacts:
                if contacts[key] == phone:
                    credit(key, float(body[1]), resp, contacts)
        else:
            resp.message("The first line of your message must be 'Credit/credit' and "
                         "the second line must be a number indicating how much you would like to credit your balance by")
    else:
        if request.form['From'] == contacts['Nishant']:
            excessive : Dict[str : float] = add(body, resp)
            for contact in excessive:
                phone : str = contacts[contact]
                resp.message(to = phone, body = "Your current balance is %.2f" % excessive[contact])
        else:
            resp.message("You only have permission to credit your balance")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)