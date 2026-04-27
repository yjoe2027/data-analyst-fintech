import sys
import os
import tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from unittest.mock import MagicMock, patch
from extract.firecrawl_to_knowledge import scrape_to_markdown, save_markdown


def test_scrape_to_markdown_returns_content():
    mock_app = MagicMock()
    mock_app.scrape_url.return_value.markdown = "# Fintech\n\nContent here"
    result = scrape_to_markdown("https://example.com", mock_app)
    assert result == "# Fintech\n\nContent here"
    mock_app.scrape_url.assert_called_once_with("https://example.com", formats=["markdown"])


def test_save_markdown_creates_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        with patch("extract.firecrawl_to_knowledge.OUTPUT_DIR", tmpdir):
            path = save_markdown("# Test content", "test_slug")
            assert os.path.exists(path)
            with open(path) as f:
                assert f.read() == "# Test content"


def test_save_markdown_filename_contains_slug():
    with tempfile.TemporaryDirectory() as tmpdir:
        with patch("extract.firecrawl_to_knowledge.OUTPUT_DIR", tmpdir):
            path = save_markdown("content", "investopedia_fintech")
            assert "investopedia_fintech" in os.path.basename(path)
