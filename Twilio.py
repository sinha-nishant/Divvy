from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def sms():
    print(request.form['Body'])
    """Respond to incoming messages with a friendly SMS."""
    # Start our response
    resp : MessagingResponse = MessagingResponse()

    # Add a message
    resp.message("Dis bruh gotta get some ho*s")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)