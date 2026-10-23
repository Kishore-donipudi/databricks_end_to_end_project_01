
{{config(materialized='view',schema='silver')}}

with c1 as (
    select count(*) as total_users from {{ref('silver_users')}}
) , c2 as (
    select count(*) as total_subscriptions from {{ref('silver_subscriptions')}}
) , c3 as (
    select count(*) as total_content from {{ref('silver_content')}}
) , c4 as (
    select count(*) as total_ratings from {{ref('silver_ratings')}}
) , c5 as (
    select count(*) as total_watch_events from {{ref('silver_watch_events')}}
)
select * from c1,c2,c3,c4,c5 