WITH track AS (
  SELECT DISTINCT
    track_id,
    track_name,
    danceability,
    energy,
    key,
    loudness,
    mode,
    speechiness,
    acousticness,
    instrumentalness,
    liveness,
    valence,
    tempo,
    duration_ms,
    time_signature
  FROM stg_raw_data
)

SELECT *
FROM track
