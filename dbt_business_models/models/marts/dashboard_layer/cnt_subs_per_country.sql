-- Count of subscriptions per country and the total revenue generated from subscriptions in each country

{{config(
    materialized='table',
    schema='gold'
)}}

with subs_counts_per_country as (
    select country,subscription_plan,count(*) as subscription_count,
    case when subscription_plan ilike '%premium%'then 499
    else 199 end as plan_price,(subscription_count * plan_price) as total_revenue
    from {{ ref('silver_users') }} group by 1,2

)
select * from subs_counts_per_country