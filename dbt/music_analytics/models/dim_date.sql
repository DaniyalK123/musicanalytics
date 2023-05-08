-- models/dim_date.sql

WITH date_range AS (
    SELECT
        GENERATE_DATE_ARRAY(
            DATE_TRUNC(DATE_SUB(CURRENT_DATE(), INTERVAL 3 MONTH), WEEK),
            CURRENT_DATE(),
            INTERVAL 1 DAY
        ) AS date
)

SELECT
    date,
    EXTRACT(DAY FROM date) AS day,
    EXTRACT(MONTH FROM date) AS month,
    EXTRACT(YEAR FROM date) AS year,
    EXTRACT(DAYOFWEEK FROM date) AS day_of_week
FROM
    date_range,
    UNNEST(date_range.date) AS date
