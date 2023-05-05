SELECT
  track_id,
  chart_date,
  chart_rank
FROM
  {{ ref('stg_billboard_hot100') }}
