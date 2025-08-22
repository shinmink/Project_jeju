import requests

# 접속 url
url = " https://www.visitjeju.net/kr/detail/list?menuId=DOM_000001718001000000 "
resp = requests.get(url, timeout=5) # 서버 요청 (5초 타임아웃)
resp.raise_for_status() # 오류(4xx·5xx) 발생 시 예외 발생

html = resp.text  # HTML 소스코드 가져오기
print(f"Status: {resp.status_code}") # 상태코드 인쇄 (200 이면 성공)
print(html[:300]) # 결과에서 앞의 300자만 미리보기