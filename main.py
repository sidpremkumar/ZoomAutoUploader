from __future__ import print_function
import datetime
from datetime import timedelta
import pickle
import os.path
import base64
import re

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from piazza_api import Piazza

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

PIAZZA_EMAIL = os.environ["PIAZZA_EMAIL"]
PIAZZA_PASSWORD = os.environ["PIAZZA_PASSWORD"]
PIAZZA_CLASS_NETWORK_ID = os.environ["PIAZZA_CLASS_NETWORK_ID"]

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('./zoomautouploader/token.pickle'):
        with open('./zoomautouploader/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'redentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    try:
        now = datetime.datetime.now()
        fifteen_min_ago = now - timedelta(seconds=900) # 15 minutes
        query = "after: {0}".format(fifteen_min_ago.strftime('%s'))
        results = service.users().messages().list(userId='me', q=query).execute()

        handle_result(results, service)

        pageToken = None
        if 'nextPageToken' in results:
            pageToken = results['nextPageToken']

        while pageToken:
            results = service.users().messages().list(userId='me', q=query, maxResults=511, pageToken=pageToken).execute()
            handle_result(results, service)
            if 'nextPageToken' in results:
                pageToken = results['nextPageToken']
            else:
                break
        
        print("Sucsessfull Run!")
    except Exception as err: 
        print(f"Error!: {err}")


def handle_result(results, service):
    """Helper function to loop over message to see if its a zoom one"""
    if not 'messages' in results:
        # If there are no messages in the result
        return
    for message in results['messages']:
        message_contents = service.users().messages().get(id=message['id'], userId='me', format="full", metadataHeaders=None).execute()
        headers = message_contents["payload"]["headers"]
        subject = [i['value'] for i in headers if i["name"]=="Subject"]
        if "Zoom Meeting is now available" in subject[0] and "Cloud Recording" in subject[0]:
            pubish_to_piazza(message_contents)

def pubish_to_piazza(message_contents):
    # Get the meeting URL + meeting password
    message_body = base64.urlsafe_b64decode(message_contents["payload"]["body"]["data"]).decode("utf-8").replace("&amp;", "&")
    meeting_url = re.findall('(https?://[^\s]+)', message_body)[2]
    meeting_password = re.findall(r'Access Password: (.{8})', message_body)[0]

    # Post them to Piazza
    piazza_message_content = f"Recording URL: {meeting_url}\nMeeting Password: {meeting_password}"
    piazza_client = Piazza()
    piazza_client.user_login(email=PIAZZA_EMAIL, password=PIAZZA_PASSWORD)
    piazza_class = piazza_client.network(PIAZZA_CLASS_NETWORK_ID)
    piazza_class.create_post(post_type="note", post_folders=["logistics"], post_subject="New Recording Available", post_content=piazza_message_content)

    print("Uploaded new recording to Piazza!")

if __name__ == '__main__':
    main()