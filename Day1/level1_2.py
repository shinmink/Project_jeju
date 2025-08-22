import requests
from bs4 import BeautifulSoup

# 1. 요청할 URL 정의
url = "https://www.visitjeju.net/kr/detail/list?menuId=DOM_000001718001000000"
print("[1] 접속 시도 중...")

# 2. GET 요청 보내기 (타임아웃: 5초)
resp = requests.get(url, timeout=5)

# 3. 응답 상태 확인
print(f"[2] 응답 상태 코드: {resp.status_code}")  # 200이면 성공
resp.raise_for_status()  # 오류 발생 시 예외 처리

# 4. HTML 소스코드 파싱
html = resp.text
print(f"[3] HTML 전체 길이: {len(html)}자")
print(f"[4] HTML 미리보기 (앞 300자):\n{html[:300]}")

# 5. BeautifulSoup으로 HTML 파싱
soup = BeautifulSoup(html, "html.parser")

# 6. a 태그 중 링크가 포함된 것 추출
print("[5] 링크 추출 시작...")
links = soup.find_all("a", href=True)

# 7. 추출된 링크 출력 (최대 20개)
print(f"[6] 총 링크 개수: {len(links)}")
for i, link in enumerate(links[:20]):  # 20개까지만 미리보기
    href = link['href']
    text = link.get_text(strip=True)
    print(f"🔗 {i+1:>2}. 텍스트: {text or '(텍스트 없음)'}")
    print(f"     → 링크: {href}")

# 8. 끝
print("[7] 크롤링 완료 ✅")