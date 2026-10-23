create or refresh streaming table dbt_bmodel_project.bronze.bronze_users
as 
select *,current_timestamp() as updated_at from 
stream read_files('s3://de-prj/users' ,format => 'csv',header =>true,inferSchema =>true) ;

create or refresh streaming table dbt_bmodel_project.bronze.bronze_content
as 
select *,current_timestamp() as updated_at from 
stream read_files('s3://de-prj/content' ,format => 'csv',header =>true,inferSchema =>true) ;

create or refresh streaming table dbt_bmodel_project.bronze.bronze_watch_events
as 
select *,current_timestamp() as updated_at from 
stream read_files('s3://de-prj/watch_events' ,format => 'csv',header =>true,inferSchema =>true) ;

create or refresh streaming table dbt_bmodel_project.bronze.bronze_ratings
as 
select *,current_timestamp() as updated_at from 
stream read_files('s3://de-prj/ratings' ,format => 'csv',header =>true,inferSchema =>true) ;

create or refresh streaming table dbt_bmodel_project.bronze.bronze_subscriptions
as 
select *,current_timestamp() as updated_at from 
stream read_files('s3://de-prj/subscriptions' ,format => 'csv',header =>true,inferSchema =>true) ;


