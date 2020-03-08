from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

from typing import Dict

import numexpr as ne

from Sheets import *
from datetime import datetime

app = Flask(__name__)

def add(body, resp):
    restaurant = body[0].title()
    subtotals: List[float] = []
    members: List[Member] = []
    for i in range(1, len(body) - 1):
        parts = body[i].split(' ')
        members.append(Member(parts[0]))
        if parts[1].isnumeric():
            subtotals.append(float(parts[1]))
        else:
            subtotals.append(ne.evaluate(parts[1]))

    total : float = float(body[-1])
    Order.splitTotal(members, subtotals, total)

    sheets : Sheets = Sheets()
    balances: Dict[str, float] = sheets.add(Order(datetime.now(), restaurant, members, total))
    resp.message("\nAdded order from %s for a total of $%.2f" % (restaurant, total))
    excessive = {key : balances[key] for key in balances if balances [key] > 100}
    return excessive


@app.route("/sms", methods = ['GET', 'POST'])
def sms():
    print(request.form['From'])
    print(request.form['Body'])

    body : List[str] = request.form['Body'].split('\n')
    command : str = body[0].title()

    resp: MessagingResponse = MessagingResponse()

    if command == "XYZ":
        pass
    else:
        excessive = add(body, resp)
        contacts = {}
        with open('Contacts.txt', 'r') as raw_contacts:
            contacts_list : List[str] = raw_contacts.readlines()
            for contact in contacts_list:
                contact_parts = contact.split(', ')
                contacts[contact_parts[0]] = contact_parts[1]
        for contact in excessive:
            resp.message(to="+1 (404) 940-7862‬", body = ("'s%s current balance is %.2f" % (contact, excessive[contact])))

    return str(resp)

    # resp : MessagingResponse = MessagingResponse()
    # resp.message(to="+1 (404) 940-7862‬", body = "testing multiple receivers")
    # resp.message(to="+1 (310) 402-6028‬", body = "testing multiple receivers")
    # resp.message(to="+1 (909) 548-5358‬", body = "testing multiple receivers")
    # return str(resp)

if __name__ == "__main__":
    app.run(debug=True)