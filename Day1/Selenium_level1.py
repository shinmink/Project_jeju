# 기본적인 브라우저 제어 코드:
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# 단계 1. 브라우저 실행
driver = webdriver.Chrome()

# 단계 2. 특정 URL로 이동
driver.get("https://www.visitjeju.net/kr/")

# 단계 3. 잠시 대기 (페이지 로딩을 위해)
time.sleep(3)

# 단계 4. 요소(Element) 찾기
# 예: 검색창(input 태그, id가 'search_bar'라고 가정) 찾기
search_box = driver.find_element(By.ID, "search_bar")

# 단계 5. 키보드로 글자 입력하기
search_box.send_keys("성산일출봉")

# 단계 6. 검색 버튼(button 태그, class가 'btn_search'라고 가정) 찾아 클릭하기
search_button = driver.find_element(By.CLASS_NAME, "btn_search")
search_button.click()