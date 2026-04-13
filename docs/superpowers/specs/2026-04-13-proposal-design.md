---
title: Fintech Equity Analytics — Project Proposal Design
date: 2026-04-13
topic: proposal
---

# Project Proposal Design

## Job Posting

**Role:** Associate Data Analyst  
**Company:** Greenlight Financial Technology  
**Team:** Marketing Science  
**File:** `docs/job-posting.pdf`

Key skills required by posting: SQL, dbt, marketing metrics (CAC, LTV, cohort analysis), CRM analytics, attribution reporting, dashboard building, demonstrated AI proficiency (Claude specifically mentioned).

## Project Framing

**Title:** Fintech Equity Analytics — Trading Volume & Fundamentals Pipeline

**Core business questions:**
- Descriptive: Which fintech stocks attract the most trading volume, and how does that vary by sector and time?
- Diagnostic: Does trading volume correlate with company fundamentals (revenue growth, market cap)? Which events drive volume spikes in fintech equities?

**Transferability:** Transfers to any fintech, investment platform, or growth analytics role. Swap instruments for users and it becomes a product analytics project.

## Data Sources

| Layer | Source | Type | Notes |
|---|---|---|---|
| Source 1 | Alpaca Market Data API | REST API | Free tier, real OHLCV + volume data for fintech tickers |
| Source 2 | SEC EDGAR API | REST API / supplement | Free, company fundamentals (revenue, market cap, sector) |
| Source 3 | Web scrape | Knowledge base | Greenlight content, a16z fintech reports, CB Insights, competitor profiles |

## Star Schema

**Fact table:** `fact_daily_prices`
- Grain: one row per instrument per trading day
- Measures: open, high, low, close, volume, vwap
- FKs: instrument_key, company_key, date_key

**Dimension tables:**

| Table | Source | Key columns |
|---|---|---|
| `dim_instrument` | Alpaca | ticker, name, exchange, asset_class |
| `dim_company` | SEC EDGAR | company_name, sector, industry, market_cap, revenue, employees |
| `dim_date` | dbt seed | date, week, month, quarter, year, is_earnings_week |
| `dim_sector` | derived in dbt | sector_name, sector_category |

**Staging models:** `stg_alpaca_prices`, `stg_edgar_fundamentals`

**Instrument scope:** ~30-50 fintech tickers (SoFi, Block, Affirm, PayPal, Robinhood, etc.)

## Dashboard (Streamlit)

- **Descriptive view:** Volume leaders by sector over time — which fintech sectors dominate trading volume each month
- **Diagnostic view:** Volume vs. fundamentals scatter — does higher revenue growth correlate with volume spikes?
- **Interactive elements:** Sector filter, date range slider, ticker multi-select

## Knowledge Base

**Raw sources (15+ from 3+ sites):**
- Greenlight blog, press releases, About page
- a16z State of Fintech reports
- CB Insights Fintech Trends
- Competitor profiles (Chime, Step, Copper, Robinhood)
- Greenlight exec bios / LinkedIn profiles
- CFPB fintech reports, SEC fintech guidance

**Wiki pages (Claude Code-generated):**
1. `overview.md` — family fintech market landscape
2. `key-players.md` — Greenlight + competitors, business models
3. `market-trends.md` — growth drivers, regulatory environment, synthesis

## Pipeline Architecture

```
Alpaca API ──────────────┐
                         ├──> GitHub Actions ──> Snowflake Raw ──> dbt Staging ──> dbt Mart ──> Streamlit
SEC EDGAR API ───────────┘

Web Scrape ──> GitHub Actions ──> knowledge/raw/ ──> Claude Code ──> knowledge/wiki/
```

## Proposal Reflection (approved)

> The Greenlight Associate Data Analyst posting is a direct match for the skills built in this course. The role requires SQL proficiency, dbt model contributions, dashboard development, and marketing funnel analytics across acquisition and CRM channels — every one of which maps to coursework in this class. The posting also explicitly names Claude as a first-class tool in their analytics workflow, making demonstrated AI proficiency a requirement rather than a nice-to-have. My project builds an end-to-end fintech equity analytics pipeline: Alpaca Market Data and SEC EDGAR APIs feed raw price and fundamentals data into Snowflake, dbt staging and mart models transform it into a star schema, and a Streamlit dashboard surfaces descriptive and diagnostic insights about trading volume patterns across fintech sectors. A Claude Code-powered knowledge base synthesizes scraped fintech industry content — Greenlight press releases, competitor profiles, and market reports — into queryable wiki pages. This project proves I can do what the role requires: write SQL, build dimensional models, automate pipelines, and use AI to accelerate analytical work.
