from __future__ import print_function

import base64
import email
import pickle
import os.path
import re

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

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

    orders = []
    for i in range(len(messages)):
        message = service.users().messages().get(userId=user_id, id=messages[i]['id']).execute()
        orders.append(message)

    # Parts is of size 2, but the second is only graphics
    parts = orders[0]['payload']['parts']
    part0 = parts[0]['body']['data']
    body = base64.urlsafe_b64decode(part0)
    em = email.message_from_bytes(body).as_string()
    # print(em)

    # Try to understand this line
    p = re.compile('\$\d+(?:\.\d+)?')
    # print(p.findall(em))

    print(re.split('- For: \w+ \w+ -', em)[3])

    # print(em)

main()