import matplotlib.pyplot as plt
import seaborn as sns

df = sns.load_dataset('titanic')  # 타이타닉 탑승자 데이터

# IQR Rule로 이상치 찾기
Q1 = df['fare'].quantile(0.25)
Q3 = df['fare'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# 이상치를 제외한 데이터만 필터링
df_no_outlier = df[(df['fare'] >= lower_bound) & (df['fare'] <= upper_bound)]

# 확인용 출력
print(f"전체 데이터 수: {len(df)}")
print(f"이상치 제외 후 데이터 수: {len(df_no_outlier)}")

# Box Plot으로 시각적으로 확인
sns.boxplot(data=df, y='fare')  # '가격' -> 'fare' 로 수정
plt.show()

