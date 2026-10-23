# dbt-databricks-files

End-to-end data pipeline for a streaming platform using synthetic data generation, Auto Loader ingestion, and a Lakeflow Spark Declarative Pipeline bronze layer — orchestrated by a scheduled Lakeflow Job.

---

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│                    Lakeflow Job: data_gen                    │
│                   (runs every 5 hours)                       │
│                                                              │
│  ┌────────────────┐     ┌─────────────────────────────────┐  │
│  │  Task 1:       │     │  Task 2: dbt-bronze             │  │
│  │  data_gen      │────▶│  (depends on data_gen)          │ │
│  │  (notebook)    │     │  Pipeline: dbt-pl               │  │
│  │                │     │  (full_refresh = true)          │  │
│  │  Generates     │     │                                 │  │
│  │  synthetic CSV │     │  Ingests CSV → bronze streaming │  │
│  │  data → S3     │     │  tables in UC                   │  │
│  └────────────────┘     └─────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
        │                              │
        ▼                              ▼
  s3://de-prj/              dbt_bmodel_project.bronze
  (CSV files)               (streaming tables)
```

---

## Components

### 1. Data Generation — `data_gen` notebook

**Location:** `/Users/kishoredonipudi921@gmail.com/dbt-databricks-files/data_gen`

Uses the `Faker` library to generate synthetic streaming-platform data and writes CSV files to `s3://de-prj/`. Each run continues the ID sequence from the previous run, producing 2 files of 100 records per entity.

**Datasets generated:**

| Dataset | S3 Path | Key Columns |
| --- | --- | --- |
| users | `s3://de-prj/users/` | user_id, user_name, country, subscription_plan |
| content | `s3://de-prj/content/` | content_id, title, genre, language, release_year |
| watch_events | `s3://de-prj/watch_events/` | event_id, user_id, content_id, watch_minutes, device_type, event_timestamp |
| ratings | `s3://de-prj/ratings/` | rating_id, user_id, content_id, rating, rating_timestamp |
| subscriptions | `s3://de-prj/subscriptions/` | subscription_id, user_id, plan, monthly_fee, start_date |

**Key functions:**

* `get_count(folder, id_col)` — reads all CSVs in an S3 folder and returns the max numeric ID + 1, enabling incremental generation.
* `fake_data(folder, data)` — generates 2 new CSV files (100 records each), continuing the ID sequence from existing files, then uploads them to S3.

---

### 2. Bronze Layer Pipeline — `dbt-pl`

**Type:** Serverless + Photon (Lakeflow Spark Declarative Pipeline)
**Storage:** Catalog `dbt_bmodel_project`, Schema `bronze`
**Source SQL:** `bronze_layer.sql`

Creates 5 streaming tables in `dbt_bmodel_project.bronze` that continuously ingest CSV files from S3 using `stream read_files()`:

| Streaming Table | Source Path |
| --- | --- |
| `bronze_users` | `s3://de-prj/users` |
| `bronze_content` | `s3://de-prj/content` |
| `bronze_watch_events` | `s3://de-prj/watch_events` |
| `bronze_ratings` | `s3://de-prj/ratings` |
| `bronze_subscriptions` | `s3://de-prj/subscriptions` |

Each table adds an `updated_at` column with `current_timestamp()`.

---

### 3. Dynamic Bronze Layer (Alternative) — `dynamic_code.py`

An alternative approach to the bronze layer that dynamically discovers all folders in `s3://de-prj/` and creates a streaming table for each one using Auto Loader (`cloudFiles`):

* Lists all folders in `s3://de-prj/`
* For each folder, creates a streaming table named `dbt_bmodel_project.bronze.br_{folder_name}`
* Uses `cloudFiles` format with CSV, header, schema inference, and merge schema
* Checkpoint locations stored in `/Volumes/workspace/default/my_files/`

---

### 4. Orchestration — Lakeflow Job `data_gen`


| Task | Type | Depends On | Description |
| --- | --- | --- | --- |
| `data_gen` | Notebook | — | Runs the `data_gen` notebook to generate synthetic CSV data into S3 |
| `dbt-bronze` | Pipeline (full refresh) | `data_gen` | Runs the `dbt-pl` pipeline to ingest S3 CSVs into bronze streaming tables |

---

## File Structure

```
dbt-databricks-files/
├── README.md              ← this file
├── data_gen               ← notebook: synthetic data generation
└── dbt-pl/
    ├── bronze_layer.sql   ← original pipeline source file
    └── dynamic_code.py    ← original dynamic approach
```

---

## How to Reproduce

1. **Generate data** — Run the `data_gen` notebook (or trigger the job) to create CSV files in `s3://de-prj/`.
2. **Ingest to bronze** — Run the `dbt-pl` pipeline to create streaming tables in `dbt_bmodel_project.bronze`.
3. **Query bronze tables** — Query any table, e.g.:
   ```sql
   SELECT * FROM dbt_bmodel_project.bronze.bronze_users LIMIT 10;
   ```

---

## Notes

* The `data_gen` job runs every 5 hours on a periodic schedule and all recent runs have completed successfully.
* The `dbt-bronze` task runs with `full_refresh = true`, so the pipeline is fully re-created on each run.
* The `dynamic_code.py` file is an alternative to `bronze_layer.sql` — it auto-discovers folders rather than hardcoding each table.