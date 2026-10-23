-- Each user watch time, total watch time, total views, favorite device and country of each user

with cte as (
    select * , row_number() over(partition by user_id order by watch_minutes desc ) as rn
    from {{ ref('silver_watch_events') }}
),
c1 as (select user_id, watch_minutes, device_type from cte where rn = 1), 
c2 as (
select c1.user_id,c1.watch_minutes,c1.device_type,c2.country from c1 
left join {{ ref('silver_users') }} as c2 on c1.user_id = c2.user_id ) ,

c3 as (
select u.user_id,u.user_name,sum(w.watch_minutes)as total_watch_time_mins,count(event_id) as total_views
,c2.device_type as fav_device,c2.country as from_country
from {{ ref('silver_users') }} u
left join {{ ref('silver_watch_events') }} w on u.user_id = w.user_id
left join c2 on u.user_id = c2.user_id
where w.user_id is not null
group by u.user_id, u.user_name,c2.device_type,c2.country 
order by total_watch_time_mins desc
)

select * ,{{watch_time_hrs('total_watch_time_mins')}} as total_watch_time_hrs from c3

