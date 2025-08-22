from bs4 import BeautifulSoup
import requests

# 웹 페이지 요청
url = "https://example.com"
res = requests.get(url)

# 파싱
soup = BeautifulSoup(res.text, "html.parser")# 기본 내장 파서
#soup = BeautifulSoup(res.text, "lxml") # 빠르고 유연함 (별도 설치 필요)
#soup = BeautifulSoup(res.text, "html5lib") # HTML5 구조로 파싱, 가장 유연함 (느림)


# 특정 태그 찾기
title = soup.find('h1').text
print("제목:", title)

# 여러 태그 리스트로 가져오기
links = soup.find_all('a')
for link in links:
    print(link.get('href'), link.text)