

-- Month-wise active users count
with ranked as (
select extract(month from event_timestamp) as month, count(distinct user_id) as active_users
from {{ref('silver_watch_events')}}
group by 1 )
select * from ranked 