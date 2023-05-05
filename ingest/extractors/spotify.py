import requests

spotify_access_token = "$SPOTIFY_API_KEY"
spotify_base_url = "https://api.spotify.com/v1/"
headers = {"Authorization": f"Bearer {spotify_access_token}"}

def get_featured_playlists(limit=50, timestamp=None):
    url = f"{spotify_base_url}browse/featured-playlists?limit={limit}"
    if timestamp:
        url += f"&timestamp={timestamp}"
    response = requests.get(url, headers=headers)
    return response.json()

def get_track_features(track_id):
    response = requests.get(
        f"https://api.spotify.com/v1/audio-features/{track_id}",
        headers=headers
    )
    return response.json()

def get_playlist_data(playlist_id):
    response = requests.get(
        f"https://api.spotify.com/v1/playlists/{playlist_id}",
        headers=headers
    )
    return response.json()

def get_playlist_tracks(playlist_id):
    url = f"{spotify_base_url}playlists/{playlist_id}/tracks"
    response = requests.get(url, headers=headers)
    return response.json()