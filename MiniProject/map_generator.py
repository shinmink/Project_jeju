import requests
import pandas as pd
import folium
from tqdm import tqdm

# ✅ 장소 후보 리스트
place_candidates = [
    '성산일출봉', '협재해수욕장', '애월카페거리', '오설록', '우도', '산굼부리', '동문시장',
    '한라산', '비자림', '쇠소깍', '세화해변', '월정리', '김녕', '이호테우', '수목원길', '사려니숲길'
]

# ✅ Kakao API 키
KAKAO_API_KEY = '여기에_너의_카카오_REST_API_KEY를_입력하세요'


# ✅ 장소명 → 위경도 변환 함수
def get_location_kakao(query):
    headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    params = {"query": query, "category_group_code": "AT4", "size": 1}

    res = requests.get(url, headers=headers, params=params)
    if res.status_code == 200 and res.json()['documents']:
        doc = res.json()['documents'][0]
        return float(doc['y']), float(doc['x'])  # (lat, lon)
    return None, None


# ✅ 위경도 수집
locations = []
for place in tqdm(place_candidates):
    lat, lon = get_location_kakao(place)
    locations.append({
        "place": place,
        "latitude": lat,
        "longitude": lon
    })

# ✅ 데이터프레임으로 변환
df_locations = pd.DataFrame(locations)
df_locations = df_locations.dropna()

# ✅ 지도 시각화
jeju_map = folium.Map(location=[33.38, 126.53], zoom_start=10)

for _, row in df_locations.iterrows():
    folium.CircleMarker(
        location=(row["latitude"], row["longitude"]),
        radius=8,
        popup=row["place"],
        color="blue",
        fill=True,
        fill_color="skyblue"
    ).add_to(jeju_map)

# ✅ 저장
jeju_map.save("jeju_hotplaces_map.html")
print("✅ 지도 저장 완료: jeju_hotplaces_map.html")