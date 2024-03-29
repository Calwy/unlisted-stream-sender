from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import pickle
import os
import requests
import asyncio

CHANNEL_ID = 'YOUROWNCHANNELID'  # Replace with your YouTube channel ID
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly'] # scope set to read only, can change this
CLIENT_SECRETS_FILE = 'client_secret.json' # import from google by creating an OAuth2.0 Client ID 


async def check_livestatus():       
    credentials=None
    if os.path.exists('token.pickle'):
        print('Loading Credentials from File...')
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)

        if not credentials or not credentials.valid:
            print('Credentials are not valid or not found.')
            print('refreshing token...')
            credentials.refresh(Request())


        try:
            youtube = build('youtube', 'v3', credentials=credentials)
            request = youtube.liveBroadcasts().list(
                part='snippet',
                mine=True,
            )
            response = request.execute()
            if 'items' in response:     
                for item in response['items']:
                    snippet = item['snippet']
                    if 'actualEndTime' not in snippet:          # to check if videos found contain the tag actualEndTime, this shows if a video is live or not
                        print('You are currently online')
                        return True

                    else: 
                        print('You are offline')
                        return False
           

        except HttpError as e:
            print(f'HTTP error occurred: {e}')
            return False

def refresh_credentials(credentials):   # function to ensure you dont have to authorize everytime
    try:
        credentials.refresh(Request())
        print('Token refreshed successfully.')
    except Exception as e:
        print(f'Error refreshing token: {e}')


def refresh_token():        # gets a new token.pickle
    credentials = None
    print('Fetching new token')
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    flow.run_local_server(port=8080,prompt="consent") # this can be changed to any port of your preference
    credentials=flow.credentials
                            
    with open("token.pickle","wb")as f:
        print("Saving creds...")
        pickle.dump(credentials,f)
        return credentials


def get_unlisted_live_stream_url():  # Creates youtube link based on current live stream
    title_list=[]
    guilded_data=[]
    credentials = None
    if os.path.exists('token.pickle'):
        print('Loading Credentials from File...')
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
                print('refreshing credentials...')
                refresh_credentials(credentials)
        else:
            print('Credentials are not valid or not found.')
            print('refreshing token..')
            credentials=refresh_token()
    
    try:
        youtube = build('youtube', 'v3', credentials=credentials)
        request = youtube.liveBroadcasts().list(
            part='snippet',
            mine=True,
        )
        response = request.execute()
        
        if 'items' in response:
            for item in response['items']:
                snippet = item['snippet']
                title_list.append(snippet['title'])
                urlextract=snippet['thumbnails']['default']['url']
                videoid_=urlextract.split('/vi/')[1].split('/default_live.jpg')[0]
                if snippet['liveChatId']:
                    # Retrieve the live broadcast URL from the url tag 
                    live_stream_url = f'https://www.youtube.com/watch?v={videoid_}'
                    if len(guilded_data)<2:         # appends only the title and stream url
                        guilded_data.append(live_stream_url)
                        guilded_data.append(title_list[0])
                    return deploy_messsage(guilded_data)

        return False
    
    except HttpError as e:
        print(f'HTTP error occurred: {e}')
        return None

def deploy_messsage(guilded_data):
    webhook_url = 'YOUR WEBHOOK URL' # change this to your webhook url
    message = {
        'content': f'EDIT THIS TO CUSTOMISE YOUR MESSAGE\n',
        'embeds': [
            {
                'description': f':link: [PLACEHOLDER]({guilded_data[0]}):tv:\n' # change this to your message
                 f'Title: {guilded_data[1]}', # Title of your livestream *optional* 
                'color': 4692262  # Color code for neon green
            }
        ]
    }
    response = requests.post(webhook_url, json=message)

    if response.status_code == 200:
        print('Deployed Message!')


async def main():
    counter = 0
    unlisted_stream_run = False  # Flag variable to track if get_unlisted_live_stream_url() has run
    
    while True:
        status = await check_livestatus()
        if status and not unlisted_stream_run:
            get_unlisted_live_stream_url()
            unlisted_stream_run = True
            counter += 1
        elif not status:
            unlisted_stream_run = False  # Reset flag if not live
        await asyncio.sleep(60)


if __name__ == '__main__':
    asyncio.run(main())
