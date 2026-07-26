from crawler import crawl
from ai import make_briefing
from notion_db import save_to_notion

print("=" * 50)
print("기사 수집 시작")
print("=" * 50)

articles = crawl(limit=10)

print(f"{len(articles)}개 기사 수집 완료")

if not articles:
    raise Exception("기사가 없습니다.")

print("=" * 50)
print("Gemini 브리핑 생성")
print("=" * 50)

briefing = make_briefing(articles)

print("=" * 50)
print("Notion 업로드")
print("=" * 50)

save_to_notion(briefing)

print("=" * 50)
print("완료!")
print("=" * 50)
