# 📌 프로젝트: SNS 데이터로 보는 제주 '진짜' 핫플레이스 분석

| 항목 | 내용 |
| --- | --- |
| **프로젝트 목표** | SNS(인스타그램/블로그) 게시글에서 제주 핫플레이스를 발굴. 언급량, 키워드 분석 및 지도 시각화를 통해 트렌드 및 요인 분석 |
| **사용 기술 스택** | Python, requests, BeautifulSoup4, re, pandas, KoNLPy, wordcloud, matplotlib, folium, (Geocoding API) |

---

## 🧩 미니 프로젝트 정리

| 번호 | 미니프로젝트명 | 설명 | 주요 기술/도구 | 목표 |
| --- | --- | --- | --- | --- |
| #1 | 제주 관련 SNS 게시글 스크래핑 및 정제 | 블로그/인스타그램 게시글 제목, 본문, 해시태그 스크래핑 → 특수문자/광고 제거 | `requests`, `BeautifulSoup4`, `re`, `pandas` | - 웹 스크래핑 심화<br>- 정규표현식으로 데이터 정제<br>- DataFrame 저장 |
| #2 | NLP 기반 핵심 키워드 및 장소 추출 | KoNLPy로 명사 등 의미 있는 단어 추출 → 장소 이름 추출 및 빈도 분석 | `KoNLPy`, `pandas`, `wordcloud`, `matplotlib` | - 형태소 분석 및 품사 태깅<br>- 명사 추출 및 빈도 분석<br>- 워드클라우드 시각화 |
| #3 | 지도 시각화 및 인사이트 도출 | 장소명 → 위경도 변환 → Folium으로 지도에 시각화 (빈도 기반 CircleMarker) | `folium`, `pandas`, `Geocoding API (선택)` | - 장소 위경도 변환<br>- 데이터 병합<br>- 지도 시각화 및 인사이트 도출 |