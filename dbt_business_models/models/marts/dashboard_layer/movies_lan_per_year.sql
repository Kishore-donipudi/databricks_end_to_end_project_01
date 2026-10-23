-- Movies released per languagein each year

{{config(
    materialized='table',
    schema='gold'
)}}

with language_per_year as (
    select release_year,language,count(*) as total_movies
    from {{ ref('silver_content') }} 
    group by all
)
select * from language_per_year