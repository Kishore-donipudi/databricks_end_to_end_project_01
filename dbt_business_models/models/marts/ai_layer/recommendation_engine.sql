-- Recommendation Engine

select u.user_id,w.content_id,count(*) as watch_count,sum(w.watch_minutes) as watch_minutes,
max(r.rating) as rating,any_value(c.genre) as genre,any_value(c.release_year) as release_year,any_value(c.language) as language,
any_value(u.subscription_plan) as sub_plan,
case when u.subscription_plan = 'premium' then 1 else 0 end as is_premium_user
,any_value(u.country) as country
from {{ref('silver_users')}} u inner join
{{ ref('silver_watch_events') }} w inner join {{ ref('silver_ratings') }} r on w.user_id = r.user_id  
left join {{ref('silver_content')}} c on w.content_id = c.content_id
group by u.user_id, w.content_id,u.subscription_plan