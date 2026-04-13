# Project Proposal

**Name:** [Your name]

**Project Name:** Fintech Equity Analytics — Trading Volume & Fundamentals Pipeline

**GitHub Repo:** [github.com/yjoe2027/data-analyst-fintech](https://github.com/yjoe2027/data-analyst-fintech)

## Job Posting

- **Role:** Associate Data Analyst
- **Company:** Greenlight Financial Technology
- **Link:** https://jobs.lever.co/greenlight/beded9c4-6acf-4fcc-8aa9-8870555d2bfb

**SQL requirement (quote the posting):** "Coursework, academic projects, internships, or self-directed work that demonstrates you can write SQL queries, think through data problems, and pull meaningful signal from messy data."

## Reflection

The Greenlight Associate Data Analyst posting is a direct match for the skills built in this course: it explicitly requires SQL proficiency, dbt model contributions, dashboard development, and pipeline automation — and it even calls out Claude by name as a first-class tool the team uses to write and review SQL, making demonstrated AI proficiency a hard requirement rather than a bonus. To prove I can do this work, I'm building an end-to-end fintech equity analytics pipeline where Alpaca Market Data and SEC EDGAR APIs feed real OHLCV price and company fundamentals data into Snowflake, dbt staging and mart layers transform it into a star schema (fact_daily_prices + dimension tables for instrument, company, sector, and date), and a Streamlit dashboard surfaces descriptive and diagnostic insights about trading volume patterns across fintech sectors — all automated via GitHub Actions. A Claude Code-powered knowledge base synthesizes scraped fintech industry content — Greenlight press releases, competitor profiles, a16z market reports — into queryable wiki pages that I can demo live. Beyond this specific role, the same project transfers directly to a Data Analyst position at any consumer fintech (Chime, SoFi, Robinhood), a Business Intelligence Analyst role at an investment or financial services platform, or an Analytics Engineer role at a fintech startup — the dimensional model, pipeline, and dashboard are the core artifacts any of those teams would actually use.
