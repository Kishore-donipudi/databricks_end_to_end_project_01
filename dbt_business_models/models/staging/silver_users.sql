{{ config(
    materialized='incremental',
    unique_key='user_id'
) }}


select user_id,user_name,country,subscription_plan,updated_at
 from  {{source('bronze','bronze_users') }}
where user_id is not null 
and user_name is not null and country is not null and subscription_plan is not null 
and updated_at is not null

{% if is_incremental() %}
  and updated_at > (select max(updated_at) from {{this}})
{% endif %}
