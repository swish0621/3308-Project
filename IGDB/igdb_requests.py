import os 
import dotenv
from dotenv import load_dotenv
import requests
import datetime

load_dotenv()

# load credentials from .env 
client_id = os.getenv("TWITCH_CLIENT_ID")
client_secret = os.getenv("TWITCH_CLIENT_SECRET")
access_token = os.getenv("TWITCH_ACCESS_TOKEN")

def get_access_token():
    url = "https://id.twitch.tv/oauth2/token"

    # create dictionary for POST request
    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
    # send request for access token
    # Response: 200 = OK
    # Response: 400 = Bad request
    # Response: 401 = Unauth
    
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()

print(get_access_token())