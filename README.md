# unlisted-stream-sender
A python file that grabs the title of your unlisted Youtube livestream and posts it on your Guilded server via a webhook 

Creating a OAuth Client ID:
  - Go to console.cloud.google.com
  - create a new project
  - head over to the library
  - select 'YouTube Data API v3' and enable
  - head over to the credential section and create a consent screen
  - then create a OAuth 2.0 Client ID and save the .json file


Creating a webhook URL:
  - Go to the channel you want the webhook you want to deploy the webhook on
  - right click > settings > webhooks > create a webhook 
  - keep the webhook url , you will need it

Using the python file:
  - I have added comments in the code showing where you place the .json file as well as where you paste your webhook url you obtain from guilded
  - the scope can be adjusted to whatever you need it to be

**IMPORTANT:** 
I set the file to be constantly running every minute to check your channel to see if you're live or not. It will print out messages on the console saying if you are live or not. 

Python libraries needed :
  - google-api-python-client
  - google-auth-oauthlib
