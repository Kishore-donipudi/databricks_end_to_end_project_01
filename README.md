# Fake Netflix Data Platform

This repository contains the dbt transformation project for a Netflix-style
analytics platform. The platform follows a medallion architecture: raw data is
generated upstream, refined through Bronze and Silver layers, and served from
Gold and AI-ready models.

## Architecture

```text
Fake Netflix Data Generator
             |
             v
Databricks Workflow / Job
(every 10-15 minutes or every hour)
             |
             v
S3 / ADLS Storage
             |
             v
DLT / Auto Loader Streaming
             |
             v
================================
             BRONZE
================================
bronze_users
bronze_content
bronze_watch_events
bronze_ratings
bronze_subscriptions

Raw ingestion | Append-only | updated_at present | Minimal transformations
             |
             v
================================
             SILVER
================================
silver_users
silver_content
silver_watch_events
silver_ratings
silver_subscriptions

dbt transformations:
cleaning | null handling | deduplication | incremental loads
business rules | standardized data types
             |
             v
================================
              GOLD
================================
Dashboard models
AI models
```

The data generator, Databricks workflow, storage, and streaming ingestion
represent the upstream platform context. This repository focuses on the dbt
layer: it declares the Bronze tables as sources, builds incremental Silver
models, and publishes dashboard and AI marts.

## lakeflow Jobs 
Contains both notebook code with lakeflow declarative pipeline
<img width="1892" height="802" alt="Screenshot 2026-10-23 163816" src="https://github.com/user-attachments/assets/0044f5e5-9348-464f-bb39-667144b806ca" />

## Bronze layer
Here is the spark LakeFlow declarative pipeline
<img width="1005" height="592" alt="image" src="https://github.com/user-attachments/assets/c67733fe-10c5-4f88-be85-f0f6da595c60" />

Bronze tables are declared in
[`models/staging/source.yml`](dbt_business_models/models/staging/source.yml)
under the `bronze` source:

- `bronze_users`
- `bronze_content`
- `bronze_watch_events`
- `bronze_ratings`
- `bronze_subscriptions`

Bronze data is expected to be raw, append-only, and to include `updated_at`.
The dbt project does not recreate or reshape these ingestion tables; it
consumes them as the source of truth for Silver transformations.

## Silver layer

The Silver models are in
[`models/staging`](dbt_business_models/models/staging). Each model reads from
its corresponding Bronze source and is configured as an incremental model with
a business key:

| Silver model | Business key | Main responsibility |
| --- | --- | --- |
| `silver_users` | `user_id` | Clean user and subscription-plan attributes |
| `silver_content` | `content_id` | Clean content metadata and release information |
| `silver_watch_events` | `event_id` | Clean viewing activity and device data |
| `silver_ratings` | `rating_id` | Clean user ratings and timestamps |
| `silver_subscriptions` | `subscription_id` | Clean subscription plans, fees, and dates |

The models filter invalid required values and, on incremental runs, process
records newer than the maximum `updated_at` already present in the target.

## Gold and AI layers

The dbt configuration materializes the marts as tables:

- Dashboard models use the `gold` schema and are located in
  [`models/marts/dashboard_layer`](dbt_business_models/models/marts/dashboard_layer).
  They provide active-user, subscription, content, performance, watch-time,
  top-user, and user-management views for reporting and BI consumption.
- AI models use the `ai_schema` schema and are located in
  [`models/marts/ai_layer`](dbt_business_models/models/marts/ai_layer).
  They currently support churn analysis and content recommendations using
  Silver user, watch-event, rating, content, and subscription data.

All downstream marts use dbt `ref()` dependencies on the Silver models, so
Silver data is the contract between ingestion and business-facing outputs.

## Project structure

```text
dbt_business_models/
|-- models/
|   |-- staging/
|   |   |-- source.yml
|   |   |-- silver_*.sql
|   |-- marts/
|       |-- dashboard_layer/
|       |-- ai_layer/
|-- macros/
|-- snapshots/
|-- dbt_project.yml
```

The `users_track` snapshot preserves historical user changes in the Silver
schema using `user_id` and `updated_at`.

### Dbt Data model
<img width="799" height="576" alt="dbt_dag_crop" src="https://github.com/user-attachments/assets/f20f361a-41b8-4525-b144-f63ff3bc6b7c" />

The generated Gold and AI tables are intended for dashboards, analytics, and
downstream machine-learning workflows.
