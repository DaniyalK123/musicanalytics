-- models/fact_playlist_tracks.sql

{{ config(unique_key='playlist_id || "_" || track_id') }}

SELECT
    p.playlist_id,
    t.track_id
FROM {{ source('raw', 'music_data') }} AS m
JOIN {{ ref('dim_track') }} AS t ON m.track_spotify_id = t.track_spotify_id
JOIN {{ ref('dim_playlist') }} AS p ON m.playlist_spotify_id = p.playlist_spotify_id
JOIN {{ ref('dim_date') }} AS d ON m.date = d.date
