WITH track AS (
  SELECT DISTINCT
    track_id,
    track_name,
    track_danceability,
    track_energy,
    track_key,
    track_loudness,
    track_mode,
    track_speechiness,
    track_acousticness,
    track_instrumentalness,
    track_liveness,
    track_valence,
    track_tempo,
    track_duration_ms,
    track_time_signature,
  FROM stg_raw_data
)

SELECT *
FROM track
