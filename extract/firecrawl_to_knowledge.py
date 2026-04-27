import os
from datetime import datetime, timezone
from firecrawl import V1FirecrawlApp as FirecrawlApp
from dotenv import load_dotenv

load_dotenv()

OUTPUT_DIR = "knowledge/raw"

URLS = [
    ("https://www.investopedia.com/terms/f/fintech.asp", "investopedia_fintech"),
]


def scrape_to_markdown(url: str, app: FirecrawlApp) -> str:
    result = app.scrape_url(url, formats=["markdown"])
    return result.markdown


def save_markdown(content: str, slug: str) -> str:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    path = os.path.join(OUTPUT_DIR, f"{slug}_{date_str}.md")
    with open(path, "w") as f:
        f.write(content)
    return path


def main():
    app = FirecrawlApp(api_key=os.environ["FIRECRAWL_API_KEY"])
    for url, slug in URLS:
        print(f"Scraping {url}...")
        content = scrape_to_markdown(url, app)
        path = save_markdown(content, slug)
        print(f"Saved: {path}")


if __name__ == "__main__":
    main()
