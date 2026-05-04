# CLAUDE.md — Project Context for Claude Code

## Project Overview

This is a fintech data analytics pipeline exploring the relationship between
weather conditions in key financial hubs (New York, London, San Francisco) and
market sentiment/trading behavior.

## Query Conventions

When querying the knowledge base, Claude Code should:

1. **Start with wiki pages** (`knowledge/wiki/`) for synthesized summaries
2. **Fall back to raw sources** (`knowledge/raw/`) for primary evidence
3. **Reference the index** (`knowledge/index.md`) to find the right file

## Example Queries

- "What does behavioral finance research say about weather and market returns?"
- "How does cloud cover correlate with NYSE trading volume?"
- "What are the key fintech trends in London vs San Francisco?"
- "What did Investopedia say about weather effects on investor psychology?"
- "Summarize the relationship between humidity and financial decision-making"

## Data Pipeline Context

- **Raw layer:** `WEATHER_RAW` table in Snowflake (WeatherAPI data)
- **Staging:** `stg_weather` (cleaned + enriched)
- **Mart:** `fact_weather_readings`, `dim_location`, `dim_date`, `dim_condition`
- **Dashboard:** Streamlit app at `streamlit_app/app.py`
- **Knowledge base:** 15+ Investopedia/financial sources in `knowledge/raw/`

## Key Concepts in This Project

- **Weather comfort score:** Composite metric (0–1) derived from temperature,
  humidity, and wind; used as a proxy for investor sentiment
- **Market sentiment bias:** Categorical label (Positive/Neutral/Negative)
  assigned to each weather condition based on behavioral finance research
- **Trading activity score:** Integer 1–5 rating of expected trading volume
  given weather conditions

## dbt Models

Run `dbt run` from `dbt_project/` to rebuild all models.
Run `dbt test` to validate data quality.
Profiles are configured via environment variables (see `.env.example`).
