# crawler.py

import json
import re
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/138.0 Safari/537.36"
    )
}

BASE_URL = "https://www.hankyung.com"


class HankyungCrawler:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def get_main_page(self):

        response = self.session.get(BASE_URL, timeout=20)
        response.raise_for_status()

        return BeautifulSoup(response.text, "lxml")

    def collect_article_links(self, limit=10):

        soup = self.get_main_page()

        articles = []
        visited = set()

        selectors = [
            "a.news-item",
            "a.txt-cont",
            "h2 a",
            "h3 a",
            "a[href*='/article/']"
        ]

        for selector in selectors:

            for tag in soup.select(selector):

                title = tag.get_text(" ", strip=True)
                href = tag.get("href")

                if not href:
                    continue

                if "/article/" not in href:
                    continue

                if href.startswith("/"):
                    href = BASE_URL + href

                href = href.split("?")[0]

                if href in visited:
                    continue

                visited.add(href)

                articles.append(
                    {
                        "title": title,
                        "url": href
                    }
                )

        cleaned = []

        for article in articles:

            if len(article["title"]) < 8:
                continue

            cleaned.append(article)

        return cleaned[:limit]
