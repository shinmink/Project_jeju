from youtubesearchpython import VideosSearch
import pandas as pd
import re
from datetime import datetime
import os
import sys  # ✅ 추가된 부분: 외부 인자 처리용

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

# ✅ 메인 수집 함수 (🆕 Flask 등에서 함수 호출 가능하도록 리팩토링됨)
def collect_youtube_data(query, limit, sort_option):
    today = datetime.now().strftime('%Y%m%d')
    output_dir = "../hotplaces"
    os.makedirs(output_dir, exist_ok=True)

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

    df = pd.DataFrame(data)

    if sort_option == "views":
        df = df.sort_values(by="views_int", ascending=False)
    elif sort_option == "latest":
        df = df.sort_values(by="published", ascending=False)

    safe_keyword = query.replace(' ', '').replace('#', '')
    file_name = f"{safe_keyword}_{today}_sorted_{sort_option}.csv"
    file_path = os.path.join(output_dir, file_name)

    df.drop(columns="views_int").to_csv(file_path, index=False, encoding='utf-8-sig')

    return f"\n🎉 총 {len(df)}개의 영상 정보를 정렬하여 [{file_path}] 파일에 저장했습니다."

# ✅ 명령줄 실행용 (🆕 input → 인자 방식으로 교체됨)
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("❌ 사용법: python youtube_crawler_clean.py <query> <limit> <sort_option>")
        sys.exit(1)

    query = sys.argv[1]
    try:
        limit = int(sys.argv[2])
    except ValueError:
        print("❌ limit은 숫자여야 합니다.")
        sys.exit(1)
    sort_option = sys.argv[3].lower()

    result_message = collect_youtube_data(query, limit, sort_option)
    print(result_message)