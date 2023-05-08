import os
import time
import pandas as pd
from datetime import datetime, timedelta
from google.cloud import storage
from extractors import *


BUCKET = os.environ.get("GCP_BUCKET")


# Calculate the dates for the last 3 months up to the current date, one date per week
start_date = datetime.now() - timedelta(weeks=12)
end_date = datetime.now()
date_range = [start_date + timedelta(weeks=x) for x in range((end_date - start_date).days // 7 + 1)]


# Calculate the dates for the last 3 months up to the current date, one date per week
start_date = datetime.now() - timedelta(weeks=12)
end_date = datetime.now()
date_range = [start_date + timedelta(weeks=x) for x in range((end_date - start_date).days // 7 + 1)]

# Fetch data from APIs
all_tracks_data = []

for date in date_range:
    timestamp = date.isoformat()

    # Get Billboard chart data
    billboard_chart_data = get_billboard_chart_data(date=date.strftime("%Y-%m-%d"))

    # Get featured playlists
    featured_playlists_data = get_featured_playlists(timestamp=timestamp)

    # Get track details from each featured playlist
    for playlist in featured_playlists_data["playlists"]["items"]:
        playlist_id = playlist["id"]
        playlist_tracks_data = get_playlist_tracks(playlist_id)

        # Get artist details from Last.fm, MusicBrainz, and chart data from Billboard
        for track_data in playlist_tracks_data["items"]:
            track = track_data["track"]
            track_name = track["name"]
            spotify_track_id = track["track"]["id"]
            track_features = get_track_features(spotify_track_id)
            playlist_data = get_playlist_data(playlist_id)
            artist_name = track["artists"][0]["name"]

            # Check if track is in Billboard Hot 100
            for entry in billboard_chart_data:
                if entry.title == track_name and entry.artist == artist_name:
                    # Get artist information from Last.fm
                    artist_info_lastfm = get_artist_info_lastfm(artist_name)
                    time.sleep(0.2)  # Respect Last.fm API rate limits

                    # Get artist information from MusicBrainz
                    artist_mbid = artist_info_lastfm["artist"]["mbid"]
                    musicbrainz_artist = get_musicbrainz_artist(artist_mbid)
                    time.sleep(1)  # Respect MusicBrainz API rate limits

                    # Combine track data, artist info, and chart data
                    track_metadata = {
                        "track_id": track["id"],
                        "track_name": track_name,
                        "artist_id": track["artists"][0]["id"],
                        "artist_name": artist_name,
                        "album_id": track["album"]["id"],
                        "album_name": track["album"]["name"],
                        "popularity": track["popularity"],
                        "artist_listeners": artist_info_lastfm["artist"]["stats"]["listeners"],
                        "artist_play_count": artist_info_lastfm["artist"]["stats"]["playcount"],
                        "artist_musicbrainz": musicbrainz_artist,
                        "chart_date": date.strftime("%Y-%m-%d"),
                        "chart_rank": entry.rank,
                        "track_danceability": track_features["danceability"],
                        "track_energy": track_features["energy"],
                        "track_key": track_features["key"],
                        "track_loudness": track_features["loudness"],
                        "track_mode": track_features["mode"],
                        "track_speechiness": track_features["speechiness"],
                        "track_acousticness": track_features["acousticness"],
                        "track_instrumentalness": track_features["instrumentalness"],
                        "track_liveness": track_features["liveness"],
                        "track_valence": track_features["valence"],
                        "track_tempo": track_features["tempo"],
                        "track_duration_ms": track_features["duration_ms"],
                        "track_time_signature": track_features["time_signature"],
                        "playlist_id": playlist_id,
                        "playlist_name": playlist_data["name"],
                        "playlist_description": playlist_data["description"],
                    }

                    all_tracks_data.append(track_metadata)
                    break
        time.sleep(1)  # Respect Spotify API rate limits


# Initialize the GCS client
storage_client = storage.Client()
bucket_name = BUCKET
bucket = storage_client.get_bucket(bucket_name)


# Create an empty DataFrame with the desired columns
columns = [
    "track_id",
    "track_name",
    "artist_id",
    "artist_name",
    "album_id",
    "album_name",
    "popularity",
    "artist_listeners",
    "artist_play_count",
    "artist_musicbrainz",
    "chart_date",
    "chart_rank",
    "track_danceability",
    "track_energy",
    "track_key",
    "track_loudness",
    "track_mode",
    "track_speechiness",
    "track_acousticness",
    "track_instrumentalness",
    "track_liveness",
    "track_valence",
    "track_tempo",
    "track_duration_ms",
    "track_time_signature",
    "playlist_id",
    "playlist_name",
    "playlist_description"
]
tracks_df = pd.DataFrame(columns=columns)

# Add each track's metadata to the DataFrame
for track_metadata in all_tracks_data:
    tracks_df = tracks_df.append(track_metadata, ignore_index=True)

# Save the DataFrame as Parquet files using a folder structure based on dates
for date in tracks_df["chart_date"].unique():
    date_folder = f"tracks_data/{date}"
    os.makedirs(date_folder, exist_ok=True)
    tracks_df[tracks_df["chart_date"] == date].to_parquet(f"{date_folder}/data.parquet", index=False)

# Save the DataFrame as Parquet files using a folder structure based on dates
# and upload the files to GCS
for date in tracks_df["chart_date"].unique():
    date_folder = f"tracks_data/{date}"
    os.makedirs(date_folder, exist_ok=True)
    parquet_file = f"{date_folder}/data.parquet"
    tracks_df[tracks_df["chart_date"] == date].to_parquet(parquet_file, index=False)

    # Upload the Parquet file to GCS
    blob = bucket.blob(f"{date_folder}/data.parquet")
    blob.upload_from_filename(parquet_file)

    # Remove the local Parquet file
    os.remove(parquet_file)

# Remove the local date folders
os.rmdir("tracks_data")
