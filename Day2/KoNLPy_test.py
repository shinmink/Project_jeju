# KoNLPy 라이브러리가 설치되어 있지 않으면 “pip install konlpy”
from konlpy.tag import Okt

okt = Okt() # Okt 형태소 분석기 객체 생성
text = "제주도 흑돼지는 정말 맛있었고, 오션뷰도 최고였어요!"

morphemes = okt.morphs(text) # 1. 형태소 단위로 분해하기
# ['제주도', '흑돼지', '는', '정말', '맛있었고', ',', '오션뷰', '도', '최고', '였어요', '!']


nouns = okt.nouns(text) # 2. 명사만 추출하기
# ['제주도', '흑돼지', '정말', '맛', '오션뷰', '최고']