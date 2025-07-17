import streamlit as st
import pandas as pd

# 제목
st.title("2025년 6월 기준 주민등록 인구 및 세대 현황")

# CSV 파일 경로 (필요 시 업로드 기능도 사용 가능)
FILE_PATH = "202506_202506_주민등록인구및세대현황_월간.csv"

# CSV 불러오기
try:
    df = pd.read_csv(FILE_PATH, encoding='euc-kr')
except Exception as e:
    st.error(f"CSV 파일을 불러오는 데 실패했습니다: {e}")
    st.stop()

# 총인구수 열 찾기
total_col = [col for col in df.columns if '총인구수' in col][0]

# 남녀 인구 열 추출 ('2025년05월_계_남자', '2025년05월_계_여자' 같은 열)
gender_cols = [col for col in df.columns if col.startswith('2025년05월_계_') and ('남자' in col or '여자' in col)]
gender_rename = {col: col.split('_')[-1] for col in gender_cols}  # '남자', '여자'

# 필요한 열만 선택하고 이름 바꾸기
df_filtered = df[['행정기관명', total_col] + gender_cols].copy()
df_filtered = df_filtered.rename(columns={total_col: '총인구수', **gender_rename})

# 숫자형 변환 (쉼표 제거)
df_filtered['총인구수'] = df_filtered['총인구수'].astype(str).str.replace(',', '').astype(int)
df_filtered['남자'] = df_filtered['남자'].astype(str).str.replace(',', '').astype(int)
df_filtered['여자'] = df_filtered['여자'].astype(str).str.replace(',', '').astype(int)

# 총인구수 기준 상위 5개 지역 추출
top5 = df_filtered.sort_values(by='총인구수', ascending=False).head(5)

# 📊 원본 데이터 출력
st.subheader("📄 상위 5개 행정구역 원본 데이터")
st.dataframe(top5)

# 📈 남녀 인구 시각화
st.subheader("👫 상위 5개 행정구역 남녀 인구 비교 (단위: 명)")

# 차트용 데이터 가공
chart_df = top5[['행정기관명', '남자', '여자']].set_index('행정기관명')

# st.line_chart는 세로축이 수치, 가로축이 인덱스인 형식이므로 그대로 사용
st.line_chart(chart_df)
