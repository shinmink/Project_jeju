# BeautifulSoup로 HTML → 순수 텍스트 정제 후 파일로 저장
import csv
import requests
from bs4 import BeautifulSoup
import unicodedata


# HTML 가져오기
url = "https://quotes.toscrape.com/"
html = requests.get(url, timeout=5).text
soup = BeautifulSoup(html, "html.parser")


# 텍스트 + 메타데이터 추출 (태그 제거 → 순수 텍스트)
records = []
for q in soup.select("div.quote"):
    quote = q.select_one("span.text").get_text(" ", strip=True)
    # “…” 제거·공백 정리
    author = q.select_one("small.author").string.strip()
    quote = unicodedata.normalize("NFKC", quote)
    # 유니코드 정규화(선택)
    records.append((quote, author))

# CSV 저장
with open("quotes.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["quote", "author"])
    writer.writerows(records)

# TXT(라인 단위) 저장
with open("quotes.txt", "w", encoding="utf-8") as f:
    for quote, author in records:
        f.write(f"{quote} ― {author}\n")