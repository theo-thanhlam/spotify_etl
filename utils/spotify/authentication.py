import os
from dotenv import load_dotenv
import json
import requests
from typing import Dict
from .. import logger

load_dotenv(dotenv_path=".env")

#Constants
__SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
__SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

#Main API routes
SPOTIFY_API_URL_PREFIX = "https://api.spotify.com/v1"


def get_token(client_id:str=__SPOTIFY_CLIENT_ID, client_secret:str=__SPOTIFY_CLIENT_SECRET):
    """
    Retrieves a Spotify access token.

    Params:
        client_id (str): The Spotify Client ID.
        client_secret (str): The Spotify Client Secret.

    Returns:
        response_json (Dict(str, str, int)): A dictionary containing:
            - access_token (str): The Spotify access token.
            - token_type (str): The type of authorization token (e.g., "Bearer").
            - expires_in (int): The token's expiration time in seconds (typically 3600).
    """
    URL_TOKEN = "https://accounts.spotify.com/api/token"
    headers = {
        "Content-Type":"application/x-www-form-urlencoded"
    }
    payload ={
        "grant_type":"client_credentials",
        "client_id":client_id,
        "client_secret":client_secret
    }
    try:
        response = requests.post(url=URL_TOKEN, headers=headers, data=payload)
        response_json = json.loads(response.content)
        logger.info("Get new spotify token")
        return response_json
    except Exception as err:
        print(err)
        return None

def get_auth_header(token: Dict[str,any]) -> Dict[str, str]:
    """
    Retrieves Spotify authorization header
    
    Params:
        token (Dict[str,any]) : token dictionary from get_token()
        
    Returns:
        authorization_header (Dict(str,str)): Bearer authorization header

    """
    authorization_header = {"Authorization": f"Bearer {token['access_token']}"}
    return authorization_header   