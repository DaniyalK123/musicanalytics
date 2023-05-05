  WITH artist AS (
  SELECT DISTINCT
    artist_id,
    artist_name,
    artist_listeners,
    artist_play_count,
    artist_musicbrainz
  FROM stg_raw_data
)

SELECT *
FROM artist

