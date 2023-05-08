-- models/fact_artist_chart_ranking.sql

{{ config(unique_key='date || "_" || artist_id') }}

SELECT
    d.date,
    a.artist_id,
    chart_rank
FROM {{ source('raw', 'music_data') }} AS m
JOIN {{ ref('dim_artist') }} AS a ON m.artist_spotify_id = a.artist_spotify_id
JOIN {{ ref('dim_date') }} AS d ON m.date = d.date
WHERE
    m.artist_chart_rank IS NOT NULL
