from youtubesearchpython import VideosSearch
import pandas as pd
import re
from datetime import datetime
import os

# ✅ 텍스트 정제 함수
def clean_text(text):
    text = re.sub(r'[\n\r\t]', ' ', text)
    text = re.sub(r'[^\w가-힣 ]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# ✅ 조회수 문자열을 숫자로 변환 (예: '1.2만회' → 12000)
def convert_views_to_int(view_str):
    try:
        if '만' in view_str:
            return int(float(view_str.replace('만회', '').replace(',', '')) * 10000)
        return int(view_str.replace('회', '').replace(',', ''))
    except:
        return 0

# ✅ 사용자 입력
query = input("🔍 수집할 유튜브 검색 키워드를 입력하세요: ").strip()
limit_input = input("📦 몇 개의 결과를 수집할까요? (숫자만 입력): ").strip()
sort_option = input("⚙️ 정렬 방식 선택 (latest / views): ").strip().lower()

try:
    limit = int(limit_input)
except ValueError:
    print("❌ 숫자만 입력하세요.")
    exit()

# ✅ 날짜 생성
today = datetime.now().strftime('%Y%m%d')

# ✅ 저장 폴더 생성
output_dir = "hotplaces"
os.makedirs(output_dir, exist_ok=True)

# ✅ 수집 및 정제
data = []
collected = 0
search = VideosSearch(query, limit=20)

while collected < limit:
    results = search.result()

    for video in results['result']:
        if collected >= limit:
            break

        title = video.get('title', '')
        link = video.get('link', '')
        channel = video.get('channel', {}).get('name', '')
        published = video.get('publishedTime', '')
        views = video.get('viewCount', {}).get('short', '')
        desc = " ".join([d['text'] for d in video.get('descriptionSnippet', [])]) if video.get('descriptionSnippet') else ''

        clean_title = clean_text(title)
        clean_desc = clean_text(desc)

        data.append({
            'title': clean_title,
            'description': clean_desc,
            'channel': channel,
            'published': published,
            'views': views,
            'views_int': convert_views_to_int(views),
            'link': link
        })

        collected += 1

    if collected < limit:
        try:
            search.next()
        except:
            print("⚠️ 더 이상 데이터가 없습니다.")
            break

# ✅ DataFrame 생성 및 정렬
df = pd.DataFrame(data)

if sort_option == "views":
    df = df.sort_values(by="views_int", ascending=False)
elif sort_option == "latest":
    df = df.sort_values(by="published", ascending=False)

# ✅ 저장 파일 경로
safe_keyword = query.replace(' ', '').replace('#', '')
file_name = f"{safe_keyword}_{today}_sorted_{sort_option}.csv"
file_path = os.path.join(output_dir, file_name)

df.drop(columns="views_int").to_csv(file_path, index=False, encoding='utf-8-sig')

# ✅ 완료 메시지
print(f"\n🎉 총 {len(df)}개의 영상 정보를 정렬하여 [{file_path}] 파일에 저장했습니다.")