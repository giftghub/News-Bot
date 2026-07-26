import os
from datetime import datetime
from notion_client import Client

notion = Client(auth=os.environ["NOTION_TOKEN"])
DATABASE_ID = os.environ["DATABASE_ID"]


def save_to_notion(briefing):

    today = datetime.today()

    notion.pages.create(
        parent={"database_id": DATABASE_ID},
        properties={
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": today.strftime("%Y-%m-%d 경제 브리핑")
                        }
                    }
                ]
            },
            "Date": {
                "date": {
                    "start": today.strftime("%Y-%m-%d")
                }
            }
        },
        children=[
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": briefing
                            }
                        }
                    ]
                }
            }
        ]
    )
