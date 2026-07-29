"""
Base Scraper Class
AI Powered Government Jobs Telegram Bot
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import Optional


class BaseScraper:
    name: str = "BaseScraper"
    BASE_URL: str = ""
    timeout: int = 20

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9"
        })

    def fetch(self, url: str) -> Optional[str]:
        try:
            res = self.session.get(url, timeout=self.timeout)
            res.raise_for_status()
            return res.text
        except Exception:
            return None

    def soup(self, url: str) -> BeautifulSoup:
        html = self.fetch(url) or "<html><body></body></html>"
        return BeautifulSoup(html, "lxml")

    @staticmethod
    def clean(text: Optional[str]) -> str:
        if not text:
            return ""
        return " ".join(str(text).split()).strip()

    @staticmethod
    def absolute(base: str, href: Optional[str]) -> str:
        if not href:
            return ""
        return urljoin(base, href.strip())

    def scrape(self):
        raise NotImplementedError("Subclasses must implement scrape()")
