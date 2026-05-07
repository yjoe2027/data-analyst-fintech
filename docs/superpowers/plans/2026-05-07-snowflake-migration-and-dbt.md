# Snowflake Migration & dbt Pipeline Fix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate WEATHER_RAW from BASKET_CRAFT to a dedicated FINTECH_WEATHER database, build out the missing dbt project files, and get the Streamlit dashboard running locally against live Snowflake data.

**Architecture:** Create FINTECH_WEATHER database with RAW / STAGING / MART schemas. dbt staging views land in STAGING; mart tables (dim_* + fact_weather_readings) land in MART. Streamlit connects to FINTECH_WEATHER.MART. A custom `generate_schema_name` macro ensures schema names are clean (no `dbt_` prefix noise).

**Tech Stack:** Python snowflake-connector-python, dbt-core + dbt-snowflake + dbt-utils, Streamlit, python-dotenv

---

## File Map

### Create
- `dbt_project/dbt_project.yml` — dbt project config (profile, model materialization)
- `dbt_project/profiles.yml` — Snowflake connection (reads env vars)
- `dbt_project/packages.yml` — declares dbt-utils dependency
- `dbt_project/macros/generate_schema_name.sql` — clean schema name macro
- `dbt_project/models/staging/sources.yml` — declares FINTECH_WEATHER.RAW.WEATHER_RAW source
- `dbt_project/models/staging/stg_weather.yml` — column tests for stg_weather
- `dbt_project/models/mart/dim_location.sql` — location dimension
- `dbt_project/models/mart/dim_date.sql` — date dimension
- `dbt_project/models/mart/dim_condition.sql` — weather condition dimension with sentiment
- `dbt_project/models/mart/mart_models.yml` — tests + docs for mart models

### Modify
- `.env` — SNOWFLAKE_DATABASE, SNOWFLAKE_WAREHOUSE, SNOWFLAKE_ROLE
- `.env.example` — same keys with placeholder values

---

### Task 1: Provision FINTECH_WEATHER database and migrate data

**Files:** none (Snowflake only)

- [ ] **Step 1: Create database, schemas, table, and copy data**

```python
# Run via: .venv/bin/python3 scripts/migrate_snowflake.py
import snowflake.connector

conn = snowflake.connector.connect(
    account="gjhezxb-lpb73600",
    user="yjoe",
    password="Korea8642vps#$",
    warehouse="COMPUTE_WH",
    role="SYSADMIN",
)
cur = conn.cursor()

stmts = [
    "CREATE DATABASE IF NOT EXISTS FINTECH_WEATHER",
    "CREATE SCHEMA IF NOT EXISTS FINTECH_WEATHER.RAW",
    "CREATE SCHEMA IF NOT EXISTS FINTECH_WEATHER.STAGING",
    "CREATE SCHEMA IF NOT EXISTS FINTECH_WEATHER.MART",
    """CREATE TABLE IF NOT EXISTS FINTECH_WEATHER.RAW.WEATHER_RAW (
        id INTEGER AUTOINCREMENT PRIMARY KEY,
        location_name VARCHAR(100),
        region VARCHAR(100),
        country VARCHAR(100),
        lat FLOAT,
        lon FLOAT,
        temp_c FLOAT,
        temp_f FLOAT,
        condition_text VARCHAR(200),
        wind_mph FLOAT,
        wind_kph FLOAT,
        humidity INTEGER,
        feelslike_c FLOAT,
        feelslike_f FLOAT,
        uv FLOAT,
        local_time VARCHAR(50),
        extracted_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
    )""",
    """INSERT INTO FINTECH_WEATHER.RAW.WEATHER_RAW
       (location_name, region, country, lat, lon,
        temp_c, temp_f, condition_text, wind_mph, wind_kph,
        humidity, feelslike_c, feelslike_f, uv, local_time, extracted_at)
       SELECT location_name, region, country, lat, lon,
              temp_c, temp_f, condition_text, wind_mph, wind_kph,
              humidity, feelslike_c, feelslike_f, uv, local_time, extracted_at
       FROM BASKET_CRAFT.RAW.WEATHER_RAW""",
]
for stmt in stmts:
    cur.execute(stmt)
    print("OK:", stmt[:60])

cur.execute("SELECT COUNT(*) FROM FINTECH_WEATHER.RAW.WEATHER_RAW")
print("Rows migrated:", cur.fetchone()[0])
cur.close()
conn.close()
```

- [ ] **Step 2: Verify row count matches**

```bash
# Expected: same count as BASKET_CRAFT.RAW.WEATHER_RAW
```

- [ ] **Step 3: Commit**

```bash
git add -A && git commit -m "chore: create FINTECH_WEATHER db and migrate WEATHER_RAW"
```

---

### Task 2: Update .env and .env.example

**Files:** `.env`, `.env.example`

- [ ] **Step 1: Update .env**

```
SNOWFLAKE_DATABASE=FINTECH_WEATHER
SNOWFLAKE_SCHEMA=RAW
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_ROLE=SYSADMIN
SNOWFLAKE_MART_SCHEMA=MART
```

- [ ] **Step 2: Update .env.example**

```
SNOWFLAKE_DATABASE=FINTECH_WEATHER
SNOWFLAKE_SCHEMA=RAW
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_ROLE=SYSADMIN
SNOWFLAKE_MART_SCHEMA=MART
```

- [ ] **Step 3: Commit**

```bash
git add .env.example && git commit -m "chore: update .env.example for FINTECH_WEATHER db"
```
(`.env` is gitignored — do not commit it)

---

### Task 3: Create dbt project scaffolding

**Files:** `dbt_project/dbt_project.yml`, `dbt_project/profiles.yml`, `dbt_project/packages.yml`, `dbt_project/macros/generate_schema_name.sql`

- [ ] **Step 1: Create dbt_project.yml**

```yaml
name: 'fintech_weather'
version: '1.0.0'
config-version: 2

profile: 'fintech_weather'

model-paths: ["models"]
macro-paths: ["macros"]

models:
  fintech_weather:
    staging:
      +materialized: view
      +schema: STAGING
    mart:
      +materialized: table
      +schema: MART
```

- [ ] **Step 2: Create profiles.yml**

```yaml
fintech_weather:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: "{{ env_var('SNOWFLAKE_ACCOUNT') }}"
      user: "{{ env_var('SNOWFLAKE_USER') }}"
      password: "{{ env_var('SNOWFLAKE_PASSWORD') }}"
      role: "{{ env_var('SNOWFLAKE_ROLE') }}"
      database: "{{ env_var('SNOWFLAKE_DATABASE') }}"
      warehouse: "{{ env_var('SNOWFLAKE_WAREHOUSE') }}"
      schema: MART
      threads: 4
      client_session_keep_alive: False
```

- [ ] **Step 3: Create packages.yml**

```yaml
packages:
  - package: dbt-labs/dbt_utils
    version: [">=1.0.0", "<2.0.0"]
```

- [ ] **Step 4: Create macros/generate_schema_name.sql**

```sql
{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- if custom_schema_name is none -%}
        {{ target.schema }}
    {%- else -%}
        {{ custom_schema_name | trim | upper }}
    {%- endif -%}
{%- endmacro %}
```

- [ ] **Step 5: Commit**

```bash
git add dbt_project/dbt_project.yml dbt_project/profiles.yml dbt_project/packages.yml dbt_project/macros/
git commit -m "feat: add dbt project config, profiles, packages, schema macro"
```

---

### Task 4: Create dbt sources and staging tests

**Files:** `dbt_project/models/staging/sources.yml`, `dbt_project/models/staging/stg_weather.yml`

- [ ] **Step 1: Create sources.yml**

```yaml
version: 2

sources:
  - name: raw
    database: "{{ env_var('SNOWFLAKE_DATABASE') }}"
    schema: RAW
    tables:
      - name: weather_raw
        description: Raw weather readings from WeatherAPI
        columns:
          - name: id
            tests: [unique, not_null]
          - name: location_name
            tests: [not_null]
          - name: temp_c
            tests: [not_null]
          - name: extracted_at
            tests: [not_null]
```

- [ ] **Step 2: Create stg_weather.yml**

```yaml
version: 2

models:
  - name: stg_weather
    description: Cleaned and enriched weather readings from WeatherAPI
    columns:
      - name: weather_id
        tests: [unique, not_null]
      - name: location_name
        tests: [not_null]
      - name: temp_c
        tests: [not_null]
      - name: condition_category
        tests:
          - not_null
          - accepted_values:
              values: ['Clear', 'Cloudy', 'Rainy', 'Snowy', 'Foggy', 'Stormy', 'Other']
```

- [ ] **Step 3: Commit**

```bash
git add dbt_project/models/staging/
git commit -m "feat: add dbt source definition and staging model tests"
```

---

### Task 5: Create dimension models

**Files:** `dbt_project/models/mart/dim_location.sql`, `dbt_project/models/mart/dim_date.sql`, `dbt_project/models/mart/dim_condition.sql`

- [ ] **Step 1: Create dim_location.sql**

```sql
-- mart/dim_location.sql
-- One row per distinct city tracked by the pipeline

with locations as (
    select distinct
        location_name,
        region,
        country,
        lat,
        lon
    from {{ ref('stg_weather') }}
),

enriched as (
    select
        {{ dbt_utils.generate_surrogate_key(['location_name']) }} as location_key,
        location_name,
        region,
        country,
        lat,
        lon,
        case location_name
            when 'New York'       then 'NYSE / NASDAQ'
            when 'London'         then 'LSE'
            when 'San Francisco'  then 'NASDAQ'
            else 'Other'
        end                                                         as financial_market,
        case location_name
            when 'New York'       then 'America/New_York'
            when 'London'         then 'Europe/London'
            when 'San Francisco'  then 'America/Los_Angeles'
            else 'UTC'
        end                                                         as timezone,
        case location_name
            when 'New York'       then 'USD'
            when 'London'         then 'GBP'
            when 'San Francisco'  then 'USD'
            else 'USD'
        end                                                         as primary_currency
    from locations
)

select * from enriched
```

- [ ] **Step 2: Create dim_date.sql**

```sql
-- mart/dim_date.sql
-- One row per distinct extraction date observed in the pipeline

with dates as (
    select distinct extraction_date as date_key
    from {{ ref('stg_weather') }}
    where extraction_date is not null
),

enriched as (
    select
        date_key,
        year(date_key)                                     as year,
        month(date_key)                                    as month,
        day(date_key)                                      as day,
        dayofweek(date_key)                                as day_of_week,
        dayname(date_key)                                  as day_name,
        monthname(date_key)                                as month_name,
        quarter(date_key)                                  as quarter,
        case when dayofweek(date_key) between 1 and 5
             then true else false end                      as is_weekday,
        case when dayofweek(date_key) in (0, 6)
             then true else false end                      as is_weekend
    from dates
)

select * from enriched
```

- [ ] **Step 3: Create dim_condition.sql**

```sql
-- mart/dim_condition.sql
-- One row per weather condition category with market sentiment metadata

with conditions as (
    select distinct condition_category
    from {{ ref('stg_weather') }}
),

enriched as (
    select
        {{ dbt_utils.generate_surrogate_key(['condition_category']) }} as condition_key,
        condition_category,
        case condition_category
            when 'Clear'   then 'Sunny or clear skies'
            when 'Cloudy'  then 'Overcast or partly cloudy'
            when 'Rainy'   then 'Rain or drizzle'
            when 'Snowy'   then 'Snow or blizzard'
            when 'Foggy'   then 'Fog or mist'
            when 'Stormy'  then 'Thunderstorm or severe weather'
            else 'Mixed or unclassified conditions'
        end                                                             as example_condition_text,
        case condition_category
            when 'Clear'   then 'Positive'
            when 'Cloudy'  then 'Slightly Negative'
            when 'Rainy'   then 'Negative'
            when 'Snowy'   then 'Negative'
            when 'Foggy'   then 'Neutral'
            when 'Stormy'  then 'Very Negative'
            else 'Neutral'
        end                                                             as market_sentiment_bias,
        case condition_category
            when 'Clear'   then 5
            when 'Cloudy'  then 3
            when 'Rainy'   then 2
            when 'Snowy'   then 2
            when 'Foggy'   then 3
            when 'Stormy'  then 1
            else 3
        end                                                             as trading_activity_score
    from conditions
)

select * from enriched
```

- [ ] **Step 4: Commit**

```bash
git add dbt_project/models/mart/dim_location.sql dbt_project/models/mart/dim_date.sql dbt_project/models/mart/dim_condition.sql
git commit -m "feat: add dim_location, dim_date, dim_condition dbt models"
```

---

### Task 6: Add mart model tests

**Files:** `dbt_project/models/mart/mart_models.yml`

- [ ] **Step 1: Create mart_models.yml**

```yaml
version: 2

models:
  - name: dim_location
    description: One row per city tracked by the pipeline
    columns:
      - name: location_key
        tests: [unique, not_null]
      - name: location_name
        tests: [unique, not_null]
      - name: financial_market
        tests: [not_null]

  - name: dim_date
    description: One row per extraction date
    columns:
      - name: date_key
        tests: [unique, not_null]

  - name: dim_condition
    description: Weather condition categories with market sentiment metadata
    columns:
      - name: condition_key
        tests: [unique, not_null]
      - name: condition_category
        tests: [unique, not_null]
      - name: market_sentiment_bias
        tests:
          - not_null
          - accepted_values:
              values: ['Positive', 'Slightly Negative', 'Negative', 'Very Negative', 'Neutral']
      - name: trading_activity_score
        tests:
          - not_null
          - accepted_values:
              values: [1, 2, 3, 4, 5]

  - name: fact_weather_readings
    description: Central fact table — one row per weather reading
    columns:
      - name: reading_key
        tests: [unique, not_null]
      - name: location_key
        tests: [not_null, relationships:
                  {to: ref('dim_location'), field: location_key}]
      - name: date_key
        tests: [not_null, relationships:
                  {to: ref('dim_date'), field: date_key}]
      - name: condition_key
        tests: [not_null, relationships:
                  {to: ref('dim_condition'), field: condition_key}]
```

- [ ] **Step 2: Commit**

```bash
git add dbt_project/models/mart/mart_models.yml
git commit -m "feat: add mart model tests and documentation"
```

---

### Task 7: Install dbt and run pipeline

**Files:** none (commands only)

- [ ] **Step 1: Install dbt into venv**

```bash
.venv/bin/pip install dbt-core dbt-snowflake -q
```

- [ ] **Step 2: Install dbt packages**

```bash
cd dbt_project && ../.venv/bin/dbt deps --profiles-dir .
```

- [ ] **Step 3: Run dbt models**

```bash
cd dbt_project && ../.venv/bin/dbt run --profiles-dir .
```

Expected: 5 models pass (stg_weather, dim_location, dim_date, dim_condition, fact_weather_readings)

- [ ] **Step 4: Run dbt tests**

```bash
cd dbt_project && ../.venv/bin/dbt test --profiles-dir .
```

Expected: all tests pass

- [ ] **Step 5: Commit**

```bash
git add dbt_project/
git commit -m "feat: complete dbt pipeline — all models and tests passing"
```

---

### Task 8: Launch Streamlit dashboard

**Files:** `streamlit_app/requirements.txt` (verify deps), then run

- [ ] **Step 1: Install Streamlit dependencies**

```bash
.venv/bin/pip install streamlit plotly pandas snowflake-connector-python python-dotenv statsmodels -q
```

- [ ] **Step 2: Launch dashboard**

```bash
cd streamlit_app && ../.venv/bin/streamlit run app.py
```

Expected: dashboard opens at http://localhost:8501, loads data from FINTECH_WEATHER.MART

- [ ] **Step 3: Verify data loads** — confirm KPI metrics show real readings, charts render, no Snowflake connection error

- [ ] **Step 4: Commit**

```bash
git commit -m "chore: end-to-end pipeline working — Snowflake + dbt + Streamlit"
```
