import csv
import requests
from bs4 import BeautifulSoup
import unicodedata

# 1. 대상 URL
url = "https://quotes.toscrape.com/"
print(f"[1] URL 접속 중: {url}")

try:
    html = requests.get(url, timeout=5).text
    print("[2] HTML 다운로드 성공 ✅")
except Exception as e:
    print(f"[오류] 요청 실패: {e}")
    exit()

# 2. BeautifulSoup으로 파싱
soup = BeautifulSoup(html, "html.parser")
print("[3] HTML 파싱 완료 ✅")

# 3. 인용구 텍스트와 저자 정보 추출
records = []
quotes = soup.select("div.quote")
print(f"[4] 인용구 블록 수: {len(quotes)}개")

for i, q in enumerate(quotes, 1):
    quote = q.select_one("span.text").get_text(" ", strip=True)
    quote = unicodedata.normalize("NFKC", quote)  # 유니코드 정규화 (줄임표, 따옴표 등 통일)
    author = q.select_one("small.author").string.strip()
    records.append((quote, author))
    print(f"    {i:>2}. \"{quote}\" - {author}")

# 4. CSV 파일 저장
csv_filename = "quotes.csv"
with open(csv_filename, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["quote", "author"])  # 헤더
    writer.writerows(records)
print(f"[5] ✅ CSV 저장 완료: {csv_filename}")

# 5. TXT 파일 저장
txt_filename = "quotes.txt"
with open(txt_filename, "w", encoding="utf-8") as f:
    for quote, author in records:
        f.write(f"{quote} ― {author}\n")
print(f"[6] ✅ TXT 저장 완료: {txt_filename}")