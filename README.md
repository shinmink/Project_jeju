
# 🏝️ 제주 핫플레이스 유튜브 트렌드 분석

> 유튜브 크롤링 + 텍스트 분석 + 시각화 기반 트렌드 인사이트 도출 프로젝트

## 📌 프로젝트 개요

- **목표**: 제주 핫플레이스 관련 유튜브 영상 데이터를 기반으로 키워드 트렌드 및 관심도 분석
- **기술 스택**: Python, YouTubeSearchPython, pandas, matplotlib, wordcloud

---

## ✅ 분석 단계 요약

### 1️⃣ 유튜브 영상 메타데이터 수집
- 키워드: `제주 핫플`, `제주 브이로그`, `제주 카페거리` 등
- 항목: 제목, 설명, 채널, 조회수, 업로드일, 링크
- 저장: `hotplaces/제주핫플_날짜.csv`

### 2️⃣ 키워드 워드클라우드
- 제목+설명에서 한글 키워드 추출
- 불용어 제거 → 워드클라우드 생성
- 결과: `wordcloud/wordcloud_날짜.png`

### 3️⃣ 키워드 vs 평균 조회수 분석
- 상위 키워드별 언급 영상들의 평균 조회수 계산
- 스캐터 플롯 시각화 (`x=키워드`, `y=평균 조회수`)
- 결과: `scatter/scatter_avgviews_날짜.png`

---

## 📁 폴더 구조

```
📁 project/
├── app.py                  # 👉 Flask 웹 서버
├── hotplaces/              # 유튜브 정제 CSV 저장 폴더
│   └── 제주핫플_20250820_sorted_views.csv
├── wordcloud/              # 워드클라우드 이미지 저장 폴더
│   └── wordcloud_20250820.png
├── scatter/                # 스캐터 플롯 이미지 저장 폴더
│   └── scatter_avgviews_20250820.png
├── templates/
│   └── index.html          # 👉 메인 HTML 템플릿
├── static/
│   ├── wordcloud.png       # 👉 복사해놓은 이미지
│   └── scatter.png
└── scripts/                # 분석 코드
    ├── youtube_crawler_clean.py
    ├── keyword_extractor.py
    └── scatter_plot.py
```
---
