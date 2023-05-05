WITH src AS (
  SELECT
    _table_suffix AS date,
    * EXCEPT (_table_suffix)
  FROM
    `your_project_id.your_dataset_name.raw_data_*`
)

SELECT
  DISTINCT artist_id,
  artist_name,
  artist_listeners,
  artist_play_count,
  artist_musicbrainz
FROM
  src
