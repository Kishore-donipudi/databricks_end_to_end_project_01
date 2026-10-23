-- Top 10 users with highest watch time by each country

with cte as (select distinct user_id,sum(watch_minutes) as total_watch_time from 
{{ref('silver_watch_events')}} group by user_id),

cte2 as (
select u.country,u.user_id,w.total_watch_time,row_number() over(partition by country order by total_watch_time desc) as rn from {{ref('silver_users')}} u
left join cte w on u.user_id=w.user_id)

select country,user_id,
{{watch_time_hrs('total_watch_time')}} as total_watch_time_hrs
from cte2
where rn <= 10

