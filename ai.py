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

경제용어를 2~3개 선정하세요.

반드시 아래 형식을 지키세요.

용어 : 설명

예시)

PPI : 생산자물가지수
GDP : 국내총생산
PER : 주가수익비율

## 한줄 정리

반드시 한 문장으로만 작성하세요.

예시)

미국 물가 둔화 기대가 커지며 반도체와 성장주 중심의 투자심리가 개선됐다.
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
