import re
import requests
from bs4 import BeautifulSoup

# 1. HTML 가져오기
url = "https://quotes.toscrape.com/"
print(f"[1] URL 접속 중: {url}")

try:
    html = requests.get(url, timeout=5).text
    print("[2] HTML 로딩 성공 ✅")
except Exception as e:
    print(f"[오류] 요청 실패: {e}")
    exit()

# 2. 파싱
soup = BeautifulSoup(html, "html.parser")
print("[3] HTML 파싱 완료 ✅")

# 3. quote 블록 추출
quotes = soup.find_all("div", class_="quote")
print(f"[4] 인용구 개수: {len(quotes)}개")

# 4. 각 인용구에서 텍스트와 저자 추출
for i, q in enumerate(quotes, 1):
    text = q.find("span", class_="text").get_text(strip=True)
    author = q.find("small", class_="author").string
    print(f"💬 {i}. {text} - {author}")

# 5. 정규표현식으로 외부 링크 추출 (http 또는 https로 시작)
external_links = soup.find_all("a", href=re.compile(r"^https?://"))
print(f"\n[5] 외부 링크 개수: {len(external_links)}개")
for i, a in enumerate(external_links, 1):
    print(f"🌐 외부 링크 {i}: {a['href']}")

# 6. CSS 선택자 활용: div.tags 내부의 a.tag
tag_elems = soup.select("div.tags a.tag")   # div.tags 내부의 a.tag 전부 선택
tags = sorted({t.string for t in tag_elems})
print(f"\n[6] 이 페이지에 등장한 태그들: {', '.join(tags)}")