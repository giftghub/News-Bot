import os
import feedparser
from datetime import datetime
from notion_client import Client

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
DATABASE_ID = os.environ["DATABASE_ID"]

notion = Client(auth=NOTION_TOKEN)

feed = feedparser.parse("https://www.hankyung.com/feed/all-news")

today = datetime.today()

for rank, article in enumerate(feed.entries[:2], start=1):

    notion.pages.create(
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

print("뉴스 저장 완료!")
