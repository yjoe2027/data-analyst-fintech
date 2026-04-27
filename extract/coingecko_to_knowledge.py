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
