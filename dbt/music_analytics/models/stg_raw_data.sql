{{ config(materialized='incremental', unique_key='id') }}

SELECT *
FROM {{ source('raw', 'music_data') }}
