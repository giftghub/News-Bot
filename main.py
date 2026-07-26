import os
from datetime import datetime
from notion_client import Client

# Notion 연결
notion = Client(auth=os.environ["NOTION_TOKEN"])

DATABASE_ID = os.environ["DATABASE_ID"]

today = datetime.now().strftime("%Y-%m-%d")

# 테스트용: 오늘 날짜만 추가
notion.pages.create(
    parent={"database_id": DATABASE_ID},
    properties={
        "Name": {
            "title": [
                {
                    "text": {
                        "content": today
                    }
                }
            ]
        }
    }
)

print("노션에 테스트 행을 추가했습니다!")
