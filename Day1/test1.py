import csv
import requests
from bs4 import BeautifulSoup

url = "https://www.imdb.com/chart/top"
headers = {
    "User-Agent": "Mozilla/5.0"  # IMDb는 간단한 UA 헤더 없으면 차단 가능성 있음
}

print(f"[1] IMDb 접속 중: {url}")
try:
    res = requests.get(url, headers=headers, timeout=5)
    res.raise_for_status()
    print("[2] HTML 다운로드 성공 ✅")
except Exception as e:
    print(f"[오류] 요청 실패: {e}")
    exit()

soup = BeautifulSoup(res.text, "html.parser")
movies = soup.select("li.ipc-metadata-list-summary-item")

print(f"[3] 영화 항목 수: {len(movies)}개")
records = []

for i, movie in enumerate(movies, 1):
    # 제목
    title_tag = movie.select_one("h3")
    title = title_tag.get_text(strip=True).split('. ', 1)[1] if title_tag else "N/A"

    # 연도
    year_tag = movie.select_one("span.ipc-title__subtext")
    year = year_tag.get_text(strip=True).strip("()") if year_tag else "N/A"

    # 평점
    rating_tag = movie.select_one("span.ipc-rating-star")
    rating = rating_tag.get_text(strip=True) if rating_tag else "N/A"

    print(f"  {i:>3}. {title} ({year}) - {rating}")
    records.append((i, title, year, rating))

# CSV 저장
csv_filename = "imdb_top250.csv"
with open(csv_filename, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["순위", "제목", "제작연도", "평점"])
    writer.writerows(records)
print(f"[4] ✅ CSV 저장 완료: {csv_filename}")

# TXT 저장
txt_filename = "imdb_top250.txt"
with open(txt_filename, "w", encoding="utf-8") as f:
    for r in records:
        f.write(f"{r[0]:>3}. {r[1]} ({r[2]}) - 평점: {r[3]}\n")
print(f"[5] ✅ TXT 저장 완료: {txt_filename}")