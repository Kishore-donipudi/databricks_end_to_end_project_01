{{config(materialized='ephemeral',schema='gold')}}

with c1 as (
  select * from {{ ref('silver_users') }} ),
  c2 as (select * from {{ ref('silver_ratings') }} ),
  c3 as (select * from {{ ref('silver_subscriptions') }} ),
  c4 as (select * from {{ ref('silver_content') }} ),
  c5 as (select * from {{ ref('silver_watch_events') }} )
select * from c1,c2,c3,c4,c5


