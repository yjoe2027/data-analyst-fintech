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
