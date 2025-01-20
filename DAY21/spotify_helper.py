import os
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

def get_access_token():
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials"
    }
    response = requests.post(url, headers=headers, data=data, auth=(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET))
    response.raise_for_status()
    return response.json()["access_token"]

def search_songs(query):
    access_token = get_access_token()
    url = "https://api.spotify.com/v1/search"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "q": query,
        "type": "track",
        "limit": 5
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()["tracks"]["items"]

def get_recommendations(mood):
    query = f"{mood} mood"
    songs = search_songs(query)
    recommendations = [(song["name"], song["artists"][0]["name"]) for song in songs]
    return recommendations
