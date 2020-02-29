from twilio.rest import Client

class Twilio:
    # Your Account Sid and Auth Token from twilio.com/console
    # DANGER! This is insecure. See http://twil.io/secure
    def __init__(self):
        self._account_sid = 'AC72eeb1b57af6d87b55791a27776aa24f'
        self._auth_token = '2568cfab8f2634a5133a2f07f1e99e43'
        self._client = Client(self._account_sid, self._auth_token)

    def send_message(self):
        message = self._client.messages.create(
            body = 'Hi there!',
            from_ = '+15017122661',
            to = '+15558675310'
        )

        print(message.sid)