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

## Knowledge Base Schema

Three operations govern the `knowledge/` directory:

### Ingest — when new files land in `knowledge/raw/`

1. Read the new file and identify which wiki pages it's relevant to (`overview`, `key-players`, `market-trends`, `marketing-analytics`).
2. Add sourced claims to the relevant wiki page(s) using `> Source: filename.md` citations.
3. Add the file to the Raw Sources table in `knowledge/index.md`.
4. If the file fills a gap listed in `market-trends.md` → Gaps section, remove that bullet.

### Query — when answering questions about fintech, Greenlight, or the role

1. Read `knowledge/index.md` to locate the right wiki page.
2. Read the wiki page — answer from there when possible.
3. If the wiki lacks detail, fall back to the raw source(s) cited on that page.
4. Always name the wiki page or raw file the answer draws from.
5. If the knowledge base doesn't cover it, say so explicitly — do not fill gaps by hallucinating.

### Lint — periodic consistency checks

1. Every `> Source: filename.md` citation in a wiki page must point to a real file in `knowledge/raw/`. Flag broken citations.
2. Every file in `knowledge/raw/` must appear in the Raw Sources table in `knowledge/index.md`. Flag unlisted files.
3. Every wiki page in `knowledge/wiki/` must be linked from `knowledge/index.md`. Flag missing links.
4. Every claim in a wiki page must carry either a `> Source:` or `> Background:` label — no unlabeled assertions.
