import os
import feedparser
from datetime import datetime
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
DATABASE_ID = os.environ["DATABASE_ID"]

notion = Client(auth=NOTION_TOKEN)

print("=" * 50)
print("DATABASE_ID:", DATABASE_ID)

# 데이터베이스 확인
db = notion.databases.retrieve(database_id=DATABASE_ID)
print("Database title:", db["title"][0]["plain_text"])
print("=" * 50)

# RSS 가져오기
feed = feedparser.parse("https://www.hankyung.com/feed/all-news")

print(f"기사 개수: {len(feed.entries)}")

today = datetime.today()

for rank, article in enumerate(feed.entries[:2], start=1):

    print(f"\n[{rank}] {article.title}")

    response = notion.pages.create(
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
                            "content": article.title
                        }
                    }
                ]
            },
            "URL": {
                "url": article.link
            }
        }
    )

    print("생성 완료!")
    print("Page URL:", response["url"])

print("\n모든 작업 완료!")
