import os
from datetime import datetime
from notion_client import Client

notion = Client(auth=os.environ["NOTION_TOKEN"])
DATABASE_ID = os.environ["DATABASE_ID"]


# -----------------------------
# 블록 생성 함수
# -----------------------------

def heading1(text):
    return {
        "object": "block",
        "type": "heading_1",
        "heading_1": {
            "rich_text": [{
                "type": "text",
                "text": {"content": text}
            }]
        }
    }


def heading2(text):
    return {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{
                "type": "text",
                "text": {"content": text}
            }]
        }
    }


def paragraph(text):
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{
                "type": "text",
                "text": {"content": text}
            }]
        }
    }


def bullet(text):
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "rich_text": [{
                "type": "text",
                "text": {"content": text}
            }]
        }
    }


def callout(text, emoji):
    return {
        "object": "block",
        "type": "callout",
        "callout": {
            "icon": {
                "type": "emoji",
                "emoji": emoji
            },
            "rich_text": [{
                "type": "text",
                "text": {
                    "content": text
                }
            }]
        }
    }


# -----------------------------
# 긴 문단 분할
# -----------------------------

def split_text(text, limit=1800):

    chunks = []

    while len(text) > limit:
        chunks.append(text[:limit])
        text = text[limit:]

    if text:
        chunks.append(text)

    return chunks


# -----------------------------
# 저장
# -----------------------------

def save_to_notion(briefing):

    today = datetime.today()

    # -----------------------------
    # 한줄 정리 추출
    # -----------------------------
    opinion = ""

    lines = [line.strip() for line in briefing.split("\n")]

    for i, line in enumerate(lines):
        if line == "## 한줄 정리":
            for next_line in lines[i + 1:]:
                if next_line:
                    opinion = next_line
                    break
            break

    # -----------------------------
    # 페이지 생성
    # -----------------------------
    page = notion.pages.create(
        parent={
            "database_id": DATABASE_ID
        },

        properties={

            "Name": {
                "title": [{
                    "text": {
                        "content": today.strftime("%Y-%m-%d 경제 브리핑")
                    }
                }]
            },

            "Date": {
                "date": {
                    "start": today.strftime("%Y-%m-%d")
                }
            },

            "Opinion": {
                "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": opinion
                    }
                }]
            }

        }
    )

    page_id = page["id"]

    blocks = []

    current_section = ""

    for line in lines:

        if not line:
            continue

        # 제목
        if line.startswith("# "):
            blocks.append(
                heading1(line.replace("# ", ""))
            )
            continue

        # 소제목
        if line.startswith("## "):

            current_section = line.replace("## ", "")

            blocks.append(
                heading2(current_section)
            )

            continue

        # 뉴스
        if line.startswith("- "):
            blocks.append(
                bullet(line[2:])
            )
            continue

        # 경제용어
        if current_section == "오늘 알아둘 경제용어":

            if ":" in line:

                word, desc = line.split(":", 1)

                blocks.append(
                    callout(
                        f"{word.strip()}\n{desc.strip()}",
                        "💡"
                    )
                )

            else:
                blocks.append(
                    paragraph(line)
                )

            continue

        # 한줄정리
        if current_section == "한줄 정리":

            blocks.append(
                callout(line, "📌")
            )

            continue

        # 일반 문단
        for chunk in split_text(line):
            blocks.append(
                paragraph(chunk)
            )

    # Notion은 한번에 최대 100개 블록
    for i in range(0, len(blocks), 100):

        notion.blocks.children.append(
            block_id=page_id,
            children=blocks[i:i+100]
        )
