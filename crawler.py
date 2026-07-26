import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def get_article_text(url):
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    paragraphs = soup.select("article p")

    text = []

    for p in paragraphs:
        t = p.get_text(" ", strip=True)

        if len(t) > 20:
            text.append(t)

    return "\n".join(text)


def crawl(limit=10):

    url = "https://www.hankyung.com"

    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    articles = []
    seen = set()

    for a in soup.select("a.news-item, a.txt-cont, h2 a, h3 a"):

        title = a.get_text(strip=True)
        link = a.get("href")

        if not title or not link:
            continue

        if link.startswith("/"):
            link = "https://www.hankyung.com" + link

        if link in seen:
            continue

        seen.add(link)

        try:
            content = get_article_text(link)
        except Exception:
            continue

        articles.append({
            "title": title,
            "url": link,
            "content": content
        })

        if len(articles) >= limit:
            break

    return articles
