from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

from Sheets import *

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def sms():
    print(request.form['Body'])

    body = request.form['Body'].split(' ')
    command = body[0]
    value = float(body[1])
    """Respond to incoming messages with a friendly SMS."""
    # Start our response
    resp : MessagingResponse = MessagingResponse()

    sheets = Sheets()
    sheets.withdraw('Arjun Mitra', value)

    resp.message("You credited $" + str(value))

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)