WITH src AS (
  SELECT
    _table_suffix AS date,
    * EXCEPT (_table_suffix)
  FROM
    `your_project_id.your_dataset_name.raw_data_*`
)

SELECT
  track_id,
  track_name,
  artist_id,
  artist_name,
  album_id,
  album_name,
  popularity,
  artist_listeners,
  artist_play_count,
  artist_musicbrainz,
  chart_date,
  chart_rank
FROM
  src
