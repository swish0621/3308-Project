import os 
import dotenv
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta

load_dotenv()

# load credentials from .env 
client_id = os.getenv("TWITCH_CLIENT_ID")
client_secret = os.getenv("TWITCH_CLIENT_SECRET")
access_token = os.getenv("TWITCH_ACCESS_TOKEN")
expiration_date = os.getenv("EXPIRES")

# retrieve a new access token and update the .env 
# with the token and exipration 
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

    #pull info from response
    new_token = response.json()["access_token"]
    expiration_seconds = response.json()["expires_in"]
    expiration = datetime.now() + timedelta(seconds=expiration_seconds)

    # call update env to add new credentials
    update_env(new_token, expiration.isoformat())
    # update enviornment 
    os.environ["TWITCH_ACCESS_TOKEN"] = new_token
    os.environ["EXPIRES"] = expiration.isoformat()
    return 


# helper to update the .env when a new access token is fetched 
def update_env(new_token, expiration ):
    lines = []
    # copy .env except for token info / append new info
    with open(".env", "r") as file:
        for line in file: 
            if not (line.startswith("TWITCH_ACCESS_TOKEN=") or
                line.startswith("EXPIRES=")):
                lines.append(line)
        lines.append(f"TWITCH_ACCESS_TOKEN={new_token}\n")
        lines.append(f"EXPIRES={expiration}\n")

    # rewrite .env from copy 
    with open(".env", "w") as file:
        file.writelines(lines)

# helper to check if token is expired for use in queries
def is_token_expired():
    return datetime.now() >= datetime.fromisoformat(expiration_date)
