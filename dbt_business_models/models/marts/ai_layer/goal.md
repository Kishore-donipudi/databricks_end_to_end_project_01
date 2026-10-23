# AI layer

## Goal

Provide AI-ready tables in the `ai_schema` schema for user-retention
analysis and personalized content recommendations. The models prepare
features and aggregates from the Silver users, subscriptions, watch events,
ratings, and content models so that downstream analytics or machine-learning
jobs can consume consistent inputs.

## Current outputs

- `churn_predict_users.sql` - combines user activity, ratings, and
  subscription history to support churn analysis and retention decisions.
- `recommendation_engine.sql` - summarizes each user's watched content,
  watch time, and ratings to support content recommendations.

These are dbt table models and are materialized in `ai_schema` by
[`dbt_project.yml`](../../../dbt_project.yml). The models provide analytical
inputs; a separate machine-learning or serving workflow can use them to
produce predictions and recommendations.
