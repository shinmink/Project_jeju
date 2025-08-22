import pandas as pd
import re
import os
import glob
from datetime import datetime
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import shutil


# ✅ 0. 가장 최근에 생성된 hotplaces 디렉토리 내 csv 파일 찾기
csv_files = glob.glob("../hotplaces/*.csv")
if not csv_files:
    print("❌ 분석 가능한 hotplaces csv 파일이 없습니다.")
    exit()

latest_file = max(csv_files, key=os.path.getmtime)
print(f"📂 가장 최신 파일을 불러옵니다: {latest_file}")

# ✅ 1. 데이터 로드
df = pd.read_csv(latest_file, encoding="utf-8-sig")

# ✅ 2. 제목 + 설명 합치고 정제
text = (df['title'].fillna('') + ' ' + df['description'].fillna('')).str.cat(sep=' ')
text = re.sub(r'[^가-힣\s]', '', text)

# ✅ 3. 단어 추출 (2자 이상 한글 단어)
words = re.findall(r'[가-힣]{2,}', text)

# ✅ 4. 불용어 제거
stopwords = [
    '제주',
    '브이로그',
    '여행',
    '카페',
    '리뷰',
    '맛집',
    '추천',
    '영상',
    '장소',
    '소개',
    '일정',
    '정리',
    '정보',
    '투어',
    '충격적인',
    '싶은',
    '기안',
    '태연',
    '너무',
    '진짜',
    '이젠',
    '아주',
    '아무도',
    '안보고',
]
words = [word for word in words if word not in stopwords]

# ✅ 5. 빈도 분석
counter = Counter(words)
most_common = counter.most_common(100)

# ✅ 6. 워드클라우드 생성
wc = WordCloud(
    font_path="/System/Library/Fonts/Supplemental/AppleGothic.ttf",  # Mac 한글 폰트
    background_color="white",
    width=800,
    height=600
)
wc.generate_from_frequencies(dict(most_common))

# ✅ 7. 저장 디렉토리 생성 및 저장
date_str = datetime.now().strftime("%Y%m%d")
output_path = f"../wordcloud/wordcloud_{date_str}.png"  # ✅ 날짜별 백업 경로
os.makedirs("../wordcloud", exist_ok=True)
wc.to_file(output_path)
print(f"✅ 워드클라우드 저장 완료: {output_path}")

# 🔁 8. Flask 웹에 사용될 static 폴더에도 복사 (경로 수정됨)
static_path = "../static/wordcloud.png"  # 🆕 웹에서 고정 경로
os.makedirs("../static", exist_ok=True)  # 🆕 폴더 없으면 생성
shutil.copy(output_path, static_path)  # 🆕 복사 실행
print(f"✅ Flask static 폴더에 복사됨: {static_path}")

# ✅ 9. 화면 시각화
plt.figure(figsize=(10, 8))
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.tight_layout()
plt.savefig(output_path)
plt.show()

print(f"✅ 워드클라우드 생성 완료: {output_path}")