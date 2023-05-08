# Music Analytics Data Pipeline

This project aims to build an end-to-end data pipeline for music analytics. The pipeline fetches data from various music-related APIs, such as Spotify, MusicBrainz, and the Billboard Charts, and combines them to gain insights into the popularity and characteristics of tracks and artists.

The data pipeline consists of three main components:

1. **Ingestion with the extractors**: Data is extracted from the APIs, cleaned, and stored in Parquet format in Google Cloud Storage.
2. **DBT**: Data is transformed and modeled using dbt (Data Build Tool) to create fact and dimension tables in a BigQuery data warehouse.
3. **Airflow**: The entire process is orchestrated and scheduled using Apache Airflow.

The data flow starts with fetching raw data from the APIs using the extractors. The raw data is then cleaned and transformed into Parquet format, which is stored in Google Cloud Storage. The Parquet files are loaded into BigQuery, where the data is modeled using dbt to create fact and dimension tables. Finally, the entire pipeline is scheduled and managed using Apache Airflow.

![Data flow diagram](https://i.imgur.com/DgmxND6.png)

To run the project, follow these high-level steps:

1. Set up and configure the API keys, GCP credentials, and environment variables for the project.
2. Deploy the data extraction script, which fetches data from the APIs and stores it in Parquet format in GCS.
3. Configure dbt and create the required models for fact and dimension tables in BigQuery.
4. Set up and configure Apache Airflow to orchestrate and schedule the data pipeline.

For detailed instructions on how to run each part, refer to the individual README files for the three components.

Below is the data model for this project:

### dim_artist (Dimension Table)
artist_id (PK)
artist_name
artist_popularity
artist_followers
artist_spotify_id
artist_musicbrainz_id


### dim_track (Dimension Table)
track_id (PK)
track_name
track_popularity
track_spotify_id
track_musicbrainz_id
track_duration_ms
track_explicit
track_danceability
track_energy
track_key
track_loudness
track_mode
track_speechiness
track_acousticness
track_instrumentalness
track_liveness
track_valence
track_tempo
track_time_signature


### dim_playlist (Dimension Table)
playlist_id (PK)
playlist_name
playlist_description
playlist_spotify_id
playlist_total_tracks


### fact_artist_chart_ranking (Fact Table)
ranking_id (PK)
date (FK to dim_date.date)
artist_id (FK to dim_artist.artist_id)
chart_rank


### fact_track_chart_ranking (Fact Table)
ranking_id (PK)
date (FK to dim_date.date)
track_id (FK to dim_track.track_id)
chart_rank


### fact_playlist_tracks (Fact Table)
playlist_track_id (PK)
playlist_id (FK to dim_playlist.playlist_id)
track_id (FK to dim_track.track_id)

### dim_date (Dimension Table)
date (PK)
day
month
year
day_of_week
