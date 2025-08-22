
import requests
import pandas as pd

# 1. API 정보 (공공데이터포털 신청 필요)
endpoint = "https://api.jejudatahub.net/v2/realtimedata/search"  # 예시 용도, 실제 URL은 공공데이터포털 확인 필요
service_key = "jj21pbtbr3p9o19222cjt323132tr9j9"

params = {
    'serviceKey': service_key,
    'datasetId': 'jeju_daily_ev_charging',  # 예시
    'startDt': '2023-01-01',
    'endDt': '2023-01-31',
}

print(f"[1] 제주도 일별 전기차 충전 이력 조회 중...")
res = requests.get(endpoint, params=params)
res.raise_for_status()
data = res.json()

records = data.get("data", [])

df = pd.DataFrame(records)
print("[2] 데이터 로딩 완료. 일부 컬럼 출력:")
print(df.head())

# CSV 저장
csv_name = "jeju_ev_charging_jan2023.csv"
df.to_csv(csv_name, index=False, encoding="utf-8-sig")
print(f"[3] CSV 저장 완료: {csv_name}")

# TXT 저장
txt_name = "jeju_ev_charging_jan2023.txt"
with open(txt_name, "w", encoding="utf-8") as f:
    for _, row in df.iterrows():
        f.write(f"{row.to_dict()}\n")
print(f"[4] TXT 저장 완료: {txt_name}")