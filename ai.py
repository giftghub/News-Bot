import os
from google import genai

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)

SYSTEM_PROMPT = """
당신은 경제 뉴스 에디터입니다.

여러 개의 경제기사를 읽고
하루 경제 브리핑을 작성하세요.

형식

# 오늘의 경제 브리핑

## 핵심 이슈

(전체 흐름 요약)

## 주요 뉴스

- ...
- ...
- ...

## 오늘 알아둘 경제용어

- 용어 : 설명

## 한줄 정리

...
"""

def make_briefing(articles):

    article_text = ""

    for idx, article in enumerate(articles, start=1):

        article_text += f"""

기사 {idx}

제목
{article['title']}

본문
{article['content'][:2000]}

원문
{article['url']}

----------------------------

"""

    response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=SYSTEM_PROMPT + article_text
)
    return response.text
