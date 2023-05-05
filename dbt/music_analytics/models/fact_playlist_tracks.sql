SELECT
  playlist_id,
  track_id
FROM
  {{ ref('stg_billboard_hot100') }}
