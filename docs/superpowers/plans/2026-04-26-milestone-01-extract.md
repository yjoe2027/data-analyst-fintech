# Milestone 01 Extract Scripts Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build two extraction scripts (WeatherAPI → Snowflake raw, CoinGecko → knowledge/raw markdown), plus credentials scaffolding and requirements.

**Architecture:** Each script is a standalone Python module that loads env vars via `python-dotenv`, calls its API with `requests`, and writes output (Snowflake for weather, markdown files for CoinGecko). No shared library needed at this stage. Tests use `unittest.mock` to avoid hitting live APIs.

**Tech Stack:** Python 3.x, `requests`, `snowflake-connector-python`, `python-dotenv`, `pytest`

---

## File Map

| Path | Action | Responsibility |
|---|---|---|
| `requirements.txt` | Create | All Python dependencies |
| `.env.example` | Create | Credential template (committed) |
| `.env` | Create | Local credentials (gitignored, user fills password) |
| `extract/weather_to_snowflake.py` | Create | WeatherAPI current weather → Snowflake RAW.WEATHER_RAW |
| `extract/coingecko_to_knowledge.py` | Create | CoinGecko markets API → knowledge/raw/*.md |
| `tests/test_weather_parse.py` | Create | Unit tests for weather record parsing |
| `tests/test_coingecko_format.py` | Create | Unit tests for markdown formatting |
| `knowledge/raw/.gitkeep` | Create | Ensure directory is tracked in git |
| `knowledge/wiki/.gitkeep` | Create | Ensure directory is tracked in git |

---

### Task 1: requirements.txt and dependency scaffolding

**Files:**
- Create: `requirements.txt`

- [ ] **Step 1: Write requirements.txt**

```
snowflake-connector-python==3.12.3
requests==2.32.3
python-dotenv==1.0.1
pytest==8.3.5
```

- [ ] **Step 2: Install dependencies**

Run: `pip install -r requirements.txt`
Expected: All packages install without error.

- [ ] **Step 3: Commit**

```bash
git add requirements.txt
git commit -m "feat: add requirements.txt for milestone 01 dependencies"
```

---

### Task 2: Credential scaffolding (.env.example and .env)

**Files:**
- Create: `.env.example`
- Create: `.env`

- [ ] **Step 1: Create .env.example**

```bash
# WeatherAPI
WEATHERAPI_KEY=your_weatherapi_key_here

# Snowflake
SNOWFLAKE_ACCOUNT=gjhezxb-lpb73600
SNOWFLAKE_USER=YUBINJOE
SNOWFLAKE_PASSWORD=your_password_here
SNOWFLAKE_DATABASE=basket_craft
SNOWFLAKE_SCHEMA=RAW
SNOWFLAKE_WAREHOUSE=basket_craft_wh
SNOWFLAKE_ROLE=basket_craft_loader
```

- [ ] **Step 2: Create .env with real credentials**

```bash
# WeatherAPI
WEATHERAPI_KEY=ff3cd52bbdbb45d7a29175240261304

# Snowflake
SNOWFLAKE_ACCOUNT=gjhezxb-lpb73600
SNOWFLAKE_USER=YUBINJOE
SNOWFLAKE_PASSWORD=FILL_IN_YOUR_PASSWORD
SNOWFLAKE_DATABASE=basket_craft
SNOWFLAKE_SCHEMA=RAW
SNOWFLAKE_WAREHOUSE=basket_craft_wh
SNOWFLAKE_ROLE=basket_craft_loader
```

- [ ] **Step 3: Verify .env is gitignored**

Run: `git check-ignore -v .env`
Expected: output like `.gitignore:139:.env    .env`

- [ ] **Step 4: Create knowledge directories**

```bash
mkdir -p knowledge/raw knowledge/wiki
touch knowledge/raw/.gitkeep knowledge/wiki/.gitkeep
mkdir -p extract tests
touch extract/__init__.py tests/__init__.py
```

- [ ] **Step 5: Commit .env.example and directory scaffolding**

```bash
git add .env.example knowledge/raw/.gitkeep knowledge/wiki/.gitkeep extract/__init__.py tests/__init__.py
git commit -m "feat: add credential template and directory structure for milestone 01"
```

---

### Task 3: WeatherAPI extraction script

**Files:**
- Create: `extract/weather_to_snowflake.py`
- Test: `tests/test_weather_parse.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_weather_parse.py`:

```python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from extract.weather_to_snowflake import parse_record

MOCK_API_RESPONSE = {
    "location": {
        "name": "New York",
        "region": "New York",
        "country": "United States of America",
        "lat": 40.71,
        "lon": -74.01,
        "localtime": "2026-04-26 10:00",
    },
    "current": {
        "temp_c": 15.0,
        "temp_f": 59.0,
        "condition": {"text": "Partly cloudy"},
        "wind_mph": 10.0,
        "wind_kph": 16.1,
        "humidity": 60,
        "feelslike_c": 14.0,
        "feelslike_f": 57.2,
        "uv": 4.0,
    },
}


def test_parse_record_extracts_location_fields():
    rec = parse_record(MOCK_API_RESPONSE)
    assert rec["location_name"] == "New York"
    assert rec["country"] == "United States of America"
    assert rec["lat"] == 40.71
    assert rec["lon"] == -74.01


def test_parse_record_extracts_weather_fields():
    rec = parse_record(MOCK_API_RESPONSE)
    assert rec["temp_c"] == 15.0
    assert rec["temp_f"] == 59.0
    assert rec["humidity"] == 60
    assert rec["condition_text"] == "Partly cloudy"
    assert rec["uv"] == 4.0


def test_parse_record_includes_extracted_at():
    rec = parse_record(MOCK_API_RESPONSE)
    assert "extracted_at" in rec
    assert rec["extracted_at"] is not None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_weather_parse.py -v`
Expected: `ImportError` or `ModuleNotFoundError` — `weather_to_snowflake` doesn't exist yet.

- [ ] **Step 3: Write extract/weather_to_snowflake.py**

```python
import os
import requests
import snowflake.connector
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

LOCATIONS = ["New York", "London", "San Francisco"]

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS WEATHER_RAW (
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
)
"""

INSERT_SQL = """
INSERT INTO WEATHER_RAW (
    location_name, region, country, lat, lon,
    temp_c, temp_f, condition_text, wind_mph, wind_kph,
    humidity, feelslike_c, feelslike_f, uv, local_time
) VALUES (
    %(location_name)s, %(region)s, %(country)s, %(lat)s, %(lon)s,
    %(temp_c)s, %(temp_f)s, %(condition_text)s, %(wind_mph)s, %(wind_kph)s,
    %(humidity)s, %(feelslike_c)s, %(feelslike_f)s, %(uv)s, %(local_time)s
)
"""


def fetch_weather(location: str) -> dict:
    url = "http://api.weatherapi.com/v1/current.json"
    params = {"key": os.environ["WEATHERAPI_KEY"], "q": location, "aqi": "no"}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def parse_record(data: dict) -> dict:
    loc = data["location"]
    cur = data["current"]
    return {
        "location_name": loc["name"],
        "region": loc["region"],
        "country": loc["country"],
        "lat": loc["lat"],
        "lon": loc["lon"],
        "temp_c": cur["temp_c"],
        "temp_f": cur["temp_f"],
        "condition_text": cur["condition"]["text"],
        "wind_mph": cur["wind_mph"],
        "wind_kph": cur["wind_kph"],
        "humidity": cur["humidity"],
        "feelslike_c": cur["feelslike_c"],
        "feelslike_f": cur["feelslike_f"],
        "uv": cur["uv"],
        "local_time": loc["localtime"],
        "extracted_at": datetime.now(timezone.utc).isoformat(),
    }


def _snowflake_conn():
    return snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
        database=os.environ["SNOWFLAKE_DATABASE"],
        schema=os.environ.get("SNOWFLAKE_SCHEMA", "RAW"),
        warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
        role=os.environ.get("SNOWFLAKE_ROLE"),
    )


def load_to_snowflake(records: list[dict]) -> None:
    conn = _snowflake_conn()
    cur = conn.cursor()
    try:
        cur.execute(CREATE_TABLE_SQL)
        for rec in records:
            cur.execute(INSERT_SQL, rec)
        conn.commit()
        print(f"Loaded {len(records)} records to WEATHER_RAW")
    finally:
        cur.close()
        conn.close()


def main():
    records = []
    for loc in LOCATIONS:
        print(f"Fetching weather for {loc}...")
        data = fetch_weather(loc)
        records.append(parse_record(data))
    load_to_snowflake(records)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_weather_parse.py -v`
Expected: 3 tests PASSED.

- [ ] **Step 5: Commit**

```bash
git add extract/weather_to_snowflake.py tests/test_weather_parse.py
git commit -m "feat: add WeatherAPI extraction script with Snowflake loader"
```

---

### Task 4: CoinGecko knowledge-base scraper

**Files:**
- Create: `extract/coingecko_to_knowledge.py`
- Test: `tests/test_coingecko_format.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_coingecko_format.py`:

```python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from extract.coingecko_to_knowledge import format_global_markdown, format_coins_markdown

MOCK_GLOBAL = {
    "active_cryptocurrencies": 12345,
    "total_market_cap": {"usd": 2_500_000_000_000},
    "total_volume": {"usd": 85_000_000_000},
    "market_cap_percentage": {"btc": 52.3, "eth": 17.1},
    "market_cap_change_percentage_24h_usd": 1.42,
}

MOCK_COINS = [
    {
        "market_cap_rank": 1,
        "name": "Bitcoin",
        "symbol": "btc",
        "current_price": 68000.0,
        "price_change_percentage_24h": 2.5,
        "market_cap": 1_300_000_000_000,
        "total_volume": 35_000_000_000,
    }
]


def test_format_global_markdown_contains_header():
    md = format_global_markdown(MOCK_GLOBAL)
    assert "# CoinGecko Global Crypto Market Overview" in md


def test_format_global_markdown_contains_metrics():
    md = format_global_markdown(MOCK_GLOBAL)
    assert "12,345" in md
    assert "52.3%" in md
    assert "1.42%" in md


def test_format_coins_markdown_contains_bitcoin():
    md = format_coins_markdown(MOCK_COINS)
    assert "Bitcoin" in md
    assert "BTC" in md
    assert "68,000" in md


def test_format_coins_markdown_has_table():
    md = format_coins_markdown(MOCK_COINS)
    assert "| Rank |" in md
    assert "|---|" in md
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_coingecko_format.py -v`
Expected: `ImportError` — `coingecko_to_knowledge` doesn't exist yet.

- [ ] **Step 3: Write extract/coingecko_to_knowledge.py**

```python
import os
import requests
from datetime import datetime, timezone

BASE_URL = "https://api.coingecko.com/api/v3"
OUTPUT_DIR = "knowledge/raw"


def fetch_global() -> dict:
    resp = requests.get(f"{BASE_URL}/global", timeout=10)
    resp.raise_for_status()
    return resp.json()["data"]


def fetch_top_coins(n: int = 25) -> list[dict]:
    resp = requests.get(
        f"{BASE_URL}/coins/markets",
        params={
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": n,
            "page": 1,
            "sparkline": False,
        },
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()


def format_global_markdown(data: dict) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    btc_pct = data["market_cap_percentage"].get("btc", 0)
    eth_pct = data["market_cap_percentage"].get("eth", 0)
    return "\n".join([
        "# CoinGecko Global Crypto Market Overview",
        "",
        f"_Scraped: {ts}_",
        "",
        "## Key Metrics",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Active Cryptocurrencies | {data['active_cryptocurrencies']:,} |",
        f"| Total Market Cap (USD) | ${data['total_market_cap']['usd']:,.0f} |",
        f"| Total 24h Volume (USD) | ${data['total_volume']['usd']:,.0f} |",
        f"| Bitcoin Market Cap % | {btc_pct:.1f}% |",
        f"| Ethereum Market Cap % | {eth_pct:.1f}% |",
        f"| Market Cap Change 24h % | {data['market_cap_change_percentage_24h_usd']:.2f}% |",
        "",
    ])


def format_coins_markdown(coins: list[dict]) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# CoinGecko Top Cryptocurrencies by Market Cap",
        "",
        f"_Scraped: {ts}_",
        "",
        "| Rank | Name | Symbol | Price (USD) | 24h Change % | Market Cap (USD) | 24h Volume (USD) |",
        "|---|---|---|---|---|---|---|",
    ]
    for c in coins:
        price = f"${c['current_price']:,.4f}" if c.get("current_price") else "N/A"
        change = f"{c['price_change_percentage_24h']:.2f}%" if c.get("price_change_percentage_24h") else "N/A"
        mcap = f"${c['market_cap']:,.0f}" if c.get("market_cap") else "N/A"
        vol = f"${c['total_volume']:,.0f}" if c.get("total_volume") else "N/A"
        lines.append(
            f"| {c['market_cap_rank']} | {c['name']} | {c['symbol'].upper()} "
            f"| {price} | {change} | {mcap} | {vol} |"
        )
    return "\n".join(lines)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    print("Fetching CoinGecko global market data...")
    global_data = fetch_global()
    global_md = format_global_markdown(global_data)
    global_path = os.path.join(OUTPUT_DIR, f"coingecko_global_{date_str}.md")
    with open(global_path, "w") as f:
        f.write(global_md)
    print(f"Saved: {global_path}")

    print("Fetching top 25 coins by market cap...")
    coins = fetch_top_coins(25)
    coins_md = format_coins_markdown(coins)
    coins_path = os.path.join(OUTPUT_DIR, f"coingecko_top_coins_{date_str}.md")
    with open(coins_path, "w") as f:
        f.write(coins_md)
    print(f"Saved: {coins_path}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_coingecko_format.py -v`
Expected: 4 tests PASSED.

- [ ] **Step 5: Commit**

```bash
git add extract/coingecko_to_knowledge.py tests/test_coingecko_format.py
git commit -m "feat: add CoinGecko scraper that saves markdown to knowledge/raw/"
```

---

### Task 5: Run all tests and smoke-test scripts

- [ ] **Step 1: Run full test suite**

Run: `pytest tests/ -v`
Expected: 7 tests PASSED, 0 failed.

- [ ] **Step 2: Smoke-test CoinGecko script (no credentials needed)**

Run: `python extract/coingecko_to_knowledge.py`
Expected: Two files created in `knowledge/raw/`:
- `knowledge/raw/coingecko_global_2026-04-26.md`
- `knowledge/raw/coingecko_top_coins_2026-04-26.md`

- [ ] **Step 3: Verify markdown files look correct**

Run: `head -20 knowledge/raw/coingecko_global_2026-04-26.md`
Expected: Markdown table with active cryptocurrencies count, market cap figures.

- [ ] **Step 4: Fill in Snowflake password in .env**

Edit `.env` and replace `FILL_IN_YOUR_PASSWORD` with your actual Snowflake password.

- [ ] **Step 5: Smoke-test WeatherAPI → Snowflake script**

Run: `python extract/weather_to_snowflake.py`
Expected:
```
Fetching weather for New York...
Fetching weather for London...
Fetching weather for San Francisco...
Loaded 3 records to WEATHER_RAW
```

- [ ] **Step 6: Commit generated knowledge files**

```bash
git add knowledge/raw/coingecko_global_*.md knowledge/raw/coingecko_top_coins_*.md
git commit -m "data: add initial CoinGecko market snapshots to knowledge base"
```
