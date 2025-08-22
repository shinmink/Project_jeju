import re
import requests
from bs4 import BeautifulSoup

# HTML 가져오기 (1·2단계와 동일)
url = "https://quotes.toscrape.com/" # 예시용 데모 사이트
html = requests.get(url, timeout=5).text
soup = BeautifulSoup(html, "html.parser")

# 클래스 이름으로 여러 요소 선택하기 (태그 이름 & 클래스 조합 검색)
quotes = soup.find_all("div", class_="quote")
# <div class="quote">···</div> 전부
for q in quotes:
    text = q.find("span", class_="text").get_text(strip=True)
    author = q.find("small", class_="author").string
    print(f"- {text} ({author})")

# 정규표현식으로 특정 속성값 필터링 (URL·ID 등 패턴으로 필터링)
external_links = soup.find_all("a", href=re.compile(r"^https?://"))
for a in external_links:
    print("외부 링크:", a["href"])

# CSS 선택자 문법 사용 필터링
tag_elems = soup.select("div.tags a.tag")   # div.tags 내부의 a.tag 전부
tags = sorted({t.string for t in tag_elems})
print("이 페이지에 등장한 태그:", ", ".join(tags))