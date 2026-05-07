import os
from datetime import datetime, timezone
from firecrawl import V1FirecrawlApp as FirecrawlApp
from dotenv import load_dotenv

load_dotenv()

OUTPUT_DIR = "knowledge/raw"

URLS = [
    # Fintech fundamentals
    ("https://www.investopedia.com/terms/f/fintech.asp",                                 "investopedia_fintech"),
    ("https://www.investopedia.com/neobank-definition-5196454",                          "investopedia_neobank"),
    ("https://www.investopedia.com/terms/d/digital-wallet.asp",                          "investopedia_digital_wallet"),
    ("https://www.investopedia.com/terms/i/interchange-fee.asp",                         "investopedia_interchange_fee"),
    ("https://www.investopedia.com/terms/p/prepaid-debit-cards.asp",                     "investopedia_prepaid_debit"),
    ("https://www.investopedia.com/terms/d/dodd-frank-financial-regulatory-reform-bill.asp", "investopedia_dodd_frank"),
    ("https://www.investopedia.com/terms/f/financial-literacy.asp",                      "investopedia_financial_literacy"),

    # Marketing analytics — role vocabulary
    ("https://www.investopedia.com/terms/c/customer-acquisition-cost.asp",               "investopedia_cac"),
    ("https://www.investopedia.com/terms/c/customer-lifetime-value.asp",                 "investopedia_clv"),
    ("https://www.investopedia.com/terms/c/churnrate.asp",                               "investopedia_churn_rate"),
    ("https://www.investopedia.com/terms/p/paybackperiod.asp",                           "investopedia_payback_period"),
    ("https://www.investopedia.com/terms/r/returnoninvestment.asp",                      "investopedia_roi"),
    ("https://www.investopedia.com/terms/c/cohort-analysis.asp",                         "investopedia_cohort_analysis"),

    # Behavioral finance and market sentiment
    ("https://www.investopedia.com/terms/b/behavioralfinance.asp",                       "investopedia_behavioral_finance"),
    ("https://www.investopedia.com/terms/m/marketsentiment.asp",                         "investopedia_market_sentiment"),
    ("https://www.investopedia.com/terms/i/investorsentiment.asp",                       "investopedia_investor_sentiment"),

    # Gen Z and subscription business context
    ("https://www.investopedia.com/terms/s/subscription-business-model.asp",             "investopedia_subscription_model"),
    ("https://www.investopedia.com/terms/g/generation-z.asp",                            "investopedia_gen_z"),
]


def scrape_to_markdown(url: str, app: FirecrawlApp) -> str:
    result = app.scrape_url(url, formats=["markdown"])
    return result.markdown


def already_scraped(slug: str) -> bool:
    if not os.path.isdir(OUTPUT_DIR):
        return False
    return any(f.startswith(slug + "_") for f in os.listdir(OUTPUT_DIR))


def save_markdown(content: str, slug: str) -> str:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    path = os.path.join(OUTPUT_DIR, f"{slug}_{date_str}.md")
    with open(path, "w") as f:
        f.write(content)
    return path


def main():
    app = FirecrawlApp(api_key=os.environ["FIRECRAWL_API_KEY"])
    scraped, skipped, failed = [], [], []

    for url, slug in URLS:
        if already_scraped(slug):
            print(f"SKIP (exists): {slug}")
            skipped.append(slug)
            continue
        try:
            print(f"Scraping: {url}")
            content = scrape_to_markdown(url, app)
            path = save_markdown(content, slug)
            print(f"  Saved: {path}")
            scraped.append(slug)
        except Exception as e:
            print(f"  ERROR {slug}: {e}")
            failed.append((slug, str(e)))

    print(f"\nDone — scraped: {len(scraped)}, skipped: {len(skipped)}, failed: {len(failed)}")
    if failed:
        for slug, err in failed:
            print(f"  FAILED: {slug}: {err}")


if __name__ == "__main__":
    main()
