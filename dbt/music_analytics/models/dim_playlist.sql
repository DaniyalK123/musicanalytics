WITH playlist AS (
  SELECT DISTINCT
    playlist_id,
    playlist_name,
    playlist_description
  FROM stg_raw_data
)

SELECT *
FROM playlist
