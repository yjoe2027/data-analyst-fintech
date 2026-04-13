# Project Proposal: Fintech Equity Analytics Pipeline

## Job Posting

**Role:** Associate Data Analyst  
**Company:** Greenlight Financial Technology  
**File:** [`docs/job-posting.pdf`](job-posting.pdf)

---

## Project Overview

**Title:** Fintech Equity Analytics — Trading Volume & Fundamentals Pipeline

An end-to-end analytics pipeline that ingests real fintech equity data from two APIs, transforms it through a dimensional model in Snowflake using dbt, and surfaces descriptive and diagnostic insights through a deployed Streamlit dashboard. A Claude Code-powered knowledge base synthesizes scraped fintech industry content into queryable wiki pages.

**Core business questions:**
- Which fintech stocks attract the most trading volume, and how does that vary by sector over time?
- Does trading volume correlate with company fundamentals like revenue growth and market cap?

---

## Reflection

The Greenlight Associate Data Analyst posting is a direct match for the skills built in this course. The role requires SQL proficiency, dbt model contributions, dashboard development, and marketing funnel analytics across acquisition and CRM channels — every one of which maps to coursework in this class. The posting also explicitly names Claude as a first-class tool in their analytics workflow, making demonstrated AI proficiency a requirement rather than a nice-to-have. My project builds an end-to-end fintech equity analytics pipeline: Alpaca Market Data and SEC EDGAR APIs feed raw price and fundamentals data into Snowflake, dbt staging and mart models transform it into a star schema, and a Streamlit dashboard surfaces descriptive and diagnostic insights about trading volume patterns across fintech sectors. A Claude Code-powered knowledge base synthesizes scraped fintech industry content — Greenlight press releases, competitor profiles, and market reports — into queryable wiki pages. This project proves I can do what the role requires: write SQL, build dimensional models, automate pipelines, and use AI to accelerate analytical work.

---

## Data Sources

| # | Source | Type | What it provides |
|---|---|---|---|
| 1 | [Alpaca Market Data API](https://alpaca.markets/docs/market-data/) | REST API | Real OHLCV price + volume data for fintech equities |
| 2 | [SEC EDGAR API](https://www.sec.gov/developer) | REST API | Company fundamentals: revenue, market cap, sector, employees |
| 3 | Web scrape | Knowledge base | Greenlight content, fintech industry reports, competitor profiles |

---

## Tech Stack

| Layer | Tool |
|---|---|
| Data Warehouse | Snowflake |
| Transformation | dbt |
| Orchestration | GitHub Actions |
| Dashboard | Streamlit (deployed to Streamlit Community Cloud) |
| Knowledge Base | Claude Code |
| Version Control | Git + GitHub (public repo) |

---

## Star Schema (planned)

**Fact:** `fact_daily_prices` — one row per instrument per trading day (open, high, low, close, volume, vwap)

**Dimensions:** `dim_instrument`, `dim_company`, `dim_sector`, `dim_date`

---

## GitHub Repository

[github.com/yjoe2027/data-analyst-fintech](https://github.com/yjoe2027/data-analyst-fintech)
