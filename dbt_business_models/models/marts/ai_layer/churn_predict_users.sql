
-- users will continue with their current plan or upgrade/downgrade it based on their activity and usage pattern
-- watch time , how many content watched , how many content rated , consecutive sub plan , no of months user is took the subscription
-- wrong code - Bcoz subs have multiple start dates but it is not considering the other start dates due to the incremental model where i 
-- created the update_at with timestamp at the same time at all the cols  
with
watch_stats as (
    select
        user_id,
        sum(watch_minutes) as total_watch_time_mins,
        count(*) as total_content_watched,
        max(to_date(event_timestamp)) as last_watch
    from {{ ref('silver_watch_events') }}
    group by user_id

),

rating_stats as (
    select
        user_id,
        count(*) as total_content_rated
    from {{ ref('silver_ratings') }}
    group by user_id

),

subscription_stats as (
    select
        user_id,
        count(*)  as no_of_months_subscribed,
        min(extract(year from start_date)) as subscription_year
    from {{ ref('silver_subscriptions') }}
    group by user_id

)

select
    u.user_id,
    u.user_name,
    u.subscription_plan as current_plan,
    u.country as user_country,
    w.total_watch_time_mins,
    {{ watch_time_hrs('w.total_watch_time_mins') }} as total_watch_time_hrs,
    w.total_content_watched,
    coalesce(r.total_content_rated,0) as total_content_rated,
    coalesce(s.subscription_year,0) as subscription_year,
    w.last_watch as last_watch_date
from {{ ref('silver_users') }} u
left join watch_stats w
    on u.user_id = w.user_id
left join rating_stats r
    on u.user_id = r.user_id
left join subscription_stats s
    on u.user_id = s.user_id
where u.user_id is not null and u.user_name is not null and u.subscription_plan is not null and u.country is not null 
and w.total_watch_time_mins is not null and w.total_content_watched is not null and r.total_content_rated is not null
and s.no_of_months_subscribed is not null and s.subscription_year is not null