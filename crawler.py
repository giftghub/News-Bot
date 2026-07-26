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

    def extract_article_body(self, url):

        response = self.session.get(url, timeout=20)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        # ---------- 1순위 : JSON-LD ----------
        for script in soup.find_all("script", type="application/ld+json"):

            if not script.string:
                continue

            try:
                data = json.loads(script.string)

                if isinstance(data, list):
                    items = data
                else:
                    items = [data]

                for item in items:

                    if not isinstance(item, dict):
                        continue

                    body = item.get("articleBody")

                    if body:

                        body = self.clean_text(body)

                        if len(body) > 300:
                            return body

            except Exception:
                pass

        # ---------- 2순위 : article 태그 ----------
        article = soup.find("article")

        if article:

            paragraphs = article.find_all("p")

            if paragraphs:

                text = "\n".join(
                    p.get_text(" ", strip=True)
                    for p in paragraphs
                )

                text = self.clean_text(text)

                if len(text) > 300:
                    return text

        # ---------- 3순위 : div 후보 ----------
        candidates = [
            "#articletxt",
            ".article-body",
            ".article_txt",
            ".articleBody",
            ".news-view",
            ".newsView",
            ".detail-body",
            ".view-content"
        ]

        for selector in candidates:

            node = soup.select_one(selector)

            if not node:
                continue

            text = node.get_text("\n", strip=True)

            text = self.clean_text(text)

            if len(text) > 300:
                return text

        return ""


    def clean_text(self, text):

        remove_patterns = [

            r"ⓒ.*",

            r"무단전재.*",

            r"재배포.*",

            r"기자.*?=", 

            r"Google.*",

            r"▶.*",

            r"\[.*?사진.*?\]",

        ]

        text = text.replace("\xa0", " ")

        for pattern in remove_patterns:
            text = re.sub(pattern, "", text)

        text = re.sub(r"\n+", "\n", text)

        text = re.sub(r"[ \t]+", " ", text)

        return text.strip()

    def crawl(self, limit=10):

        articles = self.collect_article_links(limit)

        results = []

        for article in articles:

            try:

                content = self.extract_article_body(article["url"])

                if len(content) < 300:
                    continue

                results.append({
                    "title": article["title"],
                    "url": article["url"],
                    "content": content
                })

            except Exception as e:

                print(e)

        return results
