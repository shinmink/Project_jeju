import pandas as pd
import re
import os
import glob
from datetime import datetime
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
import platform
import shutil  # ✅ static 폴더 복사용


# ✅ 한글 폰트 설정 (Mac, Windows, Linux 대응)
if platform.system() == 'Darwin':  # macOS
    plt.rcParams['font.family'] = 'AppleGothic'
elif platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
else:
    plt.rcParams['font.family'] = 'NanumGothic'  # 리눅스용

plt.rcParams['axes.unicode_minus'] = False  # 마이너스 깨짐 방지

# ✅ 1. 최신 핫플레이스 파일 불러오기
csv_files = glob.glob("../hotplaces/*.csv")
if not csv_files:
    print("❌ hotplaces 폴더에 분석할 파일이 없습니다.")
    exit()

latest_file = max(csv_files, key=os.path.getmtime)
print(f"📂 최신 파일 로드: {latest_file}")
df = pd.read_csv(latest_file, encoding='utf-8-sig')

# ✅ 조회수 전처리: '1.2M', '850K', '10000' 등 → 정수
def parse_views(view_str):
    if isinstance(view_str, str):
        view_str = view_str.replace('views', '').strip()
        if 'K' in view_str:
            return int(float(view_str.replace('K', '')) * 1_000)
        elif 'M' in view_str:
            return int(float(view_str.replace('M', '')) * 1_000_000)
        elif view_str.isdigit():
            return int(view_str)
    return 0

df['views_int'] = df['views'].apply(parse_views)

# ✅ 2. 제목 + 설명 텍스트 정제
text = (df['title'].fillna('') + ' ' + df['description'].fillna('')).str.cat(sep=' ')
text = re.sub(r'[^가-힣\s]', '', text)

# ✅ 3. 키워드 추출 (2글자 이상 한글)
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
words = [w for w in words if w not in stopwords]

# ✅ 5. 키워드 빈도 상위 30개 추출
counter = Counter(words)
top_keywords = [kw for kw, _ in counter.most_common(30)]

# ✅ 6. 각 키워드를 포함한 영상의 평균 조회수 계산
keyword_stats = []
for keyword in top_keywords:
    mask = df['title'].str.contains(keyword) | df['description'].str.contains(keyword)
    views = df.loc[mask, 'views_int']
    if not views.empty:
        keyword_stats.append({
            'keyword': keyword,
            'count': len(views),
            'avg_views': views.mean()
        })

# ✅ 7. DataFrame 변환
df_kw = pd.DataFrame(keyword_stats).sort_values(by='avg_views', ascending=False)

# ✅ 9. 시각화
plt.figure(figsize=(12, 7))
plt.scatter(df_kw['keyword'], df_kw['avg_views'], color='orange')
plt.xticks(rotation=45, ha='right')
plt.title("핫플 키워드 vs 평균 조회수", fontsize=14)
plt.xlabel("핫플 키워드")
plt.ylabel("평균 조회수")
plt.grid(True)

# 📌 y축 범위 조절 (미세한 차이 강조용)
ymin = df_kw['avg_views'].min() * 0.9
ymax = df_kw['avg_views'].max() * 1.1
plt.ylim(ymin, ymax)

plt.tight_layout()
# ✅ 저장
output_dir = "../scatter"
os.makedirs(output_dir, exist_ok=True)
today = datetime.now().strftime('%Y%m%d')
file_name = os.path.join(output_dir, f"scatter_avgviews_{today}.png")
plt.savefig(file_name)
plt.show()

print(f"✅ 스캐터 플롯 저장 완료: {file_name}")

# 🆕 static 폴더에 웹용 이미지 복사
static_path = "../static/scatter.png"
os.makedirs("../static", exist_ok=True)
shutil.copy(file_name, static_path)
print(f"✅ Flask static 폴더에 복사됨: {static_path}")