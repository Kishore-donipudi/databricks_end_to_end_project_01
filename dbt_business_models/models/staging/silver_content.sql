{{ config(materialized='incremental', unique_key='content_id' ) }}

select content_id,title,genre,language,release_year,updated_at 
from  {{ source('bronze','bronze_content') }}
where content_id is not null
and title is not null and genre is not null and language is not null and release_year is not null and updated_at is not null

{% if is_incremental() %}
  and updated_at > (select max(updated_at) from {{this}})
{% endif %}
