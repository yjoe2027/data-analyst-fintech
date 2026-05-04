# Knowledge Base Index

**Domain:** Fintech — Weather & Market Sentiment  
**Sources:** 15+ articles from Investopedia, academic papers, financial news  
**Last updated:** See git history

---

## Wiki Pages (`knowledge/wiki/`)

| Page | Description |
|------|-------------|
| [overview.md](wiki/overview.md) | Project domain overview: weather × fintech |
| [key_entities.md](wiki/key_entities.md) | Key concepts, markets, and data definitions |
| [themes.md](wiki/themes.md) | Recurring themes across all scraped sources |

---

## Raw Sources (`knowledge/raw/`)

> Add your scraped files below as you populate this folder.
> Name files descriptively: `investopedia_weather_effect_markets.md`

| File | Source | Topic |
|------|--------|-------|
| _(populate after running firecrawl_to_knowledge.py)_ | | |

---

## Query Guide

Open Claude Code in this repository and ask questions like:

- *"What does behavioral finance research say about weather and stock returns?"*
- *"How do cloud cover and sunshine hours affect NYSE trading volume?"*
- *"What are the main fintech trends in London's financial market?"*
- *"Summarize the Investopedia articles about investor psychology and weather"*
- *"What risk factors does weather introduce into algorithmic trading?"*

Claude Code reads `knowledge/wiki/` first, then falls back to `knowledge/raw/`.
See [CLAUDE.md](../CLAUDE.md) for full query conventions.
