import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
DATABASE_ID = os.environ["DATABASE_ID"]

notion = Client(auth=NOTION_TOKEN)

print("=" * 50)
print("DATABASE_ID:", DATABASE_ID)

db = notion.databases.retrieve(database_id=DATABASE_ID)
print("Database title:", db["title"][0]["plain_text"])
print("=" * 50)

headers = {
    "User-Agent": "Mozilla/5.0"
}

url = "https://www.hankyung.com"

response = requests.get(url, headers=headers)

print("HTTP Status:", response.status_code)

response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

articles = []

# 메인 기사 제목 추출
for a in soup.select("a.news-item, a.txt-cont, h2 a, h3 a"):

    title = a.get_text(strip=True)
    link = a.get("href")

    if not title:
        continue

    if not link:
        continue

    if link.startswith("/"):
        link = "https://www.hankyung.com" + link

    if link.startswith("https://www.hankyung.com"):

        if (title, link) not in articles:
            articles.append((title, link))

print("기사 개수:", len(articles))

def get_article_text(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, headers=headers)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    paragraphs = soup.select("article p")

    text = []

    for p in paragraphs:
        t = p.get_text(" ", strip=True)
        if len(t) > 20:
            text.append(t)

    return "\n".join(text)
    
today = datetime.today()

today = datetime.today()

def already_uploaded():
    result = notion.databases.query(
        database_id=DATABASE_ID,
        filter={
            "property": "Date",
            "date": {
                "equals": today.strftime("%Y-%m-%d")
            }
        }
    )
    return len(result["results"]) > 0

if already_uploaded():
    print("오늘 브리핑이 이미 존재합니다.")
    exit()

for rank, (title, link) in enumerate(articles[:2], start=1):

for rank, (title, link) in enumerate(articles[:2], start=1):

    print(f"\n[{rank}] {title}")

   try:
    content = get_article_text(link)
except Exception as e:
    print(e)
    continue

    print(content[:500])   # 테스트용

    page = notion.pages.create(
        parent={"database_id": DATABASE_ID},
        properties={
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": f"{today.strftime('%Y-%m-%d')} - {rank}"
                        }
                    }
                ]
            },
            "Date": {
                "date": {
                    "start": today.strftime("%Y-%m-%d")
                }
            },
            "Rank": {
                "number": rank
            },
            "Headline": {
                "rich_text": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            },
            "URL": {
                "url": link
            }
        }
    )

    print("생성 완료")
    print(page["url"])

print("\n모든 작업 완료!")
