# Snowflake Portfolio

A collection of five hands-on Snowflake projects built to demonstrate core platform capabilities end-to-end — from real-time ingestion to ML, cost engineering, dbt modeling, and governance. Each project lives in its own folder with a full write-up, code, and (where applicable) a live Streamlit dashboard.

Built on a Snowflake trial account to show what's achievable without enterprise infrastructure — just deliberate architecture choices and an understanding of how the platform actually works under the hood.

---

## Projects

| # | Project | What it demonstrates |
|---|---------|----------------------|
| 1 | [Real-Time Streaming Pipeline](./P1%20snowflake-streaming-pipeline) | Snowpipe auto-ingest, Streams (CDC), Tasks, AWS S3 integration |
| 2 | [Snowpark ML Pipeline](./P2%20snowflake-snowpark-ml-pipeline) | In-warehouse feature engineering, model training, Snowflake Model Registry |
| 3 | [Cost & Performance Optimization](./P3%20snowflake-cost-performance-optimization) | Query profiling, warehouse right-sizing, materialized views, search optimization |
| 4 | [Multi-Source dbt Pipeline](./P4%20snowflake-dbt-multisource-pipeline) | dbt staging/intermediate/marts modeling, multi-source ingestion, testing, lineage |
| 5 | [Data Sharing & Governance](./P5%20snowflake-data-sharing-governance) | Row access policies, dynamic & tag-based masking, Secure Data Sharing |

---

## 1. Real-Time Streaming Pipeline (Snowpipe + Streams + Tasks)

An end-to-end CDC-style pipeline: a Python producer simulates a live event stream pushed to AWS S3, Snowpipe auto-ingests via SQS event notifications, a Stream captures changes, and a scheduled Task transforms them into a curated table — with a Streamlit dashboard showing live-updating metrics.

**Stack:** AWS S3 · Snowpipe · Streams & Tasks · Python (boto3, Faker) · Streamlit in Snowflake

**Highlights:** Secure storage integration (no hardcoded AWS credentials), real IAM trust policy troubleshooting, ~1-2 minute end-to-end latency documented honestly against true streaming systems like Kafka.



---

## 2. Snowpark ML Pipeline

A churn prediction model trained on the Telco Customer Churn dataset, with feature engineering and evaluation kept close to Snowflake's compute, registered as a versioned model in the Snowflake Model Registry, and served both via SQL and a live Streamlit dashboard.

**Stack:** Snowpark · scikit-learn · XGBoost · Snowflake Model Registry · Streamlit in Snowflake

**Highlights:** Real-world adaptation from the deprecated `snowflake.ml.modeling` estimators to the native sklearn/XGBoost + Model Registry pattern Snowflake's own docs now recommend — documented as an actual engineering decision, not glossed over.

**Result:** Accuracy 0.768, F1 0.532 on held-out test data.



---

## 3. Cost & Performance Optimization Case Study

A deliberately inefficient query against Snowflake's built-in TPC-H sample dataset (SF10, ~60M rows), systematically optimized through join-key fixes, filter pushdown, warehouse right-sizing, materialized views, and Search Optimization Service — with before/after metrics captured at every step.

**Stack:** TPC-H sample data · Query Profile · warehouse sizing · materialized views · Search Optimization Service

**Highlights:** A concrete, measured before/after table (elapsed time, bytes scanned, credits consumed) plus a documented finding that warehouse size past a certain point stopped improving performance — the kind of judgment call that separates tuning from guessing.



---

## 4. Multi-Source dbt Pipeline

Three genuinely different source types — a flat file, a live REST API, and a PostgreSQL database — landed in Snowflake and modeled through a proper dbt layered architecture (staging → intermediate → marts), with schema tests and auto-generated lineage documentation.

**Stack:** dbt-core · dbt-snowflake · PostgreSQL (Docker) · REST API ingestion · Streamlit in Snowflake

**Highlights:** A final mart that genuinely combines all three sources into one customer-level view (orders, USD-normalized revenue, support ticket burden) — not three disconnected pipelines that happen to share a repo.



---

## 5. Data Sharing & Governance Demo

A synthetic multi-tenant healthcare-style dataset locked down with Row Access Policies (department-level row restriction) and Dynamic Data Masking (including tag-based masking for scalable governance), then shared cross-account via Snowflake Secure Data Sharing.

**Stack:** Row Access Policies · Dynamic Data Masking · Tag-based masking · Secure Data Sharing

**Highlights:** A governed view (not the raw table) shared to a second Snowflake account with zero data copying and zero consumer-side storage cost — demonstrating least-privilege sharing design, not just that sharing is technically possible.



---


## About

Built by Shijith Pulikkal as a hands-on Snowflake portfolio — every project was built, broken, debugged, and fixed on a live trial account rather than copied from documentation. Each project folder includes the real troubleshooting encountered along the way, because that's a more honest signal of understanding than a pipeline that "just worked."


