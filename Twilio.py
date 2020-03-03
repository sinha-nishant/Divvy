from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

from Sheets import *
from datetime import datetime

app = Flask(__name__)

@app.route("/sms", methods = ['GET', 'POST'])
def sms():
    print(request.form['Body'])

    body : List[str] = request.form['Body'].split('\n')
    command : str = body[0].title()

    resp: MessagingResponse = MessagingResponse()

    if command == "Add":
        restaurant = body[1].title()
        arjun_sub = float(body[2])
        param_sub = float(body[3])
        nishant_sub = float(body[4])
        subtotals = [arjun_sub, param_sub, nishant_sub]
        total = float(body[5])

        arjun = Member("Arjun Mitra")
        param = Member("Param Patel")
        nishant = Member("Nishant Sinha")
        members = [arjun, param, nishant]
        Order.splitTotal(members, subtotals, total)

        Sheets(Order(datetime.now(), restaurant, members, total))
        resp.message("Added order from %s for a total of %d" % (restaurant, total))

    elif command == "Custom Add":
        restaurant = body[1].title()
        subtotals : List[float] = []
        members : List[Member] = []
        for i in range(2, len(body) - 1):
            parts = body[i].split(', ')
            members.append(Member(parts[0]))
            subtotals.append(float(parts[1]))

        total = float(body[-1])
        Order.splitTotal(members, subtotals, total)

        Sheets(Order(datetime.now(), restaurant, members, total))
        resp.message("Added order from %s for a total of %d" % (restaurant, total))

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)