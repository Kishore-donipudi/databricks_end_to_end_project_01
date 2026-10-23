{{ config(materialized='incremental', unique_key='event_id' )}}

select event_id,user_id,content_id,watch_minutes,device_type,event_timestamp,updated_at
from {{ source('bronze','bronze_watch_events')}}
where event_id is not null and user_id is not null and 
content_id is not null and watch_minutes is not null and 
device_type is not null and event_timestamp is not null and 
updated_at is not null

{% if is_incremental() %}
  and updated_at > (select max(updated_at) from {{this}})
{% endif %}
