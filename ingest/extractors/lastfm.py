import requests

lastfm_api_key = "$LASTFM_API_KEY"
lastfm_base_url = "http://ws.audioscrobbler.com/2.0/"


def get_artist_info_lastfm(artist_name):
    url = f"{lastfm_base_url}?method=artist.getinfo&artist={artist_name}&api_key={lastfm_api_key}&format=json"
    response = requests.get(url)
    return response.json()