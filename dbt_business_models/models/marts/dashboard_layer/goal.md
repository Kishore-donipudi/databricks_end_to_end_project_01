

# Dashboard layer

## Goal

Create Gold-schema, dashboard-ready tables for reporting and visualization.
These dbt marts provide consistent, business-friendly outputs for BI tools
without requiring dashboards to query the Silver transformation tables
directly.

## Current dashboard outputs

The models in this folder answer questions such as:

- How many movies are released by language and year?
- Which countries and subscription plans have the most subscriptions?
- Which users have the highest watch time?
- Which month has the most active users?
- What are the content, watch-time, and user-management performance metrics?

## Models

- `active_users_per_month.sql` - ranks months by distinct active users.
- `cnt_subs_per_country.sql` - counts subscriptions and summarizes revenue by
  country and subscription plan.
- `movies_lan_per_year.sql` - counts movies by language and release year.
- `performance.sql` - combines content, ratings, and watch activity for
  performance reporting.
- `top_users.sql` - ranks users by watch time within each country.
- `user_management.sql` - produces user-level watch-time, view, country, and
  device information.
- `all_tables.sql` - provides a combined ephemeral model for development or
  ad hoc use.

All dashboard models depend on the Silver models through dbt `ref()` calls and
are configured as tables in the `gold` schema by
[`dbt_project.yml`](../../../dbt_project.yml).