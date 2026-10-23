{{config(materialized='incremental', unique_key='subscription_id' )}}

select subscription_id,user_id,plan,monthly_fee,start_date,updated_at 
from {{source('bronze','bronze_subscriptions')}}
where subscription_id is not null 
and user_id is not null and plan is not null 
and monthly_fee is not null and start_date is not null 
and updated_at is not null

{% if is_incremental() %}
  and updated_at > (select max(updated_at) from {{this}})
{% endif %}
