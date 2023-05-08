-- models/fact_track_chart_ranking.sql

{{ config(unique_key='date || "_" || track_id') }}

SELECT
    d.date,
    t.track_id,
    chart_rank
FROM {{ source('raw', 'music_data') }} AS m
JOIN {{ ref('dim_track') }} AS t ON m.track_spotify_id = t.track_spotify_id
JOIN {{ ref('dim_date') }} AS d ON m.date = d.date
WHERE
    m.track_chart_rank IS NOT NULL
