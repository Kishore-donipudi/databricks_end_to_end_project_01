-- watch time and average rating of each content

with cte as ( select ra.user_id, ra.rating from {{ref('silver_ratings')}} ra left join {{ref('silver_users')}}
 u on ra.user_id=u.user_id)
select
    c.title,
    c.genre,
    count(distinct w.user_id) as users_watched,
    {{watch_time_hrs('sum(w.watch_minutes)')}} as watch_time,
    round(avg(r.rating),2) as  avg_rating
from {{ref('silver_content')}} c
left join {{ref('silver_watch_events')}} w
    on c.content_id=w.content_id
inner join cte r
    on w.user_id=r.user_id
group by 1,2
order by sum(w.watch_minutes) desc , avg_rating desc