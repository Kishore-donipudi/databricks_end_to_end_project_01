{{ config(materialized='incremental', unique_key='rating_id' ) }}

select rating_id,user_id,rating,rating_timestamp,updated_at from {{ source('bronze','bronze_ratings')}}
where rating_id is not null and user_id is not null and rating is not null and rating_timestamp is not null and updated_at is not null

{% if is_incremental() %}
  and updated_at > (select max(updated_at) from {{this}})
{% endif %}