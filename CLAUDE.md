# CLAUDE.md — Fintech Equity Analytics Pipeline

## Project Context

This is a portfolio analytics engineering project targeting the **Associate Data Analyst** role at Greenlight Financial Technology. It demonstrates SQL, dbt dimensional modeling, pipeline automation, dashboard development, and AI-assisted analytical workflows.

**Core business questions:**
- Which fintech stocks attract the most trading volume, and how does that vary by sector over time?
- Does trading volume correlate with company fundamentals (revenue growth, market cap)?

## Repository Structure

```
data-analyst-fintech/
├── docs/                  # Proposal, job posting, design specs
├── extract/               # Python extraction scripts (API → Snowflake raw)
├── dbt/                   # dbt project (staging + mart models)
├── dashboard/             # Streamlit app
├── knowledge/
│   ├── raw/               # Scraped sources (15+ files, 3+ sites)
│   └── wiki/              # Claude Code-generated wiki pages
├── .github/workflows/     # GitHub Actions pipelines
├── CLAUDE.md              # This file
└── README.md              # Project overview
```

## Data Sources

| Source | Type | What it provides |
|---|---|---|
| Alpaca Market Data API | REST API | Real OHLCV price + volume for fintech tickers |
| SEC EDGAR API | REST API | Company fundamentals (revenue, market cap, sector) |
| Web scrape | Knowledge base | Fintech industry content |

## Star Schema

- **Fact:** `fact_daily_prices` (instrument × day grain)
- **Dims:** `dim_instrument`, `dim_company`, `dim_sector`, `dim_date`
- **Staging:** `stg_alpaca_prices`, `stg_edgar_fundamentals`

## Credentials & Secrets

Never commit credentials. All secrets are stored as environment variables and GitHub Actions secrets:
- `SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER`, `SNOWFLAKE_PASSWORD`, `SNOWFLAKE_DATABASE`, `SNOWFLAKE_WAREHOUSE`
- `ALPACA_API_KEY`, `ALPACA_SECRET_KEY`

Local development: use a `.env` file (already in `.gitignore`).

## Knowledge Base

The `knowledge/` folder is a queryable knowledge base about the fintech industry and Greenlight's competitive landscape.

### How to Query the Knowledge Base

When asked a question about the fintech industry, Greenlight, or competitors:

1. **Start with the index:** Read `knowledge/index.md` to find relevant wiki pages.
2. **Read the wiki first:** Wiki pages in `knowledge/wiki/` synthesize insights across sources. Answer from there when possible.
3. **Go to raw sources for specifics:** If the wiki doesn't have enough detail, read the relevant files in `knowledge/raw/`.
4. **Cite your sources:** When answering, name the wiki page or raw source file you drew from.
5. **Flag gaps:** If the knowledge base doesn't cover the question, say so explicitly rather than hallucinating.

### Wiki Pages

| Page | Summary |
|---|---|
| `knowledge/wiki/overview.md` | Family fintech market landscape and Greenlight's position |
| `knowledge/wiki/key-players.md` | Greenlight + competitors: business models and differentiation |
| `knowledge/wiki/market-trends.md` | Growth drivers, regulatory environment, synthesis across sources |

## Pipeline Commands

```bash
# Extract data
python extract/alpaca_prices.py
python extract/edgar_fundamentals.py

# Run dbt
cd dbt && dbt run && dbt test

# Run dashboard locally
streamlit run dashboard/app.py
```

## Milestones

| Milestone | Due | Status |
|---|---|---|
| Proposal | Apr 13, 2026 | Complete |
| Milestone 01: Extract, Load & Transform | Apr 27, 2026 | Pending |
| Milestone 02: Present & Polish | May 4, 2026 | Pending |
| Final Submission | May 11, 2026 | Pending |
