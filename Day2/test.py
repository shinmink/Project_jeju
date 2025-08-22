import pandas as pd
import re

# CSV 파일 읽기
df = pd.read_csv('fulldata_동물병원.csv', encoding='cp949')

# 열 이름 확인 (디버깅용)
print("열 목록:", df.columns.tolist())

# 상위 100개만 추출 (복사본)
df_sample = df.head(100).copy()

# 실제 열 이름 정확히 입력
# 열 이름 출력 후 맞춰서 수정할 것
target_columns = ['사업장명', '도로명주소', '소재지전체주소', '상세업무구분명']

# 정제 함수
def clean_text(text):
    if pd.isnull(text):
        return ""
    text = str(text)
    text = re.sub(r"[^가-힣0-9\s]", " ", text)  # 한글, 숫자, 공백만
    text = re.sub(r"\s+", " ", text).strip()
    return text

# 열별 정제 수행
for col in target_columns:
    if col in df_sample.columns:
        cleaned_col = f"{col}_정제"
        df_sample[cleaned_col] = df_sample[col].apply(clean_text)
    else:
        print(f"⚠️ 열 '{col}'이 존재하지 않습니다.")

# 결과 출력
출력열 = [col for col in df_sample.columns if any(t in col for t in target_columns)]
print(df_sample[출력열])