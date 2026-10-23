{% snapshot users_track %}

{{config
    (target_schema='silver',
    unique_key='user_id',
    strategy='timestamp',
    updated_at='updated_at')
}}
select * from dbt_bmodel_project.bronze.bronze_users

{%endsnapshot%}