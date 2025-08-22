from bs4 import BeautifulSoup
import requests

# 1. 요청할 URL
url = "https://example.com"
print(f"[1] URL 접속: {url}")

# 2. 웹 페이지 요청 (기본 GET)
res = requests.get(url)
print(f"[2] 응답 상태 코드: {res.status_code}")
res.raise_for_status()

# 3. BeautifulSoup으로 파싱
# ※ 기본 html.parser 사용, 다른 파서 선택지는 아래에 설명
soup = BeautifulSoup(res.text, "html.parser")
# soup = BeautifulSoup(res.text, "lxml")       # 속도 빠름 (설치 필요: pip install lxml)
# soup = BeautifulSoup(res.text, "html5lib")   # HTML5 완벽 파싱 (설치 필요: pip install html5lib)

print("[3] HTML 파싱 완료 ✅")

# 4. 제목 태그 (예: <h1>) 가져오기
title_tag = soup.find('h1')
if title_tag:
    print(f"[4] 페이지 제목 (h1): {title_tag.text.strip()}")
else:
    print("[4] 페이지에 <h1> 태그가 없습니다.")

# 5. 모든 링크 (<a> 태그) 가져오기
links = soup.find_all('a')
print(f"[5] 링크 수: {len(links)}개")

# 6. 링크 목록 출력 (최대 20개만 미리보기)
for i, link in enumerate(links[:20]):
    href = link.get('href')
    text = link.get_text(strip=True)
    print(f"🔗 {i+1:>2}. 텍스트: {text or '(텍스트 없음)'}")
    print(f"     → 링크: {href}")

print("[6] 크롤링 완료 🎉")