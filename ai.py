import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
)


SYSTEM_PROMPT = """
당신은 매일 아침 경제 브리핑을 작성하는 경제 전문 에디터이다.

반드시 아래 형식을 지켜라.

# 오늘의 경제 브리핑

## 1. 핵심 뉴스 3개

각 뉴스마다

- 제목
- 세 줄 요약
- 왜 중요한가

작성

## 2. 오늘의 핵심 경제용어

경제용어 2개

각각 2~3줄 설명

## 3. 오늘 시장 영향

국내 증시

미국 증시

환율

금리

에 어떤 영향을 줄 가능성이 있는지 설명

## 4. 오늘 한 줄 요약

30자 이내
"""


def make_briefing(articles):

    article_text = ""

    for idx, article in enumerate(articles, start=1):

        article_text += f"""
기사 {idx}

제목
{article["title"]}

본문
{article["content"]}

원문
{article["url"]}

----------------------------------------

"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": article_text
            }
        ]
    )

    return response.output_text
